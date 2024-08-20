import discord
from discord.ext import commands
import asyncio
import yt_dlp
import random #for encoding ID
import os
from dotenv import load_dotenv

def get_monking():
    intents = discord.Intents.default() 
    intents.message_content = True # gives access to message content 
    intents.members = True 
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    client = commands.Bot(command_prefix= "!", intents = intents) #Connects python to discord, sets up preffix 
    
    queues = {}
    voice_clients = {}
    is_looped = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    
    
    @client.event # decorator to register things 
    async def on_ready():
        print(f"Monk IN!!!")
        
    def id_encrypter(id: int):
        random.seed(id)
        return str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." +  str(random.randint(0,255)) + "."
    
    async def play_next(ctx, link): 
        if is_looped[ctx.guild.id]:
            await play(ctx, link = link)  
        elif queues[ctx.guild.id] != []:
            link = queues[ctx.guild.id].pop(0)
            await play(ctx, link = link)
    
    @client.command(name = "play")   
    async def play(ctx, *,link):
        if ctx == None or link == None:
            await ctx.send("Monke play WHAT exactly")
            return
    
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except AttributeError as a:
            await ctx.send("Monke you must be in channel")
        except discord.ClientException as e: # queues song if already connected
            if voice_clients[ctx.guild.id].is_playing():
                await queue(ctx, link)
                return
            else: 
                None
            
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download = False))
            
            song = data["url"]
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
                    
            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, link), client.loop)) 
        except Exception as e:
                    print(e)
        
    @client.command(name = "clear")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("Monk got rid of the songs")
        else:
            await ctx.send("Monkey its empty")
            
    @client.command(name = "skip")
    async def skip(ctx):
        voice_clients[ctx.guild.id].stop()
        await play_next(ctx)
    
    @client.command(name = "loop")
    async def loop(ctx):
        try:
            if is_looped[ctx.guild.id]:
                is_looped[ctx.guild.id] = False
                await ctx.channel.send("Ending the suffering")
            else:
                is_looped[ctx.guild.id] = True
                await ctx.channel.send("I was crazy once")
        except KeyError as e:
            is_looped[ctx.guild.id] = True
            await ctx.channel.send("I was crazy once")
    
    @client.command(name = "pause")    
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)
            
    @client.command(name = "resume")    
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)
            
    @client.command(name = "stop")    
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop
            await voice_clients[ctx.guild.id].disconnect() 
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @client.command(name = "identify")
    async def identify(ctx, user):
        user_id = [member.id for member in ctx.guild.members if user == member.display_name or user == member.name][0]
        await ctx.send(f"{id_encrypter(user_id)}\n:)")
        
    @client.command(name = "brassmonkey")    
    async def brassmonkey(ctx):
        try:
            await ctx.channel.send("That Funky Monkey")
        except Exception as e:
            print(e)
            
    @client.command(name = "squidtime")    
    async def squidtime(ctx):
        if len(voice_clients) == 0:
            await play(ctx, link = "https://youtu.be/zFdwr3jZs7Q?si=rYph9szmtN7kl83Y")
        else:
            await queue(ctx, url = "https://youtu.be/zFdwr3jZs7Q?si=rYph9szmtN7kl83Y")
    
    @client.command(name = "chimpsahoy")    
    async def chimps(ctx):
        if len(voice_clients) == 0:
            await play(ctx, link = "https://youtu.be/OBBD0XDrKlI?si=5wTv98Xfv9HwCfes")
        else:
            await queue(ctx, url = "https://youtu.be/OBBD0XDrKlI?si=5wTv98Xfv9HwCfes")
            
    
            
    @client.command(name = "queue")
    async def queue(ctx, url):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(url)
        await ctx.channel.send("Monk threw it in the queue")
        # await ctx.channel.send(f"Current queue is {queues[ctx.guild.id]}")
        
    @client.command(name = "queueis")
    async def queueis(ctx):
        await ctx.channel.send(f"Current queue is {queues[ctx.guild.id]}")
    
