# from litellm.proxy._types import UserAPIKeyAuth
# from fastapi import Request
# from litellm.proxy.exceptions import ProxyException
# from litellm.proxy.auth.litellm_api_key_auth import litellm_api_key_auth

# async def user_api_key_auth(request: Request, api_key: str) -> UserAPIKeyAuth: 
#     try: 
#         #Checks custom auth first
#         modified_master_key = "my-custom-key-xun"
#         if api_key.startswith("my-custom-key"):
#             return UserAPIKeyAuth(api_key=api_key)
#         #If custom auth fails, checks litellm api key auth
#         else:
#             return await litellm_api_key_auth(request, api_key)
#         #If both fail, returns 401
#     except: 
#         raise ProxyException(
#         message="Unauthorized: Invalid API key",
#         type="invalid_request_error",
#         param="api_key",
#         code=401,
#     )

from fastapi import Request
from typing import Union
from litellm.proxy._types import UserAPIKeyAuth
from litellm.proxy.exceptions import ProxyException
from litellm.proxy.auth.litellm_api_key_auth import litellm_api_key_auth

# (tuỳ chọn) strict list cho custom keys
CUSTOM_KEYS = {
    "my-custom-key-xun": {"user_id": "xun", "team_id": "team-001"},
    "my-custom-key-abc": {"user_id": "abc", "team_id": "team-002"},
}

async def user_api_key_auth(request: Request, api_key: str) -> Union[UserAPIKeyAuth, str]:
    """
    Flow:
      1) Check custom key
      2) Nếu fail -> fallback sang LiteLLM API key auth
      3) Nếu cả hai fail -> 401
    """
    # ---- 1) Custom auth ----
    # Nếu muốn strict: dùng dict lookup thay vì startswith
    record = CUSTOM_KEYS.get(api_key)
    if record:
        # Trả về tối thiểu api_key; có thể bổ sung user_id, team_id, quota...
        return UserAPIKeyAuth(
            api_key=api_key,
            user_id=record["user_id"],
            team_id=record["team_id"],
            # quota_limit=..., quota_used=...
        )

    # ---- 2) Fallback: LiteLLM built-in api key auth ----
    try:
        return await litellm_api_key_auth(request, api_key)
    except ProxyException as e:
        # Giữ nguyên lỗi có ý nghĩa từ built-in auth (ví dụ 403, 429)
        raise e
    except Exception:
        # ---- 3) Cả hai fail -> 401 chuẩn ----
        raise ProxyException(
            message="Unauthorized: Invalid API key",
            type="invalid_request_error",
            param="api_key",
            code=401,
        )
