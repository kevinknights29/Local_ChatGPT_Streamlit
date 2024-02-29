from __future__ import annotations

import openai
import streamlit as st
import tiktoken

from src.config import config
from src.streamlit import widgets

# Set Page Configuration
st.set_page_config(
    page_title=config()["app"]["page_title"],
    page_icon=config()["app"]["page_icon"],
)
st.title(config()["app"]["title"])

# OpenAI API Key Validation
widgets.openai_key_validation()

# Onboard User
st.markdown("\n\n".join(config()["app"]["onboarding"]))

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = config()["llm"]["default_model"]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(config()["app"]["chat_instruction"]):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    encoding = tiktoken.get_encoding(config()["embeddings"]["encoding_model"])
    input_tokens = len(encoding.encode(prompt))
    input_price = input_tokens * config()["llm"]["input_price"]
    output_tokens = len(encoding.encode(full_response))
    output_price = output_tokens * config()["llm"]["output_price"]

    st.text_area(
        "Total Price: ",
        value=f"{(input_price + output_price):.2f} USD || {input_price} input cost || {output_price} output cost",
    )
