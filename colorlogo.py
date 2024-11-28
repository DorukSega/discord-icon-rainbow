import discord
import asyncio
import random
import json
import datetime
from io import BytesIO
from PIL import Image

# CREATE secret.json with info
with open("secret.json", "r") as config_file:
    config = json.load(config_file)
    TOKEN = config["TOKEN"]
    GUILD_ID = config["GUILD_ID"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def create_color_image(color: tuple):
    'Function to create a solid color image'
    img = Image.new("RGB", (512, 512), color)
    byte_arr = BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    return byte_arr


def generate_random_color(seed=None):
    if seed is None:
        # Use the current time down to microseconds for default seeding
        seed = int(datetime.datetime.now().timestamp() * 1_000_000)
    random.seed(seed)
    return tuple(random.randint(0, 255) for _ in range(3))


async def change_server_icon():
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found!")
        return

    while True:
        random_color = generate_random_color()
        image_data = create_color_image(random_color)
        try:
            await guild.edit(icon=image_data.read())
            current_time = datetime.datetime.now()
            print(f"Changed icon to random color {random_color} {current_time.hour}:{current_time.minute}:{current_time.second}")
        except discord.errors.HTTPException as e:
            print(f"Rate limited or another issue occurred: {e}")
            await asyncio.sleep(60)  # Wait a minute if rate-limited
        additional_wait = random.randint(0, 59)
        await asyncio.sleep(60 + additional_wait)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await change_server_icon()

client.run(TOKEN)
