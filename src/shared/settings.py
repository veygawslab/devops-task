from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # set per environment by deploy/manifests/overlays (veyga-microservice deployment.env)
    COLOR: str = Field("gray", validation_alias="BACKGROUND_COLOR")
    # the image's build (the PR head's short sha), baked in by app-ci
    VERSION: str = Field("dev", validation_alias="APP_VERSION")
    # set per Kargo stage by the veyga-microservice chart (dev, prod)
    ENVIRONMENT: str = "local"


settings = Settings()
