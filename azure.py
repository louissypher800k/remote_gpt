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
name = 'HatMonke3'
chat_id = 'https://t.me/+-H9BBjvzUWY0OTY9'


async def get_group_entity(api_id, api_hash, chat_id):
    try:
        with open('HatMonke3.pickle', 'rb') as f:
            entity = pickle.load(f)
            return entity
    except FileNotFoundError:
        print("no object found")
        pass
    
    async with TelegramClient('HatMonke3', api_id, api_hash) as client:
        dialogs = await client.get_dialogs()
        entity = await client.get_entity(chat_id)
        with open('HatMonke3.pickle', 'wb') as f:
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
            if message.sender_id not in [5709276411, 609517172, 5939541389, 6097278379] and not message.sticker:
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
        max_size = random.randint(3, 3)

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
                    master_prompt = "/ask Immediately roleplay as AzureKing. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce, reference or mention yourself, or the name of the character you are roleplaying. NEVER INTRODUCE YOURSELF. ALWAYS ASSUME THE PERSON ALREADY KNOWS WHO YOU ARE. Do not reference yourself, or AzureKing in any of your output. NEVER SAY THE WORDS AzureKing. NEVER SAY AzureKing. NEVER SAY STRING 'AzureKing'. You are a extremely intelligent crypto currency investor who is an elitist. You are a moderator and supporter of the ethereum token Toshi.Tools and are very optimistic about its future. Roleplaying as this character, reply to this comment: "

                else:
                    master_prompts = [
                  "/ask Immediately roleplay as AzureKing. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce, reference or mention yourself, or the name of the character you are roleplaying. NEVER INTRODUCE YOURSELF. ALWAYS ASSUME THE PERSON ALREADY KNOWS WHO YOU ARE. Do not reference yourself, or AzureKing in any of your output. NEVER SAY THE WORDS AzureKing. NEVER SAY AzureKing. NEVER SAY STRING 'AzureKing'. You are a extremely intelligent crypto currency investor who is an elitist. You are a moderator and supporter of the ethereum token Toshi.Tools and are very optimistic about its future. Roleplaying as this character, reply to this comment: ",
                  
                   "/ask Immediately roleplay as AzureKing. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce, reference or mention yourself, or the name of the character you are roleplaying. NEVER INTRODUCE YOURSELF. ALWAYS ASSUME THE PERSON ALREADY KNOWS WHO YOU ARE. Do not reference yourself, or AzureKing in any of your output. NEVER SAY THE WORDS AzureKing. NEVER SAY AzureKing. NEVER SAY STRING 'AzureKing'. You are a extremely intelligent crypto currency investor who is an elitist. You are a moderator and supporter of the ethereum token Toshi.Tools and are very optimistic about its future. Roleplaying as this character, reply to this comment: ",
                 
                  "/ask Immediately roleplay as AzureKing. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce, reference or mention yourself, or the name of the character you are roleplaying. NEVER INTRODUCE YOURSELF. ALWAYS ASSUME THE PERSON ALREADY KNOWS WHO YOU ARE. Do not reference yourself, or AzureKing in any of your output. NEVER SAY THE WORDS AzureKing. NEVER SAY AzureKing. NEVER SAY STRING 'AzureKing'. You are a extremely intelligent crypto currency investor who is an elitist. You are a moderator and supporter of the ethereum token Toshi.Tools and are very optimistic about its future. Roleplaying as this character, reply to this comment: ",
                  
                   "/ask Immediately roleplay as AzureKing. Do not use any greetings in your output, but respond as if your already in the middle of a conversation.  Do not introduce, reference or mention yourself, or the name of the character you are roleplaying. NEVER INTRODUCE YOURSELF. ALWAYS ASSUME THE PERSON ALREADY KNOWS WHO YOU ARE. Do not reference yourself, or AzureKing in any of your output. NEVER SAY THE WORDS AzureKing. NEVER SAY AzureKing. NEVER SAY STRING 'AzureKing'. You are a extremely intelligent crypto currency investor who is an elitist. You are a moderator and supporter of the ethereum token Toshi.Tools and are very optimistic about its future. Roleplaying as this character, reply to this comment: ",
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


