import streamlit as st

st.set_page_config(page_title="Index Generation", page_icon="imgs/favicon.ico")

import os
from utils.logger import setup_logger

logger = setup_logger()


class OpenAIBot:
    def __init__(self, modelname):
        self.modelname = modelname
        self.llm = None

        if self.modelname == "openai":
            from openai import OpenAI

            os.environ["OPENAI_API_KEY"] = ""
            self.llm = OpenAI()
        elif self.modelname == "mistral":
            logger.info("Mistral Model Selected")
            from langchain.callbacks.manager import CallbackManager
            from langchain.callbacks.streaming_stdout import (
                StreamingStdOutCallbackHandler,
            )
            from langchain.llms import LlamaCpp

            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            n_gpu_layers = 80
            n_batch = 512
            self.llm = LlamaCpp(
                model_path="/home/dharmil/Downloads/mistral-7b-instruct-v0.1.Q8_0.gguf",
                n_gpu_layers=n_gpu_layers,
                n_batch=n_batch,
                callback_manager=callback_manager,
                verbose=False,
                temperature=0,
                n_ctx=650,
            )

    def query(self, message):
        if self.modelname == "openai":
            stream = self.llm.chat.completions.create(
                model="gpt-3.5-turbo-0613", messages=message, stream=False
            )
            return stream.choices[0].message.content
        elif self.modelname == "mistral":
            response = self.llm(message)
            return response

    # def get_intent(self, query):
    #     if self.modelname == "openai":
    #         messages = [
    #             {
    #                 "role": "user",
    #                 "content": "You are stock market screener and index generation bot. I will provide you queries from customer just classify them in four categories.\
    #                     1. 'CreateIndex': Customer asking to generate the index from existing data,\
    #                     2. 'UpdateOrShowData: Customer is asking to show or update the current stock pandas dataframe to filter it before generating index,\
    #                     3. 'Greetings': Customer is greetring you.\
    #                     4. 'GeneralQuery': If the customer is not asking for updating or showing the stock dataframe nor they are asking to create index and nor they are greeting.\
    #                     Answer only the name of intent out of this four 'CreateIndex', 'UpdateOrShowData', 'Greetings' and 'GeneralQuery'. Query: " \
    #                 + query,
    #             }
    #         ]
    #         return self.query(messages)
    #     elif self.modelname == "mistral":
    #         intent_prompt = "Classify the text into CreateIndex, UpdateOrShowData or GeneralQuery. \n \
    #         Text: Can you please create an index?\n \
    #         Answer: CreateIndex\n \
    #         Text: Great! Now please drop CIK column.\n \
    #         Answer: UpdateOrShowData \n \
    #         Text: What is my name? \n \
    #         Answer: GeneralQuery \n \
    #         Text: Hey I want to create an index based on S & P 500 stocks? \n \
    #         Answer: CreateIndex \n \
    #         Text: " + query + "\n \
    #         Answer:"
    #         return self.query(intent_prompt)

    # def get_action(self, query, columns):
    #     if self.modelname == "openai":
    #         message = [
    #             {
    #                 "role": "user",
    #                 "content": "You are Stock Screener expert. I will provide you statement, your role is to find the parameters from the statement and actions. \
    #                     Parameters = ['COMPANY NAME', 'HQ COUNTRY',	'SECTOR', 'TICKER', 'PREVIOUS CLOSE ($)', '1D CHANGE (%)',	'5D CHANGE (%)', 'YTD CHANGE (%)', \
    #                         'MARKET CAP ($)', 'SHARES OUTSTANDING', 'SPY WEIGHT', 'SUB SECTOR', 'CIK', 'FOUNDED'] Actions = ['Add', 'Remove', 'Filter']\
    #                         SECTORS = [['Industrials', 'Health Care', 'Information Technology', 'Utilities', 'Financials', 'Materials', 'Consumer Discretionary', \
    #                         'Real Estate','Communication Services', 'Consumer Staples','Energy']\
    #                         Answer in dictionary\n\n\
    #                         Query:  Can you Add year to date change? Answer: {' Add':[ 'YTD CHANGE(%)'], 'Remove':[], 'Filter': []}\n\
    #                         Query: Can you remove company sector and cik from this? Answer: {'Add': [], 'Remove': ['SECTOR', 'CIK], 'Filter': []}\n\
    #                         Query: Show me the data again. Answer: {'Add': [], 'Remove': [], 'Filter': []}\
    #                         Query: Filter sector with Energy only. Answer: {'Add': [], 'Remove': [], 'Filter': [{'Field': 'SECTOR', 'Value': 'Energy', 'Operation': '=='}]}\
    #                         Query: Can you keep stocks with market cap greater than 4 billion dollars. Answer: {'Add': [], 'Remove': [], 'Filter': [{'Field': 'SECTOR', 'Value': '4000000000', 'Operation': '>'}]}\
    #                         Query: "
    #                 + query
    #                 + " Answer: ",
    #             }
    #         ]
    #         return self.query(message)
    #     elif self.modelname == "mistral":
    #         message = "Your role is to find the parameters from the statement and actions. \
    #             Then return python dictionary with releavant keys(actions) and values(parameters). Please return only one python dictionary. \n \
    #             Parameters = 'COMPANY NAME', 'HQ COUNTRY',	'SECTOR', 'TICKER', 'PREVIOUS CLOSE ($)', '1D CHANGE (%)', '5D CHANGE (%)', 'YTD CHANGE (%)', \
    #             'MARKET CAP ($)', 'SHARES OUTSTANDING', 'SPY WEIGHT', 'SUB SECTOR', 'CIK', 'FOUNDED'. \n \
    #             Actions = 'Add', 'Remove', 'Filter' \n \
    #             SECTORS = 'Industrials', 'Health Care', 'Information Technology', 'Utilities', 'Financials', 'Materials', 'Consumer Discretionary', \
    #             'Real Estate','Communication Services', 'Consumer Staples','Energy'  \n \
    #             Text:  Can you Add year to date change?. \n \
    #             Answer: {'Add':['YTD CHANGE(%)'],'Remove':[],'Filter':[]} \n \
    #             Text: Can you remove company sector and cik from this?. \n \
    #             Answer: {'Add': [], 'Remove': ['SECTOR', 'CIK], 'Filter': []} \n\
    #             Text: Show me the data again. \n \
    #             Answer: {'Add': [], 'Remove': [], 'Filter': []} \n \
    #             Text: Filter sector with Energy only. \n \
    #             Answer: {'Add': [], 'Remove': [], 'Filter': [{'Field': 'SECTOR', 'Value': 'Energy', 'Operation': '=='}]} \n \
    #             Text: Can you keep stocks with market cap greater than 4 billion dollars. \n \
    #             Answer: {'Add': [], 'Remove': [], 'Filter': [{'Field': 'SECTOR', 'Value': '4000000000', 'Operation': '>'}]} \n \
    #             Text: Can you keep stocks with cik less than than 3432?. \n \
    #             Answer: {'Add': [], 'Remove': [], 'Filter': [{'Field': 'SECTOR', 'Value': '3432', 'Operation': '<'}]} \n \
    #             Text: Hey I wanna see data. \n \
    #             Answer: {'Add': [], 'Remove': [], 'Filter': []} \n \
    #             Text:" + query + "\n \
    #             Answer:"
    #         return self.query(message)


if __name__ == "__main__":
    bot = OpenAIBot()
    print("In main.................")
    bot.get_intent("Hello")
