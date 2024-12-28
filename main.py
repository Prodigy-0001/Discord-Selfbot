import discord
from discord.ext import commands
import asyncio
import random
import string
import threading
import requests
import time
import json
import sys
import re
running_threads = {}



TOKEN = 'put token here'

PREFIX = "."

should_flood_file = "should_flood.txt"
should_flood = False

auto_responder_target_id = None
auto_pressure_target_id = None
user_reactions = {}
copied_messages = {}
active_countdowns = {}
layout_to_copy = {}
mimic_user = None

try:
    with open(should_flood_file, "r") as file:
        should_flood = bool(file.read())
except FileNotFoundError:
    pass  # If the file doesn't exist, start with the default value (False)

# Function to update the should_flood state in the file
def update_should_flood(value):
    with open(should_flood_file, "w") as file:
        file.write(str(value))


GC_Name = [
    "DONT DIE TO Prodigy CUNT ", "YOURE DYING RN LOLOL", "DIRTY CUCK", "i heard you were 4'11 champ", "Nigga your fucking harmless", "die to Prodigy" "STAY ALIVE ", "DO ME SUM THO?", "DIRTY CUCK", "SHORT STUFF", "SHORT NIGGA WALKIN ROUND WITH DOWNSYNDROME", "BOSSMAN DLOW 2.0" "Pussy ass nigga not pressing shit", "die to Prodigy" "im watching u rn.. ", "Prodigy SEED..", "Prodigy MADE U..", "3 milimeter defeater", "FUCK YO MOM NIGGA", "DAUGHTER "
]
Regular_Spammer_Message = [" # @everyone look at this loser PUSSY ASS NIGGA ", " # @everyone THIS NIGGA THOUGHT HE WAS HARMFUL LMFAOO ", " # Prodigy OWNS U FAGGOT BITCH", " # @everyone This nigga a fucking loser.", " # Fat pleb"]
additional_messages = [" ill rip ur heart out pussy FUCK ", " who r u ? ", " ew a cuck ", " somebody call this nigga's dad that left him!, KYS NO ONE LIKES U BITCH ASS NIGGA", "WATCH WHAT HAPPENS IF I BRING YTS AND 764 PUSSY ASS NIGGA "]
gc_name_counter = 0
spam_counter = 0  # Initialize spam_counter
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=",", self_bot=True, intents=intents)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

running_threads = {}

# Add Changer and spam_messages functions
def Changer(channel_id):
    global gc_name_counter
    while not threading.current_thread().stopped():
        try:
            random_name = random.choice(GC_Name)
            random_additional_name = random.choice(additional_messages)
            response = requests.patch(
                f'https://discord.com/api/v9/channels/{channel_id}',
                headers={"Authorization": TOKEN},
                json={"name": f"{random_name} and {random_additional_name}x {gc_name_counter}"}
            )
            response.raise_for_status()
            
            gc_name_counter += 1
            time.sleep(0.000000000000000000000000000000000000000000000000000000000000012)  # Adjust the delay as needed
        except Exception as e:
            print(f"An error occurred in Changer: {e}")
            time.sleep(1)  # Retry after delay
        


def spam_messages(channel_id):
    global spam_counter  # Declare spam_counter as a global variable
    while not threading.current_thread().stopped():
        try:
            random_message = random.choice(Regular_Spammer_Message)
            random_additional_spam = additional_messages[spam_counter % len(additional_messages)]
            response = requests.post(
                f"https://discordapp.com/api/v6/channels/{channel_id}/messages",
                headers={"Authorization": TOKEN},
                json={"content": f"{random_message} and  {random_additional_spam} x{spam_counter}"}
            )
            response.raise_for_status()
            
            spam_counter += 1  # Increment spam_counter
            time.sleep(0)  # Adjust the delay between messages as needed
        except Exception as e:
            print(f"An error occurred in spam_messages: {e}")
            time.sleep(0)  # Retry after delay



async def connect_to_voice(channel_id):
    uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
    event = asyncio.Event()
    while not event.is_set():
        try:
            async with websockets.connect(uri, max_size=None) as websocket:
                identify_payload = {
                    'op': 2,
                    'd': {
                        'token': TOKEN,
                        'intents': 513,
                        'properties': {
                            '$os': 'linux',
                            '$browser': 'my_library',
                            '$device': 'my_library'
                        }
                    }
                }
                identify_payload_str = json.dumps(identify_payload)
                await websocket.send(identify_payload_str)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': channel_id,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False,
                        'request_to_speak_timestamp': round(time.time())
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': None,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                url = f'https://discord.com/api/v9/channels/{channel_id}/call/ring'
                headers = {
                    'Authorization': f'{TOKEN}',
                    'User-Agent': 'my_library/0.0.1',
                    'Content-Type': 'application/json'
                }
                data = {'recipients': None}
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 204:
                    print('Notification sent')
                else:
                    print(f'Failed to notify GC with status code {response.status_code}')

        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(1)  # Retry after delay

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


