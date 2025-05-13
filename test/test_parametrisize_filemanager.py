"""Tests for filemanager operations using parameterized inputs."""

import pytest
from models.user import User


@pytest.mark.parametrize(
    "user_id, username, surname",
    [(10, "Charlie", "Brown"), (20, "Diana", "Prince"), (30, "Eve", "Black")],
)
def test_user_to_dict(user_id, username, surname):
    """
    Parametrized test for checking correct dict serialization of User objects.
    """
    user = User(user_id=user_id, username=username, surname=surname)
    data = user.to_dict()

    assert data["user_id"] == user_id
    assert data["username"] == username
    assert data["surname"] == surname
    assert isinstance(data["accounts"], list)
