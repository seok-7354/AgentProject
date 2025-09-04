# LangGraph MCP Agent Template

LangGraph와 OpenRouter를 활용한 Model Context Protocol(MCP) 통합 ReAct 에이전트 템플릿입니다.

## 개요

이 템플릿은 MCP(Model Context Protocol) 도구를 동적으로 로드하고 활용할 수 있는 지능형 에이전트를 구축하기 위한 프로덕션 준비된 기반을 제공합니다. LangGraph의 `create_react_agent`를 기반으로 구축되어 OpenRouter를 통한 다양한 AI 모델과의 원활한 통합과 유연한 MCP 서버 구성을 지원합니다.

## 주요 기능

- **동적 MCP 도구 로딩**: 구성된 서버에서 MCP 도구를 자동으로 탐지하고 로드
- **다중 모델 지원**: OpenRouter API를 통한 다양한 AI 모델 지원
- **유연한 구성**: 합리적인 기본값을 가진 환경 기반 구성
- **ReAct 에이전트 패턴**: 복잡한 문제 해결을 위한 추론 및 행동 패턴 구현
- **프로덕션 준비**: 포괄적인 오류 처리 및 로깅
- **확장 가능한 아키텍처**: 사용자 정의 도구 추가 및 동작 수정 용이

## 전제 조건

