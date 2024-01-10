import pandas as pd


class HistoryManagement:
    def __init__(self):
        self.history = []

    def add(self, messages):
        self.history.append(messages)

    def get(self):
        history = []
        for messages in self.history:
            for message in messages:
                history.append(message)
        return history
