"""환경설정 값을 불러옵니다."""

import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_ROOT = Path(__file__).resolve().parents[2]

# 로컬 직접 실행에서는 backend/.env를 사용합니다. Docker Compose에서는
# env_file로 같은 설정을 주입하므로 파일이 없어도 환경변수를 읽을 수 있습니다.
load_dotenv(BACKEND_ROOT / ".env")

APP_ENV = os.getenv("APP_ENV", "development")
APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Asia/Seoul")
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"

POSTGRES_DSN = os.getenv("POSTGRES_DSN", "")
REDIS_URL = os.getenv("REDIS_URL", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
STT_MODEL = os.getenv("STT_MODEL", "gpt-4o-mini-transcribe")

BABY_CARE_MCP_URL = os.getenv(
    "BABY_CARE_MCP_URL",
    "http://localhost:8101/mcp",
)
BABY_INFO_MCP_URL = os.getenv(
    "BABY_INFO_MCP_URL",
    "http://localhost:8102/mcp",
)

MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "20"))
