import os

import discord
import requests

#from dotenv import load_dotenv

#load_dotenv()
TOKEN = "MTA3NjYyNjAxMjM5NTI3NDI2MA.GizPcc.bBgYpuLlm8CdwVMBR1zSh6g6LplTKr0X6GpWwI"
GUILD = "1076626797061488640"
API_SERVER = "http://10.18.210.197:8001"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

"""def format(threadMessages):
    for i in range(threadMessages):
        if i == 0:
            prepend with Q:
        else if i%2 == 0:
            prepend with A:
        else prepend with Q:
    
    return

    return Q/A format
def deal(message, thread):

    formattedThread = format(thread)
    # response = make a get request, with parameter formattedThread
    response = formattedThread
    return response"""
def removeExclQuery(query):
    #Given the string !query Hello, return only Hello
    if query.startswith('!query'):
        return query[7:]
    return query

def dealWithMSG(query):
    pass


def processQuery(messages):
    processedMessages = ""
    for i in range(len(messages)-1,0,-1):
        print(messages[i])
        if i == len(messages)-1 or messages[i].content.startswith('!query'): 
            processedMessages += 'Q: '+ removeExclQuery(messages[i].content) +"\n"
        elif messages[i].author.name == 'nyuHackBot' or messages[i].author.name =='Shubh587':
            if messages[i].content.startswith('Hello') and messages[i].author.name == 'nyuHackBot':
                continue
            if messages[i].content == "I don't know.":
                continue
            processedMessages += 'A: '+messages[i].content + "\n"
    return processedMessages 

#this is for the post request to interact with LLM
def get_response(query, history = None):
    data = {
        "message": query,
    }
    print('payload of POST',data)
    if history is not None:
        data['history'] = history
    x = requests.post(API_SERVER+"/query", data = data)
    response = x.json()
    print('response of POST',response)
    if(x.status_code == 200):
        return response['text']
    else:
        return "Exception occured"

#this is the end of thread signal put queries
def get_response_put(history):
    data = {}
    if history is not None:
        data['history'] = history
    else:
        return "No history to process"
    x = requests.put(API_SERVER+"/upvote", data = data)
    response = x.json()
    if(x.status_code == 200):
        return response['text']
    else:
        return "Exception occured"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #print('Professor' in [role.name for role in message.author.roles])
    if message.content.startswith('!query') and message.channel.name == 'general':
        #print(message)
        print("channel")
        #https://stackoverflow.com/questions/71797750/how-to-send-message-in-a-discord-thread
        thread = await message.channel.create_thread(name="Thread" , type=discord.ChannelType.public_thread )
        formattedMsg = removeExclQuery(message.content)
        await thread.send( message.content )
        response = get_response( removeExclQuery(message.content) )
        await thread.send(response)
        
    elif message.content.startswith('!query') and message.channel.name != 'general':
        #print(message)
        print("thread")
        thread_id = message.channel.id
        thread = message.guild.get_thread(thread_id)
        
        queryToProcess = [message async for message in thread.history()]
        formattedHist = processQuery(queryToProcess)
        response = get_response( removeExclQuery(message.content) , formattedHist )
        await thread.send(response)


    elif message.content.startswith('!done') and message.channel.name != 'general':
        thread_id = message.channel.id
        thread = message.guild.get_thread(thread_id)
        if "\U0001F44D" in message.content:
            print("bingo")
            queryToProcess = [message async for message in thread.history()]
            formattedHist = processQuery(queryToProcess)
            response = get_response_put( formattedHist )
            await message.add_reaction("👍")
        #for thumbsdown cases
        elif "\U0001F44E" in message.content:
            print("This message contains a thumbs down emoji!")
            professor_role = discord.utils.get(message.guild.roles, name="Professor")
            await thread.send(f"Hello {professor_role.mention}, this is a message for you!")
            #send to API to learn from failure

            

client.run(TOKEN)


"""
<Message id=1076648261777105017 channel=<TextChannel id=1076626797061488644 name='general' position=0 
nsfw=False news=False category_id=1076626797061488641> type=<MessageType.default: 0> author=<Member 
id=881987116635160596 name='fenderbender' discriminator='5706' bot=False nick=None guild=<Guild 
id=1076626797061488640 name="fenderbender's server" shard_id=0 chunked=False member_count=3>> 
flags=<MessageFlags value=0>>

<Message id=1076648320505745448 channel=<Thread id=1076648262217502782 name='Thread' parent=general 
owner_id=1076626012395274260 locked=False archived=False> type=<MessageType.default: 0> 
author=<Member id=881987116635160596 name='fenderbender' discriminator='5706' bot=False 
nick=None guild=<Guild id=1076626797061488640 name="fenderbender's server" shard_id=0 
chunked=False member_count=3>> flags=<MessageFlags value=0>>


        queryToProcess = [message.content async for message in thread.history()]
        for i in range(len(queryToProcess)-1, -1, -1):
            if i == 0:
                print("Q: " + queryToProcess[i])
            elif i%2 == 0:
                print("A: " + queryToProcess[i])
            else:
                print("Q: " + queryToProcess[i])
"""