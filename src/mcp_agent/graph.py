from datetime import UTC, datetime
from typing import Dict, List

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.runtime import Runtime

from mcp_agent.context import Context
from mcp_agent.state import InputState, State
from mcp_agent.tools import get_all_tools
from mcp_agent.utils import load_chat_model


async def agent_node(
    state: State, runtime: Runtime[Context]
) -> Dict[str, List[BaseMessage]]:
    """MCP 도구를 동적으로 로드하여 ReAct 에이전트를 실행합니다."""
    try:
        # MCP 도구 가져오기
        tools = await get_all_tools()

        # 모델 초기화
        model = load_chat_model(runtime.context.model)

        # 시스템 프롬프트 포맷팅
        system_prompt = runtime.context.system_prompt.format(
            system_time=datetime.now(tz=UTC).isoformat()
        )

        # ReAct 에이전트 생성
        agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=system_prompt,
        )

        # 에이전트 실행
        response = await agent.ainvoke(state)
        return response

    except Exception as e:
        print(f"❌ 에이전트 실행 실패: {e}")
        return {
            "messages": [
                AIMessage(
                    content="죄송합니다. 시스템에 일시적인 문제가 발생했습니다. 나중에 다시 시도해 주세요."
                )
            ]
        }


# StateGraph 생성 (langgraph.json 호환성을 위해)
builder = StateGraph(State, input_schema=InputState, context_schema=Context)
builder.add_node("agent", agent_node)
builder.add_edge("__start__", "agent")
builder.add_edge("agent", "__end__")

# 실행 가능한 그래프로 컴파일
graph = builder.compile(name="MCP ReAct Agent")
