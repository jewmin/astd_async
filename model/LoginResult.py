from model.enum.LoginStatus import LoginStatus, LoginStatusString


class LoginResult:
    """登录结果"""
    def __init__(self):
        self.status: LoginStatus = None
        self.game_url: str = None
        self.session_id: str = None
        self.cookies: dict = None

    def __repr__(self) -> str:
        return LoginStatusString.ToString(self.status)
