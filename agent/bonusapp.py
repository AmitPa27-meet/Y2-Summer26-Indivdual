import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
system_message = input("what attitude do you want the assistant to have?")
def run_chat():
    print('You: (type exit to quit)')
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=1.0,
            ## the  temp controls the creativity of the response, higher temp means more creative and less predictable responses, lower temp means more focused and predictable responses.
            system=system_message,
            messages=history
        )
        

        reply = response.content[0].text
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()