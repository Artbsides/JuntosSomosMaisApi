from functools import lru_cache
from prettyconf import config


class BaseConfig:
    APP_DEBUG = config("DEBUG",
        default=False, cast=config.boolean
    )

    APP_ENVIRONMENT = config("APP_ENVIRONMENT",
        default="test", cast=str
    )

    APP_HOST = config("APP_HOST",
        default="127.0.0.1", cast=str
    )

    APP_HOST_PORT = config("APP_HOST_PORT",
        default=8000, cast=int
    )

    APP_PREFIX = config("APP_PREFIX",
        default="", cast=str
    )

    JSM_DATA_URL = config("JSM_DATA_URL",
        default="", cast=str
    )

    IBGE_DATA_URL = config("IBGE_DATA_URL",
        default="", cast=str
    )

    JWT_SECRET = config("JWT_SECRET",
        default="", cast=str
    )

    JWT_ALGORITHM = config("JWT_ALGORITHM",
        default="HS256", cast=str
    )


class ProductionConfig(BaseConfig):
  ...


class DevelopmentConfig(BaseConfig):
  ...


class TestsConfig(BaseConfig):
  ...


@lru_cache
def get_environment_settings() -> BaseConfig:
    config_cls_dict = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "tests": TestsConfig,
    }

    return config_cls_dict[
        BaseConfig.APP_ENVIRONMENT
    ]()


settings = get_environment_settings()
