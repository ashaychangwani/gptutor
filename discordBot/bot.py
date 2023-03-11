import os
import asyncio
import requests
import interactions  
import json

TOKEN = os.getenv('DISCORD_TOKEN')
API_SERVER = "http://127.0.0.1:8001"
tracked_threads = []
GUILD_NUM = os.getenv('GUILD_NUM')
client = interactions.Client(token=TOKEN)

@client.event
async def on_ready():
    global GUILD, PROFESSOR_ROLE
    print(f'Connected to Discord!')
    GUILD = client.guilds[0]
    PROFESSOR_ROLE = next((role for role in await GUILD.get_all_roles() if role.name == 'professor'), None)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

async def get_history(channel):
    message_history = [message for message in await channel.history().flatten()]
    history = []
    for i, message in reversed(list(enumerate(message_history))):
        content = message.referenced_message.content if i == (len(message_history) - 1) else message.content
        if message.author == await client.get_self_user():
            if content.startswith("I don't know") or content.startswith("Hello") or content.startswith('Thanks for confirming'):
                continue
            if i == (len(message_history) - 1):
                history.append(content) #The first message in the thread is the query
            else:
                history.append(" A: " + content)
        elif message.author.username == 'PROF':
            history.append(" A: " + content)
        else:
            history.append(" Q: " + content)
    return history

#this is for the post request to interact with LLM
def get_response(query):
    data = {
        "message": '\n'.join(query)+"\n A: ",
    }
    print('payload of POST',data)
    x = requests.post(API_SERVER+"/query", data = data)
    response = x.json()
    print('response of POST',response)
    if(x.status_code == 200):
        return response['text']
    else:
        return "Exception occured"

#this is the end of thread signal put queries
def thread_done(history):
    data = {}
    if history is not None:
        data['history'] = history
    else:
        return "No history to process"
    
    x = requests.put(API_SERVER+"/upvote", data = json.dumps(data))
    response = x.json()
    if(x.status_code == 200):
        return response['text']
    else:
        return "Exception occured"

@client.command(
    name="query",
    description="Ask a query for the tutor!",
    scope=GUILD_NUM,
)
@interactions.option(
    name="text",
    description="What is your question?",
    type=interactions.OptionType.STRING,
    required=True,
)
async def query(ctx, text):
    message = await ctx.send("Q: " + text)
    thread = await ctx.channel.create_thread(name=text, message_id=message)
    tracked_threads.append(thread)
    history = await get_history(thread)
    response = get_response(history)
    await thread.send(response)

@client.event
async def on_message_create(message):
    if message.author == await client.get_self_user() or message.author.username == 'deepk':
        return
    thread = await message.get_channel()
    if thread in tracked_threads:
        history = await get_history(thread)
        response = get_response(history)
        await thread.send(response)

@client.command(
    name="downvote",
    description="Ask for the professor's attention",
    scope=GUILD_NUM,
)
async def downvote(ctx):
    reply = f'Hello {PROFESSOR_ROLE.mention}, this is a message for you!'
    await ctx.send(reply) 

@client.command(
    name="done",
    description="End the thread and update the model",
    scope=GUILD_NUM,
)
async def done(ctx):
    thread = await ctx.get_channel()
    if thread in tracked_threads:
        message = await ctx.send('Thanks for confirming! The model has been updated 👍', ephemeral=False)
        thread = await message.get_channel()
        history = await get_history(thread)
        tracked_threads.remove(thread)
        response = thread_done(history)
    else:
        await ctx.send('This command can only be called in an active query thread', ephemeral=True)

client.start()