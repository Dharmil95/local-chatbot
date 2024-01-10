import streamlit as st
from PIL import Image
from utils.streamlit_utils import (
    init,
    display,
    Message,
    reset,
    general_query_event,
)
from utils.logger import setup_logger

logger = setup_logger()

# Parse Arguments Model types
import argparse

parser = argparse.ArgumentParser(description="Stock Screener Application")
parser.add_argument(
    "--model_name", default="mistral", help="Model name. openai or mistral"
)
args = parser.parse_args()
init_flag = True
if init_flag:
    init(args.model_name)
    init_flag = False


def on_chat_event():
    message_list = None
    chat = st.session_state.human_prompt
    message_list = general_query_event(chat)
    if message_list:
        st.session_state.history.add(message_list)


chat_placeholder = st.container()
prompt_placeholder = st.chat_input(on_submit=on_chat_event, key="human_prompt")

st.sidebar.button("Reset", on_click=reset, use_container_width=True)

with chat_placeholder:
    for chat in st.session_state.history.get():
        display(chat)
