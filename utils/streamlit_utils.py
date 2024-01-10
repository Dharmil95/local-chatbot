import streamlit as st
from utils.chat_utils import OpenAIBot
from utils.history_management import HistoryManagement
from datetime import datetime
import ast
import pandas as pd
from PIL import Image

BOT = "bot"
HUMAN = "human"

from utils.logger import setup_logger

logger = setup_logger()

modelname = None


def init(model_name):
    global modelname
    modelname = model_name
    st.sidebar.write("Use the widgets to reset history:")
    with open("./static/styles.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    title = st.container()
    with title:
        st.markdown("<style>h1 {text-align: center;}</style>", unsafe_allow_html=True)
        st.title("Local Chat Bot 🤖")

    if "history" not in st.session_state:
        st.session_state.history = HistoryManagement()
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = OpenAIBot(modelname)


def reset():
    global modelname
    logger.debug("modelname:{}".format(modelname))
    st.session_state.history = HistoryManagement()
    st.session_state.index_plot = False


class Message:
    def __init__(self, user, message, dtype):
        self.user = user
        self.message = message
        self.dtype = dtype

    def get_user(self):
        return self.user

    def get_message(self):
        return self.message

    def get_dtype(self):
        return self.dtype


def general_query_event(chat):
    global modelname
    message_list = []
    message_list.append(Message(HUMAN, chat, str))
    if modelname == "openai":
        messages = [
            {
                "role": "user",
                "content": "You are stock market screener and index generation bot. If you don't know the answer please say I don't know. Question:"
                + chat,
            }
        ]
        answer = st.session_state.chatbot.query(messages)
    elif modelname == "mistral":
        answer = "I dont know the answer. How can I help you with generating index?"
        text = (
            "<s>[INST] What is your favourite condiment? [/INST]\
                Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!</s>\
                [INST] "
            + chat
            + " [/INST]"
        )
        answer = st.session_state.chatbot.query(text)
    logger.debug("Reply of General Query:".format(answer))
    message_list.append(Message(BOT, answer, str))
    return message_list


def display(chat):
    messgae = chat.get_message()
    user = chat.get_user()
    dtype = chat.get_dtype()
    if isinstance(messgae, Image.Image):
        st.image(
            messgae,
            width=None,
            use_column_width=True,
            clamp=False,
            channels="RGB",
            output_format="auto",
        )
    elif isinstance(messgae, str):
        if user == HUMAN:
            bubble = "human-bubble"
            row_reverse = "row-reverse"
            div = f"""
                <div class="chat-row {row_reverse}">
                <div class="chat-bubble {bubble}">{messgae}</div></div>"""
            st.markdown(div, unsafe_allow_html=True)
        else:
            bubble = "human-bubble"
            row_reverse = "row-reverse"
            div = f"""
                <div class="chat-row">
                <div class="chat-bubble {bubble}">{messgae}</div></div>"""
            st.markdown(div, unsafe_allow_html=True)
    else:
        # st.write(":blue[Agent:] ")
        st.write(messgae)
