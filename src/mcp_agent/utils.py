"""유틸리티 및 헬퍼 함수들."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

# .env 파일 로드
load_dotenv()


def load_chat_model(model_name: str, max_tokens: int = 2048) -> BaseChatModel:
    """완전히 지정된 이름에서 채팅 모델을 로드합니다.

    Args:
        model_name (str): 'provider/model' 형식의 문자열
        max_tokens (int): 최대 생성 토큰 수 (기본값: 2048)
    """
    # OpenRouter API를 사용하여 ChatOpenAI 모델 초기화
    # 온도는 0.1로 설정하여 일관성 있는 응답 생성
    # max_tokens를 설정하여 크레딧 부족 오류 방지
    model = ChatOpenAI(
        temperature=0.1,
        model_name=model_name,
        max_tokens=max_tokens,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    )
    return model
