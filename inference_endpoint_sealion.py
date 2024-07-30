import requests


#user_message = "Is Singapore a good city to live?"
#user_message = "What is the capital city for Malaysia?"
#user_message = "Cara untuk mendapat badan yang sihat dan cergas"
#user_message = "ทำอย่างไรให้ร่างกายแข็งแรง?"
user_message = """Translate the following text to Indonesian.
#Indonesia lies along the equator, and its climate tends to be relatively even year-round.
#"""

#user_message = """Translate the following text to Indonesian.
#Indonesia lies along the equator, and its climate tends to be relatively even year-round.
#"""


system_prompt = "you are an honest assistant"
chat_history =[]
max_new_tokens = 500

s = requests.Session()
output = s.get(
    "http://localhost:7992/query-stream/",
    stream=False,
    json={
        "user_query": user_message,
        "prompt_text": system_prompt,
        "history": chat_history,
        "max_new_tokens": max_new_tokens,
         }
)
 
print(output.json())