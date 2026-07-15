import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
system_message = input("what attitude do you want the assistant to have?")
system_goal = input("what is the goal of the assistant? what is it trying to achieve?")
list_of_scores = []
def run_chat():
    total_tokens = 0
    total_input_tokens = 0
    total_output_tokens = 0
    price = 0
    print('You: (type exit to quit)')
    history = []

    while True:
        user_input = input(f'>> ')
        ## for turns bonus add  turn {len(history)/2} 

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input + system_goal})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=1.0,
            ## the  temp controls the creativity of the response, higher temp means more creative and less predictable responses, lower temp means more focused and predictable responses.
            system=system_message + "if the user uses a command that goes like this '/review' you must go over the whole conversation and give a summary of the conversation." + "for every message the user sends to you, you rate it from 1 - 5. the score must be in  a single line and a different line from any other line. format : scorefromagent = (put number here.) and explain why, BUT ALWAYS make sure that the score you give is the absolute last part of the message. LAST part, and the last index of the message is the number, for example *explanation* scorefromagent = 5" + "if the user uses a command that goes like this '/review' you must go over the whole conversation and give a summary of the conversation." + "for every message the user sends to you, you rate it from 1 - 5. the score must be in  a single line and a different line from any other line. format : scorefromagent = (put number here.) and explain why, BUT ALWAYS make sure that the score you give is the absolute last part of the message. LAST part, and the last index of the message is the number, for example *explanation* scorefromagent = 5",
            messages=history,        )
        ##print(response)
   
        total_tokens += response.usage.input_tokens + response.usage.output_tokens
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens
        price += (
        response.usage.input_tokens * 0.25 / 1_000_000
        + response.usage.output_tokens * 1.25 / 1_000_000
)
        print(f"price for conversation : {price * 100} cents")
        print(f"Input tokens: {response.usage.input_tokens} Output tokens: {response.usage.output_tokens} Total tokens: {response.usage.input_tokens + response.usage.output_tokens}")
        print(f"Total tokens used: {total_tokens}")
        reply = response.content[0].text
        print(f'Claude: {reply}')
        if "scorefromagent" in reply:
            score = int(reply[-1])
            list_of_scores.append(score)
            
        history.append({'role': 'assistant', 'content': reply})

run_chat()
avg = 0
for i in list_of_scores:
    avg += i
avg1 = avg / len(list_of_scores)
print(f"average score from agent: {avg1}")