# Command to perform actions in the specified GC
@bot.command()
async def gc(ctx, gc_id: int):
    if gc_id in running_threads:
        await ctx.send(f"Actions are already running in GC {gc_id}. Use >gc_end {gc_id} to stop them first.")
        return

    changer_thread = StoppableThread(target=Changer, args=(gc_id,))
    spam_thread = StoppableThread(target=spam_messages, args=(gc_id,))

    running_threads[gc_id] = [changer_thread, spam_thread]

    changer_thread.start()
    spam_thread.start()

    await connect_to_voice(gc_id)
    await ctx.send(f"Started Cuffing in GC {gc_id}")
@bot.command()
async def gc_end(ctx, gc_id: int):
    if gc_id not in running_threads:
        await ctx.send(f"No CUFFING  in GC {gc_id}.")
        return

    threads = running_threads.pop(gc_id)
    for thread in threads:
        thread.stop()
        thread.join()

    await ctx.send(f"Stopped Cuffing in GC {gc_id}")

auto_responses = [
      "",
      " youre impure ",
      " dirty cuck ",
      "barrel shotgun nose",
      "rooster foot",
      "nigga got a baseball bat nose",
      "tapdancing killer clown with a gorilla foot",
      "i made you tho?",
      "# nigga captures scorpians",
      " # fat ass nose..",
      "# nonce",
      "# pedo",
      "# kid touching weirdo",
      "# you pay no bills",
      "unloved dildo nose",
      "# giant skateboad back",
      "used ass wipe ",
      "walking shitstain",
      "yo granny smoke cigs",
      "yo granny talk through a pipe",
      "0 vpm",
      "0/10 ragebait",
      "father 4 father rn?",
      "0/10 aura..",
      "nigga you stink like shit",
      "Prodigy ran a train on ur mom..",
      'COME DIE LMFAO',
'NIGGA IS ASS AS FUCK',
'☠️ 😭',
'UR GONNA STAY THE FUCK DOWN',
'UR FUCKING SHITTY',
'DIE TO UR FUCKING LORD',
'# LOLOL ',
'# OUTLAST ME I WONT STOP ',
' # ODO WONT WORK',
'☠️ 😭',
'NIGGA WHERE THE FUCK ARE U',
'# NIGGA FUCKING DIED',
'# UR SHIT LMAO IM CLOWNING U',
'SLOW FUCK I WIN LMFAOOO',
'# NIGGAS SLOW AS FUCK',
'UR ASS',
'SIT THE FUCK DOWN RЕTARD LMFAO',
'UR A GAY FAGGОT LMAO',
'# U SUCK NIGGA',
'GO FASTER BITCH',
'COME HERE',
'UR A FUCK TOY',
'U WONT DO SHIT',
'STUPID FUCK',
'# SLOW ASS NIGGA',
'# UR A FUCKING LOSER',
'NIGGAS CANT FW YTS',
'POOR ASS FUCK NIGGA',
'U CANT OUTLAST ME',
'I WIN U FUCKING RETARD LFMAO UR NOT DOING SHIT',
'# U CANT FUCKING PRESSURE',
' # Prodigy RUN YOU LOMAAOSODKDJDJ',
' # Prodigy HOED YO BITCH ASS LOL',
'WHY THIS NIGGA SOME SHIT LMFAO', 
'KNEEL',
'# Dont Ping Me I Dont Fw You..',
'wait who r u again..',
'Prodigy made u bite da curb...',
'suck my cock faggot',
'ill cuff yo bitch PUSSY',
'# LOLOL ',
'# OUTLAST ME I WONT STOP ',
'shit turd',
'DONT DIE TO ME BITCH',
'HOLY SHIT YOU ARE DOGSHIT', 
'SLICE N DICE UR NECK NOW',
'Prodigy IS BULLYING YOU LMAO',
'DONT RUN TO A CLIENT BUDDY',
'WYA? ION SEE U',
'G-G-GG-ETDOWN FUCK NIGGA',
'HOW TF CAN ANYONE BE THIS SLOW BRO?',
'GOTTA GO FAST!',
'KEEP TF UP BITCH',
'WHO TOLD YOU TO STOP? KEEP GOING',
'ROSE TOY',
'SEX DOLL',
'PLATYPUS FUCKER',
'BULLDOZER BELLY',
'PENGUIN BREATHE',
'U SAID RED BULL GIVE U WINGS AND JUMPED OFF THE EMPIRE STATE BUILDING N DIED',
'MY FOOT IS ON UR HEAD LMAOOAL',
'JESUS CHRIST PLEASE SLOW ME DOWN FOR THIS RETARD',
'TRY UR BEST -1000 AURA PAL :nerd:',
'NIGGAS NOT DOIN SHIT',
'WRISTSLITTER',
'# cut for me ',
'CUCK',
'fag bag',
'# DIE TO ME LOL', 
'# U CANT FUCKING MANUAL', 
'# KYS',
'# UR A FAT PLEB FAT NIGGA',
'# ur waste of my time',
'# Ur a cornball, u cant stop texting',
' # Low tier trash',
' # Nigga cant do non LOL',

    
    # Add more responses as needed
]
auto_responses_enabled = True
auto_adder_enabled = False
auto_adder_thread = None
user_id_to_add = None



