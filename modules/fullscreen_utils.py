# ==================================================
# FULLSCREEN UTILITIES
# ==================================================
# Detects and controls browser Fullscreen Mode for
# the AI Interview System.
#
# Install required packages:
#   pip install streamlit-javascript
# ==================================================

import warnings
import streamlit as st

try:
    from streamlit_javascript import st_javascript
except ImportError:
    st_javascript = None
    warnings.warn(
        "streamlit_javascript is not installed. Fullscreen status detection will be disabled.",
        UserWarning,
    )


# ==================================================
# CHECK CURRENT FULLSCREEN STATUS
# ==================================================
def check_fullscreen_status(key="fullscreen_check"):
    """
    Returns True if the main browser window (the parent
    Streamlit document, not this component's iframe) is
    currently in Fullscreen Mode, otherwise False.

    `key` must be unique per call-site if this function is
    called more than once during the same script run.
    """

    js_code = """
    !!(window.parent.document.fullscreenElement ||
       window.parent.document.webkitFullscreenElement ||
       window.parent.document.mozFullScreenElement ||
       window.parent.document.msFullscreenElement)
    """

    if st_javascript is None:
        return False

    try:
        result = st_javascript(js_code, key=key)
    except Exception:
        result = None

    # st_javascript returns None on the very first render
    # while the frontend component is still initializing.
    if result is None:
        return False

    return bool(result)


# ==================================================
# ENTER FULLSCREEN BUTTON
# ==================================================
def render_enter_fullscreen_button(label="🖥 Enter Fullscreen Mode"):
    """
    Renders an HTML/JS button. On click, it requests
    Fullscreen Mode on the top level Streamlit document.

    NOTE: Some browsers restrict requestFullscreen() calls
    made from inside an embedded iframe (which is how this
    button is rendered). If clicking the button does
    nothing in your browser, ask the candidate to press
    F11 instead — fullscreen *detection* will still work
    correctly either way.
    """

    html_code = f"""
    <script>
    function requestAppFullscreen() {{
        const doc = window.parent.document;
        const el = doc.documentElement;

        if (el.requestFullscreen) {{
            el.requestFullscreen();
        }} else if (el.webkitRequestFullscreen) {{
            el.webkitRequestFullscreen();
        }} else if (el.mozRequestFullScreen) {{
            el.mozRequestFullScreen();
        }} else if (el.msRequestFullscreen) {{
            el.msRequestFullscreen();
        }}
    }}
    </script>

    <button onclick="requestAppFullscreen()" style="
        width:100%;
        padding:12px 20px;
        font-size:16px;
        font-weight:600;
        color:white;
        background:linear-gradient(90deg, #06b6d4, #2563eb);
        border:none;
        border-radius:12px;
        cursor:pointer;
    ">
        {label}
    </button>
    """

    st.components.v1.html(html_code, height=65)


# ==================================================
# EXIT FULLSCREEN BUTTON
# ==================================================
def render_exit_fullscreen_button(label="🔙 Exit Fullscreen Mode"):
    """
    Renders an HTML/JS button. On click, it exits
    Fullscreen Mode on the top level Streamlit document.
    """

    html_code = f"""
    <script>
    function exitAppFullscreen() {{
        const doc = window.parent.document;

        if (doc.exitFullscreen) {{
            doc.exitFullscreen();
        }} else if (doc.webkitExitFullscreen) {{
            doc.webkitExitFullscreen();
        }} else if (doc.mozCancelFullScreen) {{
            doc.mozCancelFullScreen();
        }} else if (doc.msExitFullscreen) {{
            doc.msExitFullscreen();
        }}
    }}
    </script>

    <button onclick="exitAppFullscreen()" style="
        width:100%;
        padding:10px 18px;
        font-size:15px;
        font-weight:600;
        color:white;
        background:#334155;
        border:none;
        border-radius:12px;
        cursor:pointer;
    ">
        {label}
    </button>
    """

    st.components.v1.html(html_code, height=60)