from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Config:
    OPENROUTER_API_KEY: str = getenv("OPENROUTER_API_KEY", "")

    @property
    def api_key(self) -> str:
        if not self.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not set in environment")
        return self.OPENROUTER_API_KEY


config = Config()
