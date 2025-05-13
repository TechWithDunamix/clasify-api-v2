from nexios.http import Request
from nexios.auth.exceptions import AuthenticationFailed

async def get_user_session(request: Request) -> dict[str, str]:
    if request.user is None:
        raise AuthenticationFailed
    return request.user.session