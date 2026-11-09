import pytest
from fastapi import HTTPException

from server import app as server_app


def test_session_rejects_role_mismatch(world):
    with pytest.raises(HTTPException) as error:
        server_app.create_session(
            server_app.SessionCreate(user_id=9002, role="shopper")
        )

    assert error.value.status_code == 403


def test_token_cannot_authorize_another_session(world):
    server_app._SESSIONS.clear()
    first = server_app.create_session(
        server_app.SessionCreate(user_id=9002, role="merchant")
    )
    second = server_app.create_session(
        server_app.SessionCreate(user_id=9002, role="merchant")
    )

    with pytest.raises(HTTPException) as error:
        server_app._authorize(
            second["session_id"],
            f"Bearer {first['token']}",
        )

    assert error.value.status_code == 403
