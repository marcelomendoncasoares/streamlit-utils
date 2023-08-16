"""
Test the streamlit session state dataclass-like singleton decorator.

"""

import streamlit as st

from unittest.mock import patch
from typing import Any

from streamlit_utils.state import session_state


class _SessionStateMock:
    """Mock class to replace `st.session_state` accepting setattr calls."""

    def __init__(self) -> None:
        self.__dict__ = {}

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __getattr__(self, name: str) -> Any:
        return self.__dict__[name]

    def __getitem__(self, name: str) -> Any:
        return self.__dict__[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __iter__(self) -> Any:
        return iter(self.__dict__)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, dict):
            return all(self[key] == value for key, value in __value.items())
        return super().__eq__(__value)


@patch.object(st, "session_state", _SessionStateMock())
def test_session_state_backend() -> None:
    """
    Test the session state backend is on `st.session_state`.
    """
    assert st.session_state == {}

    @session_state
    class State:
        attr: int = 0

    assert st.session_state == {"State": State}


@patch.object(st, "session_state", _SessionStateMock())
def test_session_state_re_declaration() -> None:
    """
    Test the session state class is not re-declared, but retrieved from the backend.
    """
    assert st.session_state == {}

    @session_state
    class State:
        attr: int = 0

    first_state = State
    assert st.session_state == {"State": State}

    State.attr = 1

    @session_state
    class State:  # type: ignore[no-redef]
        attr: int = 0

    assert State is first_state
    assert State.attr == 1


@patch.object(st, "session_state", _SessionStateMock())
def test_session_state_key_recover() -> None:
    """
    Test that a key in format `State.attr` is recovered from the backend.
    """
    assert st.session_state == {}
    st.session_state["State.attr"] = 1

    @session_state
    class State:
        attr: int = 0

    assert st.session_state == {"State": State, "State.attr": 1}
    assert State.attr == 1
