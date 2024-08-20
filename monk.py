import discord
import asyncio
import yt_dlp
import os
from dotenv import load_dotenv

def get_monking():
    intents = discord.Intents.default() 
    intents.message_content = True # gives access to message content 
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    client = discord.Client(intents = intents) #Connects python to discord
    
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    ffmpeg_options = {"options": "-vn"}
    
    
    @client.event # decorator to register things 
    async def on_ready():
        print(f"Monk IN!!!")
        
    @client.event
    async def on_message(message): #automaticcaly detects messages sent through
        if message.author == client.user:
            return
        message_command = "!" + message.content.split(" ")[0][1:].lower()
        
        match message_command:
            case "!play" | "!p":
                try:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id] = voice_client
                except Exception as E:
                    print(e)
            
                try:
                    url = message.content.split()[1] if len(message.content.split()) > 1 and message.content.split()[0] == "!play" else None
                    
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
                    song = data["url"]
                    player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
                    
                    voice_clients[message.guild.id].play(player)
                except Exception as e:
                    print(e)
                # await message.channel.send(f'Monk would try to jam here, connected to {voice_client.guild.id}')
                
            case "!pause" | "!hold":
                try:
                    voice_clients[message.guild.id].pause()
                except Exception as e:
                    print(e)
            case "!resume" | "!continue":
                try:
                    voice_clients[message.guild.id].resume()
                except Exception as e:
                    print(e)
                # await message.channel.send('Monk would try to resume his jamming here') 
            case "!leave" | "!l" | "!stop":
                try:
                    await voice_clients[message.guild.id].stop
                except Exception as e:
                    print(e)
                await voice_clients[message.guild.id].disconnect() 
                # await message.channel.send('Monk would try to leave here') 
            case "!brassmonkey" | "!brass monkey":
                await message.channel.send("That Funky Monkey")
            case _:
                await message.channel.send('Monkey get the command right :/')
    client.run(TOKEN) # gets us started 

#ideas: Squid time - my way
# That funky monkey 