# Discord bot events and commands
@bot.event
async def on_ready():
    print(f" ** Logged in as: {bot.user.name} **")
    print("Prodigys bot pussy!!")
    print(",check (to check the bot lil bro)")

# Command to set victim users for auto-responder and auto-pressure functionalities
@bot.command()
async def target(ctx, auto_responder: discord.User, auto_pressure: discord.User):
    try:
        # Set the global variables to the IDs of the mentioned users
        global auto_responder_target_id, auto_pressure_target_id
        auto_responder_target_id = auto_responder.id
        auto_pressure_target_id = auto_pressure.id

        # Print out the mentions for debugging
        auto_responder_mention = auto_responder.mention
        auto_pressure_mention = auto_pressure.mention
        print(f"Auto-responder mention: {auto_responder_mention}, Auto-pressure mention: {auto_pressure_mention}")
        await asyncio.sleep(1)
        # Send a confirmation message
        confirmation_msg = await ctx.send("Victim IDs set for Auto-Responder and Auto-Pressure.")

        # Delete the confirmation message after 1 second
        await asyncio.sleep(1)
        await confirmation_msg.delete()

        # Delete the command message after 1 second
        await asyncio.sleep(1)
        await ctx.message.delete()

    except Exception as e:
        print(f"An error occurred in 'victim' command: {e}")
        await ctx.send("An error occurred while setting victim IDs.")




# Command to check the bot's status
@bot.command()
async def check(ctx):
    msg = await ctx.send("**WSP FAGGOT DOES Prodigy OWN YOU**")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()

# Command to disable auto-responses
@bot.command()
async def end(ctx):
    global auto_responses_enabled
    auto_responses_enabled = False
    msg = await ctx.send(" **ProdigyS - OFF** ")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()

# Command to enable auto-responses
@bot.command()
async def start(ctx):
    global auto_responses_enabled
    auto_responses_enabled = True
    msg = await ctx.send(" **ProdigyS POWER - ON* ")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()

# Command to set reaction for a user
@bot.command()
async def react(ctx, user: discord.User, emoji: str):
    # Add or update the user's reaction in the dictionary
    user_reactions[user.id] = emoji

# Command to remove reaction for a user
@bot.command()
async def reactend(ctx, user: discord.User):
    # Check if the user ID exists in the dictionary
    if user.id in user_reactions:
        # Remove the user ID from the dictionary
        del user_reactions[user.id]
    else:
        await ctx.send(f"Nigga damn got me doing all this work {user.name}")





@bot.event
async def on_message(message):
    
 


    # Check if the message is from a user with a specified reaction
    if message.author.id in user_reactions:
        # React to the message with the specified emoji
        emoji = user_reactions[message.author.id]
        await message.add_reaction(emoji)
    
    # Check if auto-responses are enabled and the message is from the auto-responder target
    if auto_responses_enabled and message.author.id == auto_responder_target_id:

        # Select a random auto-response and send it
        response = random.choice(auto_responses)
        await message.reply(response)
        # You can also add reactions here if needed
    if message.author.id in copied_messages:
        # Send the copied message using the bot
        await message.channel.send(copied_messages[message.author.id])
    # Continue processing other commands and events
        
    global mimic_user
    if mimic_user and message.author == mimic_user:
        await message.channel.send(message.content)
    
    
    
    
    
     # Check if the message author was in the active countdowns
    if message.author in active_countdowns:
        # Remove the user from active countdowns
        del active_countdowns[message.author]
        await message.channel.send(f"Cancelling Afk Check.....")

    await bot.process_commands(message)





# Command to display the command menu
@bot.command()
async def cmds(ctx):

   
    cmds_text = "```# "
    
    cmds_text += "MOON + SUN SB MADE BY PRODIGY"

    cmds_text += " check -  Check if the bitch is on.\n"
    
    cmds_text += "# gc (gc id) -  Gc Spammer/Fuck the gc\n"
    
    cmds_text += "# react (user_here) (emoji_here) -  Come on you know wtf this is.\n"
       
    cmds_text += "# start - Enables The Fucking Auto Responder.\n"

    cmds_text += "# react (user) [emoji] -  idk why i made two but yh.\n"
    
    cmds_text += "# reactend -  (user): stops fucking putting emojis retard.\n"
    
    cmds_text += "# Start (auto_responder) (auto_pressure) -  Set victim IDs for auto-responder and auto-pressure functionalities.\n"
       
    cmds_text += "***Prodigy owns u lol*** ```"
    
    cmds_message = await ctx.send(cmds_text, delete_after=50)  # Self-delete after 10 seconds
# Run the bot
bot.run(TOKEN, bot=False)
