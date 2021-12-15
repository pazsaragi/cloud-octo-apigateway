import os


def get_env(variable: str, default=None, optional: bool = False) -> str:
    try:
        var = os.getenv(variable)
        if not var:
            if not default:
                if optional:
                    return
                raise RuntimeError(f"Runtime variable {variable} is not set")
            return default
        return var
    except Exception as e:
        raise RuntimeError(f"Runtime variable {variable} is not set. Error reason: {e}")


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = get_env("SECRET_KEY")
ALGORITHM = get_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = get_env("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS")
ENVIRONMENT = get_env("ENVIRONMENT", "development")
LOCALSTACK_HOSTNAME = get_env("LOCALSTACK_HOSTNAME", None, True)
AUTH_TABLE_NAME = get_env("AUTH_TABLE_NAME", "auth-table")
