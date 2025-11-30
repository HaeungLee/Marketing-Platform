# Gemini가 제안하는 Marketing-Platform 리팩토링 방안

이 문서는 현재 코드베이스를 정적 분석하여 도출된 리팩토링 제안 사항을 정리한 것입니다. 프로젝트의 안정성, 유지보수성, 확장성을 향상시키는 것을 목표로 합니다.

---

## 🎯 Backend 개선 제안

### 1. `insights_analysis_service.py` 리팩토링

- **문제점 1: 하드코딩된 경로**
  - `MCPServerConnector` 클래스 내 `server_path`가 로컬 경로(`"d:/FinalProjects/Marketing-Platform/mcp-server"`)로 하드코딩되어 있어 다른 환경에서의 실행을 불가능하게 합니다.
- **제안:**
  - 환경 변수(`os.getenv`)나 설정 파일(`config/settings.py`)을 통해 경로를 주입받도록 수정하여 이식성을 높입니다.

- **문제점 2: 불안정한 MCP 서버 호출 방식**
  - `subprocess.shell`을 사용하여 Node.js 스크립트를 직접 실행하는 방식은 오류 처리, 타임아웃 관리, 성능 모니터링이 어렵고 불안정합니다.
- **제안:**
  - `docker-compose.yml`에 이미 `mcp-server`가 서비스로 정의되어 있으므로, Docker 네트워크를 통해 직접 HTTP API 요청을 보내는 방식으로 변경합니다. `httpx`나 `aiohttp` 라이브러리를 사용하여 비동기 요청을 보낼 수 있습니다.

- **문제점 3: Mock 데이터와 실제 로직의 혼재**
  - `MCPServerConnector`에 Mock 데이터 반환 로직(`_mock_tool_call`)이 포함되어 있어 코드가 복잡하고 테스트가 어렵습니다.
- **제안:**
  - 개발/테스트 환경을 위한 `MockMCPServerConnector` 클래스를 별도로 분리합니다. 의존성 주입(Dependency Injection) 패턴을 사용하여 실제 환경과 테스트 환경에서 다른 구현체를 사용하도록 설정합니다.

- **문제점 4: 광범위한 예외 처리**
  - 각 서비스 메서드(`analyze_target_customers` 등)의 `try...except Exception` 블록이 너무 광범위하여 모든 예외를 동일하게 처리하고 기본값을 반환합니다. 이는 디버깅을 어렵게 만듭니다.
- **제안:**
  - `mcp_connector.call_tool`에서 발생할 수 있는 구체적인 예외(e.g., `httpx.ConnectError`, `TimeoutError`)를 명시적으로 처리하고, 그 외의 예외는 API 최상단 레벨의 예외 처리 미들웨어에서 처리하여 일관된 오류 응답을 반환하도록 구조를 개선합니다.

### 2. Domain Models (`domain/models/*.py`) 개선

- **문제점: 비표준 인덱스 정의**
  - `BusinessStore` 모델 등에서 `class Meta`를 사용하여 인덱스를 정의하는 것은 Django 스타일이며, SQLAlchemy의 표준 방식이 아닙니다.
- **제안:**
  - SQLAlchemy의 `Index` 구문을 사용하여 테이블 정의와 함께 명시적으로 인덱스를 생성합니다.
    ```python
    from sqlalchemy import Index
    # ... 모델 클래스 정의 후 ...
    Index('ix_business_stores_location', BusinessStore.sido_name, BusinessStore.sigungu_name, BusinessStore.dong_name)
    ```

- **문제점: 일관성 없는 임포트 경로**
  - `user.py`에서 `from ..database import Base`와 같이 상대 경로 임포트를 사용하여 순환 참조의 위험이 있습니다.
- **제안:**
  - `from src.config.database import Base`와 같이 프로젝트 루트를 기준으로 하는 절대 경로 임포트를 일관되게 사용하여 코드의 명확성과 안정성을 높입니다.

---

## 🎨 Frontend 개선 제안

### 1. API 서비스 로직 (`services/*.ts`) 개선

- **문제점 1: 하드코딩된 API URL**
  - `apiService.ts`의 `generateImage` 함수 내에 `http://localhost:8000/api/images/generate` URL이 하드코딩되어 있습니다.
- **제안:**
  - `api.ts`의 `apiClient`와 동일하게 `.env` 파일의 환경 변수(`VITE_API_URL`)를 사용하도록 수정하여 환경별 설정을 용이하게 합니다.

- **문제점 2: 중복 `axios` 인스턴스 사용**
  - `populationService.ts`는 `apiClient`를 사용하지 않고 별도의 `axios` 인스턴스를 생성하여 사용합니다. 이로 인해 `apiClient`에 설정된 요청/응답 인터셉터(인증 토큰 주입, 401 에러 시 자동 로그아웃 등)가 적용되지 않아 일관성이 깨집니다.
- **제안:**
  - `populationService.ts`에서도 `apiClient`를 임포트하여 모든 API 호출을 일관된 방식으로 처리하도록 통일합니다.

- **문제점 3: 클라이언트 사이드 비즈니스 로직**
  - `populationService.ts`의 `analyzePopulationTrend`, `generateInsights` 메서드는 서버에서 처리해야 할 분석 및 인사이트 도출 로직을 포함하고 있습니다.
- **제안:**
  - 해당 로직을 백엔드 API로 이전하고, 프론트엔드는 결과 데이터를 받아 표시하는 역할만 담당하도록 변경합니다. 이를 통해 로직을 중앙에서 관리하고 재사용성을 높일 수 있습니다.

### 2. React 컴포넌트 (`pages/*.tsx`) 개선

- **문제점: 복잡한 비동기 상태 관리**
  - `PopulationDashboardPage.tsx` 등에서 `useState`와 `useEffect`를 과도하게 사용하여 데이터 페칭, 로딩, 에러 상태를 수동으로 관리하고 있어 코드가 복잡하고 잠재적인 버그 발생 가능성이 높습니다.
- **제안:**
  - `React Query` (`TanStack Query`) 또는 `SWR`과 같은 서버 상태 관리 라이브러리를 도입합니다. 이를 통해 데이터 페칭, 캐싱, 로딩/에러 상태 관리를 선언적이고 효율적으로 처리하여 코드의 가독성과 안정성을 크게 향상시킬 수 있습니다.

- **문제점: 불필요한 임시 파일 존재**
  - `apiService.ts.new`, `PopulationDashboardPage.tsx.new` 등 리팩토링 과정에서 생성된 것으로 보이는 임시 파일들이 남아있습니다.
- **제안:**
  - 작업이 완료된 파일들은 원본 파일에 병합하고, 불필요한 `.new` 파일들을 삭제하여 코드베이스를 깔끔하게 정리합니다.

---

## 🚀 종합 제안

1.  **API 통신 방식 개선 (최우선):** 백엔드와 MCP 서버 간의 통신을 `subprocess` 대신 **HTTP API**로 변경하여 안정성과 확장성을 확보합니다.
2.  **프론트엔드 상태 관리 라이브러리 도입:** **`React Query`**를 도입하여 API 데이터 관리 로직을 혁신적으로 개선하고 개발 생산성을 높입니다.
3.  **코드 일관성 확보:** 모든 API 호출이 `apiClient`를 사용하도록 통일하고, 임포트 경로와 파일명을 정리하여 프로젝트의 일관성을 유지합니다.
4.  **환경 변수 활용:** 하드코딩된 모든 경로와 URL을 환경 변수로 분리하여 배포 유연성을 확보합니다.
