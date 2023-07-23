# streamlit-utils
General utilities to make streamlit app creation easier in an object-oriented
manner. This package started with the idea for the `session_state` decorator to
simplify the interaction with the `st.session_state` object. It has since grown
to include other utilities as well.

- [streamlit-utils](#streamlit-utils)
  - [General utilities](#general-utilities)
    - [The `session_state` decorator](#the-session_state-decorator)
  - [Contributing](#contributing)

## General utilities

This section describes the general utilities provided by this package in a
non-exhaustive manner. For more information, please refer to the docstrings of
the individual functions and classes.

### The `session_state` decorator

Traditionally, storing state in a Streamlit app is done by saving a value to a
key in the `st.session_state` object. This object is a `SessionState` instance
that is created only on the first run of the app and will be persisted between
reruns of the app. As the apps are procedural, this means that we have to check
for the existence of the key before we can use it.

A typical usage of the `st.session_state` object looks like this:

```python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
```

However, this approach creates two major inconveniences:
- The code gets cluttered with `if` statements to check for key existences.
- We lose the ability to use type hints with our stateful variables.

And we can also observe that the code gets less 'pythonic', with lots of if
statements in a 'look-before-you-leap' fashion. This is where the
`session_state` decorator comes in. The code above can be rewritten as:

```python
import streamlit as st

from streamlit_utils.state import session_state

@session_state
class MyState:
    counter: int = 0

if st.button("increment"):
    MyState.counter += 1

st.write(f"Counter: {MyState.counter}")
```

What the above code does is to create a `MyState` instance that is stored in
the `st.session_state` object. The `MyState` instance is created only on the
first run of the app and will be retrieved from the `st.session_state` object
on subsequent runs. This means that we can use the `MyState` instance as if it
was a normal **singleton**, without having to worry about the key existence.

The example uses only one state variable, but the `MyState` class can have as
many state variables as needed. The state variables can also be of any type
that is supported by the `st.session_state` object.

Another possible usage, when using a `session_state` decorated singleton to
store state for Streamlit buttons and fields is:

```python
@session_state
class MyState:
    counter: int = 0
    query: str = ""

st.text_input("What would you like to ask?", key="MyState.query")
```

Note that the `key` argument to store and persist the `text_input` value is
specified with the name of the singleton class and the key on a string. This
feature is provided by the `session_state` decorator and allow seamless usage
with any Streamlit widget that accepts a `key` argument.

## Contributing

Install the package to your local Python virtual environment with one of the
following commands:

```bash
make install

# OR directly with pip
pip install -e .[dev]
```

Before contributing, please always check your code health by running:

* Code formatter, linter and type-checker:

```bash
# The install command can be suppressed if the package was installed using the
# `make install` convenience command.
pre-commit install
pre-commit run --all-files
```

* Tests:

```bash
# Can be run with `make test` as well.
pytest --cov
```