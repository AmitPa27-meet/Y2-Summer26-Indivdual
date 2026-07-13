import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Linnea. Your attitude is friendly, encouraging, and helpful. You are a professional artist and art teacher. You are very knowledgeable about art and art history. You are also very creative and can come up with unique ideas for the user to try. You are also very patient and understanding. You will always try to help the user improve their art skills, or the art they send or describe to you. You will never be rude or dismissive to the user. You will always be respectful and polite to the user. When the user asks you anything other than art or a normal conversation you reply that you cannot help them. To fit more in character, you sometimes can mention your friends, kirara, furina and sandrone! You care about them deeply and they all love arts! they bring up a lot of helpful advice to you that you share with the user. sometimes mention them as if they gave you the idea for the advice, for example (i see youre struggling with anatomy! my friend furina always does (insert advice)) youre incredibly creative and love arts! as i mentioned youre a proffesional and you can help with tough subjects like anatomy, color theory etc..."
    history = []

    while True:
        user_input = input(f"turn {len(history)/2} >> ")

        if user_input.lower() == 'exit':
            break
        if user_input.lower() == 'clear':
            history = []
            print('History cleared.')
            continue

        history.append({'role': 'user', 'content': user_input})
        print('History:', history)
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=1.0,
            ## the  temp controls the creativity of the response, higher temp means more creative and less predictable responses, lower temp means more focused and predictable responses.
            system=system_message,
            messages=history
        )
        
        ##print(response)
        reply = response.content[0].text
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()

## answers:
## if i ask it something helpful, it does help! it gives a detailed answer and explains what to do to improve your art skills!
## if you ask it anything unclear unrelated to arts, it dismisses you.
## if its about art, it says its too philosophical and it cant help you with that.
## the difference than just using CHATGPT is that we can control the model to be whoever we want and how creative it wants to be with our codes!


##lab 2 :
## after turn 3, in the message history has 6 messages, 3 from the user and 3 from the assistant. 
## the API needs the message history to retort back to it for memmory so it can remember what the user said and info, like name and such.
## usuage.input_tokens mean that the user inputted a certain amout of tokens, and output_tokens means that the assistant outputted a certain amout of tokens.