"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated

from . import prompts


@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20241022",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name. Available via OpenRouter."
        },
    )

    mcp_config_path: str = field(
        default="mcp_config.json",
        metadata={
            "description": "Path to the MCP configuration file."
        },
    )

    max_tokens: int = field(
        default=2048,
        metadata={
            "description": "Maximum number of tokens to generate in the response."
        },
    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args.
        
        환경 변수 우선순위:
        1. 명시적으로 전달된 인수 (최우선)
        2. 환경 변수 (대문자 필드명)
        3. 기본값
        """
        for f in fields(self):
            if not f.init:
                continue

            # 필드가 기본값과 같으면 환경 변수에서 읽기 시도
            current_value = getattr(self, f.name)
            if current_value == f.default:
                env_value = os.environ.get(f.name.upper())
                if env_value is not None:
                    # 타입 변환 (int 필드의 경우)
                    if f.type == int:
                        try:
                            setattr(self, f.name, int(env_value))
                        except ValueError:
                            print(f"⚠️ 환경 변수 {f.name.upper()}의 값 '{env_value}'를 int로 변환할 수 없습니다. 기본값 사용.")
                    else:
                        setattr(self, f.name, env_value)
