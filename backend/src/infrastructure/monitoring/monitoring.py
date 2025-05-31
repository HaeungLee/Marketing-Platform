"""
핵심 시스템 모니터링 설정
"""
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Gauge, Counter, Histogram
import psutil
import logging
from discord_webhook import DiscordWebhook
from typing import Dict, Any
import time
import asyncio
from config.settings import settings

# 메트릭 정의
SYSTEM_MEMORY_USAGE = Gauge("system_memory_usage_percent", "System memory usage in percent")
SYSTEM_CPU_USAGE = Gauge("system_cpu_usage_percent", "System CPU usage in percent")
DATABASE_CONNECTION_COUNT = Gauge("database_connection_count", "Number of active database connections")
API_ERROR_COUNT = Counter("api_error_count", "Number of API errors", ["endpoint", "error_type"])
API_RESPONSE_TIME = Histogram(
    "api_response_time_seconds",
    "API response time in seconds",
    ["endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

def init_instrumentator(app: FastAPI) -> None:
    """Prometheus 미들웨어 초기화"""
    Instrumentator().instrument(app).expose(app)

class MonitoringService:
    def __init__(self, app: FastAPI, discord_webhook_url: str):
        self.app = app
        self.discord_webhook_url = discord_webhook_url
        self.error_count: Dict[str, int] = {}
        self.last_alert_time: Dict[str, float] = {}
        self.alert_cooldown = 300  # 5분 쿨다운

        # 임계값 설정
        self.memory_threshold = settings.memory_threshold
        self.cpu_threshold = settings.cpu_threshold
        self.error_threshold = settings.error_threshold

    async def _send_alert(self, message: str):
        """Discord로 알림 전송"""
        try:
            webhook = DiscordWebhook(
                url=self.discord_webhook_url,
                content=f"```\n{message}\n```"
            )
            response = webhook.execute()
            if not response:
                logging.error(f"Discord webhook 실패: 응답 없음")
            elif response.status_code != 200:
                logging.error(f"Discord webhook 실패: {response.status_code}")
        except Exception as e:
            logging.error(f"Discord 알림 전송 실패: {str(e)}")

    async def setup(self):
        """모니터링 설정"""
        # 초기 연결 테스트
        await self._send_alert("🟢 모니터링 시스템이 시작되었습니다.")
        
        # 시스템 메트릭 수집 시작
        asyncio.create_task(self._collect_system_metrics())

    async def _collect_system_metrics(self):
        """시스템 메트릭 수집"""
        while True:
            try:
                # 시스템 메트릭 수집
                memory_percent = psutil.virtual_memory().percent
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # 메트릭 업데이트
                SYSTEM_MEMORY_USAGE.set(memory_percent)
                SYSTEM_CPU_USAGE.set(cpu_percent)
                
                # 임계값 체크 및 알림
                await self._check_thresholds(memory_percent, cpu_percent)
                
                await asyncio.sleep(60)  # 1분 간격으로 체크
            except Exception as e:
                logging.error(f"메트릭 수집 중 오류 발생: {str(e)}")
                await asyncio.sleep(60)

    async def _check_thresholds(self, memory_percent: float, cpu_percent: float):
        """임계값 체크 및 알림"""
        current_time = time.time()

        # 메모리 사용량 체크
        if memory_percent > self.memory_threshold:
            if self._should_send_alert("memory"):
                await self._send_alert(f"🚨 높은 메모리 사용량: {memory_percent:.1f}% (임계값: {self.memory_threshold}%)")
                self.last_alert_time["memory"] = current_time

        # CPU 사용량 체크
        if cpu_percent > self.cpu_threshold:
            if self._should_send_alert("cpu"):
                await self._send_alert(f"🚨 높은 CPU 사용량: {cpu_percent:.1f}% (임계값: {self.cpu_threshold}%)")
                self.last_alert_time["cpu"] = current_time

    def _should_send_alert(self, alert_type: str) -> bool:
        """알림 전송 여부 확인"""
        current_time = time.time()
        last_alert = self.last_alert_time.get(alert_type, 0)
        return (current_time - last_alert) > self.alert_cooldown

    async def record_api_error(self, endpoint: str, error_type: str):
        """API 에러 기록"""
        try:
            API_ERROR_COUNT.labels(endpoint=endpoint, error_type=error_type).inc()
            
            # 에러 카운트 증가
            key = f"{endpoint}:{error_type}"
            self.error_count[key] = self.error_count.get(key, 0) + 1
            
            # 임계값 초과시 알림
            if self.error_count[key] >= self.error_threshold:
                if self._should_send_alert(key):
                    await self._send_alert(
                        f"🚨 다수의 API 에러 발생!\n"
                        f"엔드포인트: {endpoint}\n"
                        f"에러 타입: {error_type}\n"
                        f"발생 횟수: {self.error_count[key]}\n"
                        f"임계값: {self.error_threshold}"
                    )
                    self.last_alert_time[key] = time.time()
                    self.error_count[key] = 0
        except Exception as e:
            logging.error(f"에러 기록 중 오류 발생: {str(e)}")
