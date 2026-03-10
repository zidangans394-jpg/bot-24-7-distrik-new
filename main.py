import os
import discord
from discord.ext import commands

# Mengambil Token dari Environment Variable
TOKEN = os.environ.get('TOKEN')

# MASUKKAN ID VOICE CHANNEL DISINI
VOICE_CHANNEL_ID = 1368851076408672337

# Mengatur Intent
intents = discord.Intents.default()
intents.message_content = True

# Inisialisasi Bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot berhasil login sebagai {bot.user}')

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel:
        try:
            if not bot.voice_clients:
                await channel.connect()
                print("Bot auto join voice channel")
        except Exception as e:
            print("Gagal auto join:", e)

# Command !ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command !join
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await ctx.send(f"Bot pindah ke channel **{channel.name}**")
        else:
            await channel.connect()
            await ctx.send(f"Bot berhasil masuk ke **{channel.name}**")
    else:
        await ctx.send("Kamu tidak berada di voice channel! Masuk dulu baru panggil bot.")

# Command !leave
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot keluar dari voice channel.")
    else:
        await ctx.send("Bot tidak ada di voice channel manapun.")

# Menjalankan bot
if TOKEN is None:
    print("ERROR: Token tidak ditemukan!")
else:
    bot.run(TOKEN)
