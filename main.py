import os
import discord
from discord.ext import commands

# TOKEN dari Railway Environment
TOKEN = os.environ.get("TOKEN")

# GANTI DENGAN ID VOICE CHANNEL KAMU
VOICE_CHANNEL_ID = 1368851076408672337

# Intent
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# status untuk tahu apakah user pakai !leave
manual_disconnect = False


@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel:
        try:
            if not bot.voice_clients:
                await channel.connect(reconnect=True)
                print("Bot auto join voice channel")
        except Exception as e:
            print("Gagal auto join:", e)


@bot.event
async def on_voice_state_update(member, before, after):
    global manual_disconnect

    if member.id == bot.user.id:
        if after.channel is None and not manual_disconnect:
            print("Bot keluar dari VC, mencoba reconnect...")
            channel = bot.get_channel(VOICE_CHANNEL_ID)

            if channel:
                try:
                    await channel.connect(reconnect=True)
                    print("Reconnect berhasil")
                except Exception as e:
                    print("Reconnect gagal:", e)

        manual_disconnect = False


# COMMAND PING
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# COMMAND JOIN
@bot.command(name="masukvoice")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = ctx.voice_client

        try:
            if voice and voice.is_connected():
                await voice.move_to(channel)
                await ctx.send(f"Bot pindah ke **{channel.name}**")
            else:
                await channel.connect()
                await ctx.send(f"Bot masuk ke **{channel.name}**")
        except Exception as e:
            await ctx.send("Gagal join voice.")
            print("Join error:", e)
    else:
        await ctx.send("Masuk voice channel dulu.")


# COMMAND LEAVE
@bot.command(name="keluarvoice")
async def leave(ctx):
    global manual_disconnect

    voice = ctx.voice_client

    if voice and voice.is_connected():
        manual_disconnect = True
        await voice.disconnect()
        await ctx.send("Bot keluar dari voice channel.")
    else:
        await ctx.send("Bot tidak ada di voice channel.")


# START BOT
if TOKEN is None:
    print("ERROR: Token tidak ditemukan!")
else:
    bot.run(TOKEN)
