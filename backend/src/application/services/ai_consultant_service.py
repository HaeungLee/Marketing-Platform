"""
AI 상담 서비스 - 소상공인 특화 상담 시스템
"""
from typing import Dict, Any, Optional
from src.infrastructure.ai.gemini_service import GeminiService


class AIConsultantService(GeminiService):
    """소상공인 특화 AI 상담 서비스"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.consultation_prompt = self._get_consultation_system_prompt()
    
    def _get_consultation_system_prompt(self) -> str:
        """소상공인 상담 전용 시스템 프롬프트"""
        return """
당신은 한국의 소상공인 전문 경영 컨설턴트입니다.

**전문 분야:**
- 상권 분석 및 입지 선정
- 업종별 창업 전략 수립
- 마케팅 및 홍보 방안
- 정부 지원사업 및 제도 안내
- 경영 개선 및 수익성 향상

**답변 원칙:**
1. 실용적이고 구체적인 조언 제공
2. 한국 시장 상황에 맞는 현실적 솔루션
3. 단계별 실행 가능한 액션 플랜 제시
4. 관련 정부 지원사업이나 제도 정보 포함
5. 비용 효율적인 방안 우선 제안

**답변 형식:**
- 친근하고 전문적인 톤
- 구체적인 숫자나 예시 포함
- 실행 단계를 명확히 구분
- 추가 질문이나 상담이 필요한 부분 안내

항상 소상공인의 입장에서 생각하고, 실제로 도움이 되는 조언을 해주세요.
"""

    async def get_consultation(self, 
                             question: str, 
                             business_type: Optional[str] = None,
                             region: Optional[str] = None,
                             budget: Optional[str] = None,
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """AI 상담 응답 생성"""
        try:
            # 상담 컨텍스트 구성
            context_info = self._build_consultation_context(
                business_type, region, budget, context
            )
            
            # 상담 프롬프트 생성
            full_prompt = f"{self.consultation_prompt}\n\n{context_info}\n\n사용자 질문: {question}"
            
            # Gemini API 호출
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
                contents=full_prompt
            )
            
            # 응답 파싱
            answer = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    answer += part.text
            
            return {
                "answer": answer.strip(),
                "context": context_info,
                "question": question,
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            print(f"AI 상담 오류: {e}")
            return self._get_fallback_consultation_response(question)
    
    def _build_consultation_context(self, 
                                  business_type: Optional[str] = None,
                                  region: Optional[str] = None,
                                  budget: Optional[str] = None,
                                  additional_context: Optional[Dict[str, Any]] = None) -> str:
        """상담 컨텍스트 구성"""
        context_parts = []
        
        if business_type:
            context_parts.append(f"업종: {business_type}")
        
        if region:
            context_parts.append(f"지역: {region}")
            
        if budget:
            context_parts.append(f"예산: {budget}")
            
        if additional_context:
            for key, value in additional_context.items():
                if value:
                    context_parts.append(f"{key}: {value}")
        
        if context_parts:
            return f"**상담 정보:**\n" + "\n".join(f"- {part}" for part in context_parts) + "\n"
        
        return ""
    
    def _get_fallback_consultation_response(self, question: str) -> Dict[str, Any]:
        """서비스 오류 시 대체 응답"""
        fallback_responses = {
            "상권": "상권 분석을 위해서는 다음을 고려해보세요:\n\n1. **유동인구 조사**: 시간대별, 요일별 유동인구 패턴 분석\n2. **경쟁업체 현황**: 반경 500m 내 동종업체 수와 운영현황\n3. **접근성**: 대중교통, 주차시설, 도보 접근성\n4. **임대료 수준**: 매출 대비 임대료 비율 10-15% 권장\n\n소상공인시장진흥공단의 상권정보시스템(상권넷)을 활용해보세요.",
            
            "창업": "창업 준비 단계별 체크리스트:\n\n1. **시장조사**: 목표 고객층, 시장 규모, 경쟁 현황\n2. **사업계획서**: 수익모델, 마케팅 전략, 재무계획\n3. **자금조달**: 창업지원금, 정책자금, 투자 유치\n4. **법적 준비**: 사업자등록, 각종 인허가, 보험 가입\n\n중소벤처기업부의 창업지원사업을 확인해보시기 바랍니다.",
            
            "마케팅": "효과적인 소상공인 마케팅 방법:\n\n1. **온라인 마케팅**: 네이버 플레이스, 인스타그램, 블로그\n2. **지역밀착**: 동네 커뮤니티, 전단지, 현수막\n3. **고객관리**: 단골 고객 우대, 리뷰 관리, 추천 이벤트\n4. **협력마케팅**: 주변 상권과의 공동 프로모션\n\n소상공인시장진흥공단의 마케팅 지원사업도 활용해보세요.",
            
            "지원사업": "주요 소상공인 지원사업:\n\n1. **소상공인시장진흥공단**: 경영개선, 마케팅, 교육지원\n2. **중소벤처기업부**: 창업지원금, 기술개발지원\n3. **지자체 지원**: 지역별 특화 지원사업\n4. **온라인 판로**: 온라인쇼핑몰 입점 지원\n\n정부24나 소상공인지원센터에서 더 자세한 정보를 확인하세요."
        }
        
        # 키워드 매칭으로 적절한 응답 선택
        for keyword, response in fallback_responses.items():
            if keyword in question:
                return {
                    "answer": response,
                    "context": "",
                    "question": question,
                    "timestamp": self._get_current_timestamp(),
                    "fallback": True
                }
        
        # 기본 응답
        return {
            "answer": """안녕하세요! 소상공인 AI 상담사입니다. 🏪

궁금한 내용을 좀 더 구체적으로 말씀해 주시면 더 정확한 도움을 드릴 수 있습니다.

**상담 가능 분야:**
• 📍 상권 분석 및 입지 선정
• 🚀 창업 전략 및 사업계획
• 📢 마케팅 및 홍보 방안  
• 💰 정부 지원사업 정보
• 📊 경영 개선 방안

어떤 분야에 대해 도움이 필요하신가요?""",
            "context": "",
            "question": question,
            "timestamp": self._get_current_timestamp(),
            "fallback": True
        }
    
    def _get_current_timestamp(self) -> str:
        """현재 시간 문자열 반환"""
        from datetime import datetime
        return datetime.now().isoformat()
