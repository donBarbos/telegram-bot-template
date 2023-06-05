import json


with open("bot/texts/buttons.json", "r") as file:
    button_texts = json.load(file)

with open("bot/texts/messages.json", "r") as file:
    message_texts = json.load(file)
