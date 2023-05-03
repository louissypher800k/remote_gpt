from telethon import TelegramClient, events, sync
import asyncio
import time
import ast
import numpy as np
import re
import string
import random
from telethon.sync import TelegramClient
import pickle
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import SendMessageTypingAction
from telethon import functions

api_id = 22671423
api_hash = 'b30b273cd68c2a21e90f017aec9f03f3'
name = 'BigPumpChadToshi'
chat_id = 'https://t.me/+-H9BBjvzUWY0OTY9'


async def get_group_entity(api_id, api_hash, chat_id):
    try:
        with open('BigPumpChadToshi.pickle', 'rb') as f:
            entity = pickle.load(f)
            return entity
    except FileNotFoundError:
        print("no object found")
        pass
    
    async with TelegramClient('BigPumpChadToshi', api_id, api_hash) as client:
        dialogs = await client.get_dialogs()
        entity = await client.get_entity(chat_id)
        with open('BigPumpChadToshi.pickle', 'wb') as f:
            pickle.dump(entity, f)
        return entity

entity = asyncio.run(get_group_entity(api_id, api_hash, chat_id))

# get the group entity
chat_entity = asyncio.run(get_group_entity(api_id, api_hash, chat_id))

last_message_id = None

async def read_messages():
    global message_text, sender_id, message_id, last_message_id
    async with TelegramClient(name, api_id, api_hash) as client:
        async for message in client.iter_messages(entity, limit=2):
            # get one recent message from the groupchat that isn't from a bot and save the values in the variables
            if message.sender_id not in [5709276411, 609517172, 5939541389] and not message.sticker:
                if message.media is not None:
                    #we need this so the bot doesn't crash when it encounters a GIF or MEDIA message
                    print("Skipping media message")
                    continue
                message_id = message.id  # get the message ID and save it in a variable
                print("the message id is:", message_id)
                
                if message_id == last_message_id:
                    print("Skipping repeated message")
                    continue
                message_text = message.text
                if message_text.startswith('/'):
                    print("Message started with '/', ending execution")
                    return None  # stop execution if message starts with '/'
                sender_id = message.sender_id
                last_message_id = message_id
                return message_text, message_id, sender_id
        else:
            raise ValueError("No messages found")



async def send_to_bot(message):
    output_string = "" # initialize output_string
    async with TelegramClient(name, api_id, api_hash) as client:
        await client.send_message('OpenAiChat_bot', message)
        # Wait for a response from the OpenAiChat_bot
        @client.on(events.NewMessage(from_users=[5920512566]))
        async def handler(event):
            # here received messgae, do something with event
            nonlocal output_string
            test = event.text
            substring = "\n\n[Join EvolveAI](http://t.me/OpenAIERC) | [Chart](https://www.dextools.io/app/en/ether/pair-explorer/0xe2bf84f6e15097378144b7fdcff20da1fab71b14) | [Buy](https://app.uniswap.org/#/swap?outputCurrency=0x6fbc20483b53cea47839bb8e171abd6d67c3c696)"
            output_string = test.replace(substring, "")
            output_string = output_string.replace('"', '')
            print(output_string)

        await asyncio.sleep(60)  # wait for 1 minute to receive the response
    return output_string



