import asyncio
import discord
import os
import sys
import time
import random
from pystyle import Colorate, Colors

tokenfile = "tokens.txt"
messagefile = "messages.txt"

BANNER = r"""
███████╗ ██████╗ ███╗   ██╗██████╗  ██████╗██╗   ██╗████████╗███████╗
██╔════╝██╔═══██╗████╗  ██║╚════██╗██╔════╝██║   ██║╚══██╔══╝██╔════╝
███████╗██║   ██║██╔██╗ ██║ █████╔╝██║     ██║   ██║   ██║   █████╗  
╚════██║██║   ██║██║╚██╗██║██╔═══╝ ██║     ██║   ██║   ██║   ██╔══╝  
███████║╚██████╔╝██║ ╚████║███████╗╚██████╗╚██████╔╝   ██║   ███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
"""

BLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"

def type_anim(text, delay=0.01):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Vertical(Colors.white_to_blue, BANNER))
    time.sleep(0.5)

def read_lines(name):
    possible = [
        os.path.join(os.getcwd(), name),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), name),
        os.path.expanduser(f"~/{name}")
    ]
    for path in possible:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
    print(f"{BLUE}[$]{RESET} can't find {WHITE}{name}{RESET}")
    return []

def mask_token(token, show=20):
    return f"{token[:show]}{'*' * max(0, len(token) - show)}"

def log(msg, token=None):
    prefix = f"{BLUE}[{WHITE}$]{RESET}"
    delay = random.uniform(0.02, 0.05)
    time.sleep(delay)
    if token:
        t = mask_token(token)
        print(f"{prefix} [{t}] {WHITE}{msg}{RESET}")
    else:
        print(f"{prefix} {WHITE}{msg}{RESET}")

async def send_dm(token, user_id, messages, idx):
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        log(f"bot {idx} logged in as {client.user.name}", token)
        try:
            user = await client.fetch_user(user_id)
            for msg in messages:
                await user.send(msg)
                log(f"sent dm | \"{msg}\"", token)
                await asyncio.sleep(random.uniform(1.2, 2.1))
            log("finished sending all messages", token)
        except Exception as e:
            log(f"error: {e}", token)
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        log(f"login failed: {e}", token)

async def send_channel(token, channel_id, messages, idx):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        log(f"bot {idx} logged in as {client.user.name}", token)
        try:
            channel = await client.fetch_channel(channel_id)
            for msg in messages:
                await channel.send(msg)
                log(f"sent to channel | \"{msg}\"", token)
                await asyncio.sleep(random.uniform(1.2, 2.0))
            log("done sending.", token)
        except Exception as e:
            log(f"error {e}", token)
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        log(f"login failed: {e}", token)

async def main():
    banner()
    tokens = read_lines(tokenfile)
    messages = read_lines(messagefile)

    type_anim(f"{BLUE}[{WHITE}+{BLUE}]{RESET} Loaded {len(tokens)} tokens.")
    type_anim(f"{BLUE}[{WHITE}+{BLUE}]{RESET} Loaded {len(messages)} messages.")
    print()

    if not tokens or not messages:
        type_anim(f"{BLUE}[$]{RESET} missing tokens or messages file.")
        return

    while True:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{BLUE}[01]{RESET} Send DM to user")
        print(f"{BLUE}[02]{RESET} Send to channel")
        print(f"{BLUE}[03]{RESET} Exit")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        choice = input(f"{BLUE}[$]{RESET} Choose option: ").strip()
        print()

        if choice == "1":
            try:
                user_id = int(input(f"{BLUE}[$]{RESET} user ID: ").strip())
            except ValueError:
                type_anim(f"{BLUE}[$]{RESET} Invalid user Id.")
                continue

            type_anim(f"{BLUE}[$]{RESET} Sending DMs using {len(tokens)} bots")
            await asyncio.gather(*(send_dm(token, user_id, messages, i + 1) for i, token in enumerate(tokens)))

        elif choice == "2":
            try:
                channel_id = int(input(f"{BLUE}[$]{RESET} channel ID: ").strip())
            except ValueError:
                type_anim(f"{BLUE}[$]{RESET} invalid channel ID.")
                continue

            type_anim(f"{BLUE}[$]{RESET} Sending messages using {len(tokens)} bot")
            await asyncio.gather(*(send_channel(token, channel_id, messages, i + 1) for i, token in enumerate(tokens)))

        elif choice == "3":
            type_anim(f"{BLUE}[$]{RESET} bye bye")
            sys.exit(0)

        else:
            type_anim(f"{BLUE}[$]{RESET} not a valid choice.")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BLUE}[$]{RESET} Closing.")
        sys.exit(0)

