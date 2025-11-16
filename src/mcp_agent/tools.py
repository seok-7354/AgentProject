"""MCP 통합 도구 모듈

이 모듈은 Model Context Protocol(MCP)을 통한 도구 통합을 제공합니다.
"""

import json
from typing import Any, Callable, List, Optional

import aiofiles
import aiofiles.os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.runtime import get_runtime

from mcp_agent.context import Context



async def load_mcp_config(config_path: str) -> dict:
    """MCP 설정 파일을 비동기로 로드합니다."""
    try:
        async with aiofiles.open(config_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
    except Exception as e:
        print(f"⚠️ MCP 설정 로드 실패: {e}")
        return {}


async def get_mcp_tools(mcp_config: dict) -> List[Any]:
    """MCP 클라이언트를 초기화하고 도구를 가져옵니다."""
    if not mcp_config:
        return []
        
    try:
        client = MultiServerMCPClient(mcp_config)
        tools = await client.get_tools()
        print(f"✅ MCP 도구 {len(tools)}개 로드됨")
        return tools
    except Exception as e:
        print(f"❌ MCP 도구 로드 실패: {e}")
        return []


async def get_all_tools(runtime_context: Context = None) -> List[Callable[..., Any]]:
    """MCP 도구를 가져옵니다.
    
    Args:
        runtime_context: Context 객체 (None이면 get_runtime()으로 가져옴)
    """
    try:
        # Context 가져오기
        if runtime_context is None:
            runtime = get_runtime(Context)
            if runtime is None or runtime.context is None:
                # get_runtime()이 None을 반환하는 경우 기본값 사용
                runtime_context = Context()
            else:
                runtime_context = runtime.context
        
        config_path = runtime_context.mcp_config_path
        
        # MCP 설정 파일 존재 확인 및 로드
        if await aiofiles.os.path.exists(config_path):
            mcp_config = await load_mcp_config(config_path)
            tools = await get_mcp_tools(mcp_config)
            return tools
        else:
            print(f"⚠️ MCP 설정 파일 없음: {config_path}")
            return []
            
    except Exception as e:
        print(f"❌ 도구 로딩 실패: {e}")
        return []




# 기본 도구 (비어있음 - MCP 도구만 사용)
TOOLS: List[Callable[..., Any]] = []