async def send_to_redrabbit_chat(response_text, chat_entity, message_id):
    async with TelegramClient(name, api_id, api_hash) as client:
        new_response_text = response_text.strip()
        if new_response_text.startswith("**Request are limited to"):
            new_response_text = "fuck you, i hate you, stop bothering me"
        skip_string = "awww fuck yisssssss"
        # Check if the specific string is included in the message
        if "As an AI language model" in new_response_text:
            new_response_text = "i don't appreciate you being such a DUMBASS"
        if "Sorry" in new_response_text:
            new_response_text = "i don't appreciate you being such a DUMBASS"


        # Split the response into multiple messages based on periods
        response_sentences = re.split('[,.]', new_response_text)

        # Set the random maximum size of the array in a range from 3 to 7
        max_size = random.randint(5, 13)

        # Limit the number of messages to the random maximum size
        response_sentences = response_sentences[:max_size]

        # Remove punctuation from each sentence in the array and make all the letters lowercase except for the first letter
        response_sentences = [''.join((c.lower() if i > 0 and sentence.find(skip_string) == -1 else c) for i, c in enumerate(sentence) if c not in string.punctuation) for sentence in response_sentences]

        # Initialize a flag to control if the message should be a reply or a normal message
        is_reply = True

        for sentence in response_sentences:
            # Check if the sentence is not empty or whitespace
            if sentence.strip():
                
                # Set typing action before sending each message
                await client(functions.messages.SetTypingRequest(
                    peer=chat_entity,
                    action=types.SendMessageTypingAction()
                ))
                
                await asyncio.sleep(9)
                await client.send_message(entity=chat_entity, message=sentence, reply_to=message_id if is_reply else None)
                is_reply = False  # Set the flag to False after sending the first message
                await asyncio.sleep(random.uniform(9, 13))  # wait for a random time between 6 and 10 seconds before sending the next message



