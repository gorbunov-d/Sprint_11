from dataclasses import dataclass


@dataclass(frozen=True)
class RegisteredUser:
    credentials: dict
    user_id: int
    token: str