- Python 3.11 이상
- [uv](https://github.com/astral-sh/uv) 패키지 매니저
- OpenRouter API 키
- LangGraph 및 MCP 개념에 대한 기본 이해

## 설치

### 1. uv 패키지 매니저 설치

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**대안 (pip를 통한 설치):**
```bash
pip install uv
```

### 2. 프로젝트 클론 및 설정

```bash
git clone https://github.com/teddynote-lab/langgraph-mcp-agent-template.git
cd langgraph-mcp-agent-template
uv sync
```

## 구성

### 환경 변수

프로젝트 루트에 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

다음 변수들을 구성합니다:

```env
# 필수: OpenRouter API 구성
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# 선택사항: LangSmith 추적 (개발 시 권장)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=LangGraph-MCP-Agent-Template

# 선택사항: 기본 모델 재정의
MODEL=anthropic/claude-3-5-sonnet-20241022

# 선택사항: 사용자 정의 MCP 구성 경로
MCP_CONFIG_PATH=mcp_config.json
```

### MCP 서버 구성

`mcp_config.json`에서 MCP 서버를 구성합니다:

```json
{
  "weather": {
    "command": "uv",
    "args": ["run", "python", "server/mcp_server_local.py"],
    "transport": "stdio"
  },
  "web_search": {
    "url": "https://api.example.com/mcp",
    "transport": "streamable_http"
  }
}
```

#### 구성 옵션

**로컬 MCP 서버 (stdio 전송):**
```json
{
  "server_name": {
    "command": "python",
    "args": ["path/to/server.py"],
    "transport": "stdio"
  }
}
```

**원격 MCP 서버 (HTTP 전송):**
```json
{
  "server_name": {
    "url": "https://api.example.com/mcp",
    "transport": "streamable_http"
  }
}
```

## 사용법

### 개발 서버 시작

```bash
uv run langgraph dev
```

이 명령어는 LangGraph 개발 서버를 시작하고 자동으로:
- 구성된 서버에서 MCP 도구를 로드
- 선택된 모델로 ReAct 에이전트를 초기화
- LangGraph Studio 인터페이스를 실행

### 에이전트 액세스

1. 제공된 URL(일반적으로 `https://smith.langchain.com/studio/...`)로 브라우저를 열기
2. LangGraph Studio 인터페이스를 사용하여 에이전트와 상호작용
3. 에이전트는 구성된 모든 MCP 도구에 자동으로 액세스 가능

### 상호작용 예시

```
사용자: 서울의 날씨는 어떤가요?
에이전트: 서울의 날씨를 확인해드리겠습니다.

[도구 호출: weather_check with location="Seoul"]
[도구 응답: "서울은 현재 맑고 기온은 22°C입니다"]

현재 서울은 맑은 날씨이며 기온은 22°C입니다.
```

## 아키텍처

### 프로젝트 구조

```
langgraph-mcp-agent-template/
├── src/mcp_agent/
│   ├── __init__.py          # 패키지 초기화
│   ├── context.py           # 구성 및 컨텍스트 관리
│   ├── graph.py             # 메인 에이전트 그래프 정의
│   ├── prompts.py           # 시스템 프롬프트 및 템플릿
│   ├── state.py             # 상태 관리 스키마
│   ├── tools.py             # MCP 도구 로딩 및 관리
│   └── utils.py             # 유틸리티 함수
├── server/
│   └── mcp_server_local.py  # 예시 로컬 MCP 서버
├── mcp_config.json          # MCP 서버 구성
├── langgraph.json           # LangGraph 프로젝트 구성
├── pyproject.toml           # 프로젝트 의존성
└── .env.example             # 환경 변수 템플릿
```

### 핵심 컴포넌트

#### 컨텍스트 관리 (`context.py`)
- 구성 매개변수 관리
- 환경 변수 주입 처리
- 타입 안전 구성 액세스 제공

#### 도구 로딩 (`tools.py`)
- 구성된 서버에서 MCP 도구를 동적으로 로드
- stdio 및 HTTP 전송 프로토콜 모두 처리
- 오류 복원력 및 폴백 메커니즘 제공

#### 에이전트 그래프 (`graph.py`)
- `create_react_agent`를 사용한 ReAct 패턴 구현
- MCP 도구를 추론 루프와 통합
- 포괄적인 오류 처리 제공

### 구성 우선순위

시스템은 다음과 같은 구성 우선순위 순서를 따릅니다:

1. **명시적 생성자 인수** (최고 우선순위)
2. **환경 변수** (대문자 필드명)
3. **기본값** (데이터클래스 필드에 정의됨)

예시:
```python
# 환경 변수 MODEL이 기본값보다 우선
# export MODEL="openai/gpt-4-turbo"
context = Context()  # 환경에서 MODEL 사용

# 명시적 인수가 환경보다 우선
context = Context(model="anthropic/claude-3-haiku")
```

## 개발

### 사용자 정의 MCP 서버 추가

1. MCP 서버 구현 생성
2. `mcp_config.json`에 서버 구성 추가
3. 개발 서버 재시작

### 에이전트 동작 수정

`src/mcp_agent/prompts.py`에서 시스템 프롬프트를 편집합니다:

```python
SYSTEM_PROMPT = """
당신은 다양한 도구에 접근할 수 있는 도움이 되는 어시스턴트입니다.
사용 가능한 도구를 활용하여 정확하고 도움이 되는 응답을 제공하세요.
"""
```

### 디버깅

환경 변수를 설정하여 상세한 로깅을 활성화합니다:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=your_key
uv run langgraph dev
```

## 지원 모델

템플릿은 OpenRouter를 통해 사용 가능한 모든 모델을 지원합니다. 인기 있는 선택지는 다음과 같습니다:

- `anthropic/claude-3-5-sonnet-20241022` (기본값)
- `openai/gpt-4-turbo`
- `openai/gpt-4o`
- `meta-llama/llama-3.1-405b-instruct`
- `google/gemini-pro-1.5`

## 문제 해결

### 일반적인 문제

**MCP 서버 연결 실패:**
```
❌ MCP 도구 로드 실패: unhandled errors in a TaskGroup
```
- `mcp_config.json`에서 MCP 서버 구성 확인
- 서버 명령어/URL이 접근 가능한지 확인
- 상세한 오류 정보를 위해 서버 로그 확인

**OpenRouter 인증 실패:**
```
❌ 에이전트 실행 실패: Unauthorized
```
- `.env` 파일에서 `OPENROUTER_API_KEY` 확인
- API 키가 충분한 크레딧/권한을 가지고 있는지 확인

**도구 로딩 문제:**
```
⚠️ MCP 설정 파일 없음: mcp_config.json
```
- 프로젝트 루트에 `mcp_config.json` 생성
- 파일 형식이 유효한 JSON인지 확인
- 파일 권한 확인

### 도움 요청

1. [LangGraph 문서](https://langchain-ai.github.io/langgraph/) 확인
2. [MCP 사양](https://modelcontextprotocol.io/docs) 검토
3. 상세한 오류 정보를 위해 서버 로그 검토
4. 요청 디버깅을 위해 LangSmith 추적 활성화

## 기여

기여를 환영합니다! 다음 가이드라인을 따라주세요:

1. 저장소를 포크
2. 기능 브랜치 생성
3. 적절한 테스트와 함께 변경사항 작성
4. 명확한 설명과 함께 풀 리퀘스트 제출

### 개발 설정

```bash
git clone https://github.com/<your-username>/langgraph-mcp-agent-template.git
cd langgraph-mcp-agent-template
uv sync --dev
uv run pytest  # 테스트 실행 (사용 가능한 경우)
```

## 라이센스

MIT License

----

made by teddynote LAB
