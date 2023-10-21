from __future__ import annotations

import streamlit as st

from src.openai import check_openai_api_key


def openai_key_validation() -> None:
    """
    Validates and sets the OpenAI API Key.

    This function checks if the OpenAI API Key is valid and sets it in the session state.
    It prompts the user to enter the API Key if it is not already provided in the secrets.

    Returns:
        None
    """
    openai_api_key = ""
    if "api_key_is_valid" not in st.session_state:
        if "openai" in st.secrets:
            if "api_key" in st.secrets.openai:
                st.session_state["api_key_is_valid"] = check_openai_api_key(
                    st.secrets.openai.api_key,
                )
            else:
                st.warning(
                    "The OpenAI API Key provisioned is invalid... Check secrets!",
                )
                st.session_state["api_key_is_valid"] = False
        else:
            st.warning("The OpenAI API Key provisioned is invalid... Check secrets!")
            st.session_state["api_key_is_valid"] = False
    if not st.session_state["api_key_is_valid"]:
        openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
        if not openai_api_key:
            st.info("Enter an OpenAI API Key to continue")
            st.stop()
        st.session_state["api_key_is_valid"] = check_openai_api_key(openai_api_key)
    if not st.session_state["api_key_is_valid"]:
        st.warning("The OpenAI API Key provisioned is invalid!")
        st.stop()
    st.success("The OpenAI API Key provisioned is valid!")
    st.session_state["api_key_is_valid"] = True
