from fastapi import HTTPException, Request
from typing import Union
from litellm.proxy._types import UserAPIKeyAuth, ProxyException


async def user_api_key_auth_auto_mode(request: Request, api_key: str) -> Union[UserAPIKeyAuth, str]:
    """
    Flow:
      1) Check custom key
      2) Nếu fail -> fallback sang LiteLLM API key auth
      3) Nếu cả hai fail -> 401
    """
    try:
        # ---- 1) Check custom key auth----
        custom_key = "my-custom-key-xun"
        if api_key == custom_key:
            return UserAPIKeyAuth(api_key=api_key)
        
        # ---- 2) If check custom key fail => raise exception to fallback: LiteLLM built-in api key auth ----
        raise ProxyException(
            message="Invalid custom key, fallback to litellm",
            type="invalid_request_error",
            param="api_key",
            code=401,
        )
    except Exception:
        # 3. Nếu cả 2 fail -> trả về 401
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid API key",
        )


async def user_api_key_auth_on_mode(request: Request, api_key: str) -> UserAPIKeyAuth: 
    """
    Change in config.yaml:
        custom_auth: custom_auth.user_api_key_auth
    """
    try: 
        modified_master_key = "sk-my-master-key"
        if api_key == modified_master_key:
            return UserAPIKeyAuth(api_key=api_key)
        raise Exception
    except:
        raise Exception
