# AI 기능 구현 계획 (Claude Trade MAX)

## 개요
사용자 요청: 
1. 웹사이트(앱)에서 AI에게 묻는 기능 연계
2. Gemini API 통합 (무료 티어 베스트)
3. 실시간 포트폴리오 가격 변동 모니터링
4. Gemini + GPT + Claude + Grok 4AI 토론 및 결론 시스템 (AI Council)

## 사용 기술 스텝
- **Gemini API**: 무료 티어 가장 관대한 limit (Flash 모델). 한글 지원 좋음. 사용자가 자신의 API Key 입력 (설정 페이지).
- **실시간 가격**: 기존 backend (/api/quote) 활용. 1~2분 자동 폴링 추가. 변동 % , 총 가치, 방향 표시 강화.
- **Multi-AI Council**: Gemini 하나로 4AI 페르소나 시뮬레이션 (Grok: 진실추구, Claude: 신중, GPT: 창의적, Gemini: 데이터 기반). 토론 구조 프롬프트로 각 의견 -> 바람 -> 최종 결론 + 구체 행동 제안 (rebalance % 등). 
  나중에 OpenRouter 통해 실제 4개 모델 호출 지원 추가 가능.

## 구현 단계
1. **1단계 (현재)**: 실시간 가격 변동 모니터링 강화 + 포트폴리오 총 가치/변동 표시
2. **2단계**: Gemini API Key 설정 + AI 채팅 기능 추가 (portfolio context 자동 주입)
3. **3단계**: AI Council 모드 구현 (4AI 토론 시뮬 + 결론)
4. **4단계** (optional): OpenRouter 지원 및 디자인 업그레이드

## 보안
- API Key는 localStorage 저장 (사용자 기기). 백엔드 프록시 추천 (frontend 키 노출 방지).
- 비용: Gemini 무료 티어 내 사용 가능. 다수 호출 시 OpenRouter 크레딕 필요.

## 다음 작업
- App.jsx 에 실시간 자동 갱신 useEffect 추가
- Holdings 표시 에 live change % , 화살표, 포트폴리오 통계 카드 추가
- 새 탭 "AI 상담" 또는 플로팅 채팅 버튼 추가

---
**Claude Trade MAX** 개인 포트폴리오 트래킹 + AI 어드바이저 앱
