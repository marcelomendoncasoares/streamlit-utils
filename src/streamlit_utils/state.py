"""
Streamlit State Utils

Contains utilities to simplify initialization and interaction with Streamlit's
`session_state` object.

"""

import streamlit as st

from inspect import ismethod
from typing import Any, Dict, Callable, Optional, Tuple, Type, TypeVar, overload


_T_class = TypeVar("_T_class", bound=Type[Any])


class StreamlitStateMetaClass(type):
    """
    Metaclass to create singleton dataclass-like classes that use Streamlit's
    `session_state` as back-end. The class must be used with annotations and all
    annotated attributes must have initial value. Also, all methods must be class
    methods or static methods.

    Keys in `st.session_state` that are formatted like `cls.__name__.<attr>` will
    also be recovered as attributes of the class upon access. This allows the user
    to reference the attributes on widgets as keys, but recovering them from the
    singleton instead of from the `session_state` object.
    """

    def __new__(cls, cls_name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):
        if cls_name in st.session_state:
            return st.session_state[cls_name]

        initialized = super().__new__(cls, cls_name, bases, attrs)
        initialized.__validate_subclass()
        setattr(st.session_state, cls_name, initialized)
        return initialized

    def __validate_subclass(cls) -> None:
        """
        Validate that the class uses annotations and all annotated attributes have
        initial value. Also, validate that all methods are class methods or static
        methods. If any of the validations fail, a `TypeError` will be raised.
        """

        if "__annotations__" not in cls.__dict__:
            raise TypeError(
                f"Class {cls.__name__!r} must be used with annotations. All "
                f"attributes must be annotated with their type and have initial value."
            )

        not_init_attrs = tuple(set(cls.__annotations__) - set(cls.__dict__))
        if not_init_attrs:
            raise TypeError(
                f"All annotated attributes of class {cls.__name__!r} must have "
                f"initial value. Not initialized attributes: {not_init_attrs!r}."
            )

        not_annotated: Tuple[str, ...] = ()
        not_class_methods: Tuple[str, ...] = ()

        for attr_name, attr_value in cls.__dict__.items():
            if attr_name.startswith("__"):
                continue
            if ismethod(attr_value):
                attr_value = cls.__dict__[attr_name]
                if not isinstance(attr_value, (staticmethod, classmethod)):
                    not_class_methods += (attr_name,)
            elif attr_name not in cls.__annotations__:
                not_annotated += (attr_name,)

        if not_annotated:
            raise TypeError(
                f"Class {cls.__name__!r} admits only annotated attributes. The "
                f"following attributes are missing type annotation: {not_annotated!r}."
            )

        if not_class_methods:
            raise TypeError(
                f"Class {cls.__name__!r} must have all methods as class methods "
                f"or static methods. Invalid methods: {not_class_methods!r}."
            )

    @property
    def _attrs(cls) -> Dict[str, Any]:
        """
        Return a dictionary with all annotated attributes of the class.
        """
        return {attr: cls.__dict__[attr] for attr in cls.__annotations__}

    def __getattribute__(cls, __name: str) -> Any:
        """
        Recover the keys formatted like `cls.__name__.<attr>` from `st.session_state`.
        """
        if __name.startswith("__"):
            return super().__getattribute__(__name)
        if (possible_bind_key := f"{cls.__name__}.{__name}") in st.session_state:
            setattr(cls, __name, st.session_state[possible_bind_key])
        return super().__getattribute__(__name)

    def __repr__(cls) -> str:
        short_repr = ", ".join(f"{k}={v!r}" for k, v in cls._attrs.items())
        if len(one_line_repr := f"{cls.__name__}({short_repr})") < 50:
            return one_line_repr
        long_repr = "\n".join(f"    {k}={v!r}," for k, v in cls._attrs.items())
        return f"{cls.__name__}(\n{long_repr}\n)"


@overload
def session_state(__cls: None = None) -> Callable[[_T_class], _T_class]:
    ...


@overload
def session_state(__cls: _T_class) -> _T_class:
    ...


def session_state(__cls: Optional[_T_class] = None):
    """
    Transform the class in a singleton dataclass-like classes that use Streamlit's
    `session_state` as back-end. The class must be used with annotations and all
    annotated attributes must have initial value. Also, all methods must be class
    methods or static methods.

    Keys in `st.session_state` that are formatted like `cls.__name__.<attr>` will
    also be recovered as attributes of the class upon access. This allows the user
    to reference the attributes on widgets as keys, but recovering them from the
    singleton instead of from the `session_state` object.
    """
    if __cls is None:
        return session_state
    return StreamlitStateMetaClass(
        __cls.__name__,
        __cls.__bases__,
        dict(__cls.__dict__),
    )
