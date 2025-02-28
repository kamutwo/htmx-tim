from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2CookiePasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        authorization = request.cookies.get("authorization")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(401, detail="Not authenticated")
            else:
                return None

        return param
