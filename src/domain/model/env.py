from pydantic import Field
from pydantic_settings import BaseSettings


class GithubEnv(BaseSettings):
    """Read Github releated secret from environment variables"""

    access_token: str = Field(alias="GITHUB_ACCESS_TOKEN")
