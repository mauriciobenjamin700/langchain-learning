from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class for managing application configuration.

    Attributes:
        LANGSMITH_TRACING (bool): Enable or disable LangSmith tracing.
        LANGSMITH_API_KEY (str): API key for LangSmith.
        LANGSMITH_PROJECT (str): Name of the LangSmith project.
        GOOGLE_API_KEY (str): API key for Google services.  
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    # LangSmith settings
    LANGSMITH_TRACING: str = "true"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str = "YOUR_API_KEY_HERE"
    LANGSMITH_PROJECT: str = "YOUR_PROJECT_NAME_HERE"

    GOOGLE_API_KEY: str = "YOUR_GOOGLE_API_KEY_HERE"


settings = Settings()