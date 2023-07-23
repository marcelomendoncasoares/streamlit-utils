"""
Utilities for manipulating the CSS style of Streamlit buttons.

"""

from typing import Dict, Optional, Union

from streamlit import markdown
from streamlit.components.v1 import html


def button_style_changer(
    *buttons: Union[str, int],
    style_css: Dict[str, str],
    hover_css: Optional[Dict[str, str]] = None,
    click_css: Optional[Dict[str, str]] = None,
) -> None:
    """
    Change the CSS style of a sequence of buttons in Streamlit. This function should
    be called after the buttons are created. If no buttons are passed, the dictionaries
    should contain `CSS` keys and values that will be applied to all buttons. Otherwise,
    the keys and values should be valid `Javascript HTML DOM Style Object` properties.

    For a reference of the available `Javascript` properties, see:
    https://www.w3schools.com/jsref/dom_obj_style.asp

    Parameters
    ----------
    *buttons : int | str
        Label or index of the buttons to change the style. If a label is passed,
        all buttons with the same label will be changed. If an index is passed,
        the button with that index *on Javascript* will be changed. Int lookup is
        faster because will not need to search for the button in the DOM.
    style_css : Dict[str, str]
        A dictionary with the style to apply to the buttons. All keys will be applied
        to the `.style` property of each button element, or to the `<style>` tag if
        no buttons are passed.
    hover_css : Dict[str, str], optional
        A dictionary with the style to apply to the buttons when the mouse is hovering
        over them. Follows the same rules as `style_css`.
    click_css : Dict[str, str], optional
        A dictionary with the style to apply to the buttons when they are clicked.
        Follows the same rules as `style_css`. Note that the style does not revert to
        the previous style when the button is clicked again.
    """

    if not buttons:
        raise ValueError("At least one button must be passed")

        markdown(
            """
                <style>
                div.stButton > button:first-child {
                    color: white;
                    // height: 2em;
                    // width: 15em;
                    // border-radius:6px;
                    // border:0px solid #000000;
                    // font-size:20px;
                    // font-weight: bold;
                    // text-align: left;
                    // margin: auto;
                    // margin-top:-10px;
                    // display: block;
                }
                div.stButton > button:first-child:hover {
                    color: white;
                }
                div.stButton > button:first-child:active {
                    color: white;
                }
                </style>
            """,
            unsafe_allow_html=True,
        )
        return

    base_style_css_apply = "\n".join(
        [f"elements[i].style.{key} = {value!r};" for key, value in style_css.items()]
    )

    style_css_apply = base_style_css_apply
    style_css_apply += f"""\n
        elements[i].onmouseleave = function() {{
            {style_css_apply.replace('elements[i]', 'this')}
        }}
    """

    if hover_css:
        style_css_apply += f"""\n
            elements[i].onmouseover = function() {{
                {"".join([
                    f"this.style.{key} = {value!r};"
                    for key, value in hover_css.items()
                ])}
            }}
        """

    if click_css:
        # first_key = list(click_css.keys())[0]
        # first_value = list(click_css.values())[0]
        # style_css_apply += f"""\n
        #     elements[i].onclick = function() {{
        #         if (this.style.{first_key} == {first_value!r}) {{
        #             {base_style_css_apply.replace('elements[i]', 'this')}
        #         }}
        #         else {{
        #             {"".join([
        #                 f"this.style.{key} = {value!r};"
        #                 for key, value in click_css.items()
        #             ])}
        #         }}
        #     }}
        # """
        style_css_apply += f"""\n
            elements[i].onclick = function() {{
                {"".join([
                    f"this.style.{key} = {value!r};"
                    for key, value in click_css.items()
                ])}
            }}
        """

    if isinstance(buttons[0], str):
        for button in buttons:
            html(
                f"""
                <script>
                    var elements = window.parent.document.querySelectorAll('button');
                    for (var i = 0; i < elements.length; ++i) {{
                        if (elements[i].innerText == "{button}") {{
                            {style_css_apply}
                            break;
                        }}
                    }}
                </script>
            """
            )

    else:
        html(
            f"""
            <script>
                var elements = window.parent.document.querySelectorAll('button');
                const buttons = {list(buttons)};
                for (var i = 0; i < buttons.length; ++i) {{
                    {style_css_apply.replace('[i]', f'[buttons[i]]')}
                }}
            </script>
        """
        )
