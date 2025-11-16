"""LangGraph MCP Agent를 Python 코드로 직접 사용하는 예시"""

import argparse
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from mcp_agent.graph import graph
from mcp_agent.context import Context

# .env 파일 로드 (OPENROUTER_API_KEY 등을 읽기 위해)
load_dotenv()


async def main(model: str = None, message: str = None):
    """에이전트에 메시지를 보내고 응답을 받는 예시
    
    Args:
        model: 사용할 모델명 (예: "openai/gpt-4-turbo", "google/gemini-2.0-flash-exp:free")
              None이면 환경 변수 MODEL 또는 기본값 사용
        message: 보낼 메시지 (None이면 기본 메시지 사용)
    """
    
    # 초기 상태 생성 (사용자 메시지 포함)
    user_message = message or "서울의 날씨는 어떤가요?"
    initial_state = {
        "messages": [
            HumanMessage(content=user_message)
        ]
    }
    
    # 컨텍스트 생성 - 모델 선택 우선순위:
    # 1. 함수 인자로 전달된 model
    # 2. 환경 변수 MODEL (.env 파일)
    # 3. 기본값 (anthropic/claude-3-5-sonnet-20241022)
    if model:
        context = Context(model=model)
    else:
        # 환경 변수에서 읽거나 기본값 사용
        context = Context()
    
    print(f"사용 모델: {context.model}")
    print(f"사용자 메시지: {user_message}\n")
    
    # 예시 모델들:
    # - "openai/gpt-4-turbo"
    # - "anthropic/claude-3-5-sonnet-20241022"
    # - "google/gemini-2.0-flash-exp:free"
    # - "qwen/qwen3-30b-a3b"
    # 전체 목록: https://openrouter.ai/models
    
    # 그래프 실행 (configurable context 전달)
    result = await graph.ainvoke(
        initial_state,
        config={"configurable": {"context": context}}
    )
    
    # 응답 출력
    print("\n=== 에이전트 응답 ===")
    for message in result["messages"]:
        if hasattr(message, "content") and message.content:
            print(f"\n{message.__class__.__name__}:")
            print(message.content)
        if hasattr(message, "tool_calls") and message.tool_calls:
            print(f"\n도구 호출:")
            for tool_call in message.tool_calls:
                print(f"  - {tool_call.get('name', 'unknown')}: {tool_call.get('args', {})}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LangGraph MCP Agent 실행 예시",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 기본 모델 사용 (환경 변수 또는 기본값)
  python example_usage.py
  
  # 특정 모델 지정
  python example_usage.py --model "openai/gpt-4-turbo"
  
  # 모델과 메시지 모두 지정
  python example_usage.py --model "google/gemini-2.0-flash-exp:free" --message "파리의 날씨는?"
  
  # 메시지만 변경
  python example_usage.py --message "안녕하세요!"
        """
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="사용할 모델명 (예: openai/gpt-4-turbo, google/gemini-2.0-flash-exp:free)"
    )
    parser.add_argument(
        "--message",
        type=str,
        default=None,
        help="에이전트에게 보낼 메시지"
    )
    
    args = parser.parse_args()
    asyncio.run(main(model=args.model, message=args.message))