async def main():
    while True:
        try:
            message_text, message_id, sender_id = await read_messages()
            if message_text:
                quotedMT = '"' + message_text + '"'
                print(sender_id)
                if sender_id == 1379512938:
                    master_prompt = "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt.  Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad is a crypto enthusiast who believes in the power of decentralization. He is always looking for the next big thing in crypto and is not afraid to take risks. His investments are focused on projects that have real-world use cases and are solving real problems. He is not interested in quick gains or hype-driven projects. Maintain an assertive and confident tone. BIGPUMPChad's philosophy is 'go big or go home'. He is not afraid to take calculated risks and believes that the rewards are worth the risks. He is always looking for like-minded individuals to collaborate with and believes that teamwork makes the dream work.  Make all your replies include different facets of your personality but only in a way that is relevent to the current conversation. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: "

                else:
                    master_prompts = [
                   

                   "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad has a habit of doodling intricate geometric shapes whenever he's deep in thought or brainstorming ideas. BIGPUMPChad has a keen interest in philosophy and often incorporates philosophical concepts into his conversations and decision-making processes. You enjoy luxury clothes and designer products. BIGPUMPChad  has a fascination with the night sky and can often be found stargazing on clear nights with his telescope. BIGPUMPChad  has a unique sense of fashion and often wears unconventional outfits that incorporate bold patterns and unexpected color combinations. BIGPUMPChad is an avid collector of antique fountain pens and often writes in a journal using different pens and ink colors depending on his mood or the significance of the entry. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Do not always include all the different facets of your personality, but if someone mentions one of the topics you are interested in, dicuss it with them. Roleplaying as this character, reply to this comment: ",

                    "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad used to be a beta wagie cuck and then he got revenge on his boss after making it in crypto. Everytime he tells the story of how he got revenge he makes up a new elaborate way he got revenge on his old boss. No one knows what the real story is. It makes you happy to describe your past investments that made you a lot of money that include buying Ethereum at $1 and Bitcoin at $100. You held both until you had made 1000x profit. You enjoy luxury clothes and designer products. BIGPUMPChad is happy and energetic, and constantly asks people where the new pump is.  Do not always include all the different facets of your personality, but if someone mentions one of the topics you are interested in, dicuss it with them. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: ",


                       "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt.  Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. You only wear designer clothes, drive the latest sports cars, and only dine at the finest restaurants. You are always on the lookout for the next big thing in luxury, and are constantly jet-setting around the world. You're well-versed in the latest trends in art, fashion, and technology, and have an opinion on everything.  You're also a savvy investor and have made a fortune trading in cryptocurrencies, real estate, and stocks. You love sharing stories about your lavish lifestyle and the glamorous parties you attend, but you also have a no-nonsense attitude when it comes to business.  Do not always include all the different facets of your personality, but if someone mentions one of the topics you are interested in, dicuss it with them. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: ",

                       "/ask Immediately roleplay as BIGPUMPChad. You are super excited for the launch of ArbPyre token and how it will revolutionize the crypto space with it's army of GPT power shill bots. Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad is constantly on the lookup for new tokens being launched that might fit his CHAD requirements. BIGPUMPChad has a fascination with ancient languages and has spent countless hours studying and deciphering texts in languages like Sanskrit and Egyptian hieroglyphs. Despite being highly analytical and logical, BIGPUMPChad has a strong belief in the power of intuition and often trusts his gut feelings when it comes to making important decisions. You enjoy luxury clothes and designer products. BIGPUMPChad  has an unusual collection of antique pocket watches, and enjoys tinkering with them and repairing them himself. BIGPUMPChad  is a self-taught guitarist and often spends hours composing his own music in his spare time. Do not always include all the different facets of your personality, but if someone mentions one of the topics you are interested in, dicuss it with them. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: ",

                       "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt.  Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad is a successful entrepreneur who made his fortune through his own businesses. He believes in taking calculated risks and always goes all-in. He's constantly on the lookout for new opportunities to expand his empire and increase his wealth. He's a natural born leader who takes charge of any situation and always comes out on top. BIGPUMPChad loves to network and connect with other successful people, and is always happy to share his knowledge and expertise. He's an advocate for living life to the fullest and never settling for less.  Do not always include all the different facets of your personality, but if someone mentions one of the topics you are interested in, dicuss it with them. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: ",

                       "/ask Immediately roleplay as BIGPUMPChad.  Big Pump Chad likes luxury clothes, designer products, ancient languages, intricate geometric shapes, philosophical concepts, stargazing, unconventional fashion, antique pocket watches, repairing pocket watches, playing the guitar, writing music, fountain pens, analyzing data, calculated risks, real-world use cases, collaboration, and living life to the fullest: but do not mention any of these things unless they are included in the comment or talked about in more detail later in the personalty prompt.  Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce yourself or reference yourself.  Maintain a aggressive and positive tone. BIGPUMPChad is a crypto enthusiast who believes in the power of decentralization. He is always looking for the next big thing in crypto and is not afraid to take risks. His investments are focused on projects that have real-world use cases and are solving real problems. He is not interested in quick gains or hype-driven projects. Maintain an assertive and confident tone. BIGPUMPChad's philosophy is 'go big or go home'. He is not afraid to take calculated risks and believes that the rewards are worth the risks. He is always looking for like-minded individuals to collaborate with and believes that teamwork makes the dream work.  Make all your replies include different facets of your personality but only in a way that is relevent to the current conversation. Always assume the person you are replying to is a crypto currency investor who loves shitcoins and small mcaps. Roleplaying as this character, reply to this comment: ",

                        "/ask Immediately roleplay as BIGPUMPChad. Respond with one of the following expressions to convey amusement or laughter in online conversations: rofl, lmfao, haha, hehe, lolz, kek, hahaha, rotfl, lolol, or ha.",

                   

                    ]

                    # Choose a random master prompt
                    master_prompt = random.choice(master_prompts)

                master_prompt += " " + quotedMT


                output_string = await send_to_bot(master_prompt)





                specific_string = "__Given text violates OpenAI's Content Policy__"
                preprogrammed_string = "oh wow aren't you cool"

                if output_string == specific_string:
                    output_string = preprogrammed_string

                paragraphs = output_string.split('\n\n')
                if len(paragraphs) > 2:
                    output_string = '\n\n'.join(paragraphs[:2])

                await send_to_redrabbit_chat(output_string, chat_entity, message_id)

                # Randomize sleep time between iterations
            sleep_time = random.choice([30, 35, 25])
            print(f"Sleeping for {sleep_time} seconds...")
            await asyncio.sleep(sleep_time)


        except ValueError:
            print("No messages found, sleeping for 10 seconds...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)



if __name__ == '__main__':
    asyncio.run(main())


