import os
import discord
from discord.ext import commands

# Mengambil Token dari Environment Variable
TOKEN = os.environ.get('TOKEN')

# Mengatur Intent
intents = discord.Intents.default()
intents.message_content = True

# Inisialisasi Bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot berhasil login sebagai {bot.user}')

# Command !ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command !join (Untuk masuk voice channel)
@bot.command()
async def join(ctx):
    # Cek apakah user yang ngetik sedang di voice channel
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        
        # Jika bot sudah di voice channel, pindah ke channel user
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await ctx.send(f"Bot pindah ke channel **{channel.name}**")
        else:
            # Bot masuk ke voice channel
            await channel.connect()
            await ctx.send(f"Bot berhasil masuk ke **{channel.name}**")
    else:
        await ctx.send("Kamu tidak berada di voice channel! Masuk dulu baru panggil bot.")

# Command !leave (Untuk keluar voice channel)
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
