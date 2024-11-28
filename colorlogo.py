import discord
from asyncio import sleep
from random import seed, randint
from json import load
from datetime import datetime
from math import sqrt
from io import BytesIO
from PIL import Image

# CREATE secret.json with info
with open("secret.json", "r") as config_file:
    config = load(config_file)
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


def generate_random_color():
    nseed = int(datetime.now().timestamp() * 1_000_000)
    seed(nseed)
    return tuple(randint(0, 255) for _ in range(3))


def color_distance(color1, color2):
    """Calculate the Euclidean distance between two colors in RGB space."""
    return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def generate_random_color_distant(last_color=None, min_distance=150):
    nseed = int(datetime.now().timestamp() * 1_000_000)
    seed(nseed)
    while True:
        new_color = tuple(randint(0, 255) for _ in range(3))
        if last_color is None or color_distance(new_color, last_color) >= min_distance:
            return new_color


async def change_server_icon():
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found!")
        return

    last_color = generate_random_color()
    while True:
        new_color = generate_random_color_distant(last_color=last_color)
        last_color = new_color
        image_data = create_color_image(new_color)
        additional_wait = randint(0, 59)
        try:
            await guild.edit(icon=image_data.read())
            current_time = datetime.now()
            print(f"Changed to {new_color} {current_time.hour}:{current_time.minute}:{current_time.second}")
            print(f"Next in {60 + additional_wait} seconds")
        except discord.errors.HTTPException as e:
            print(f"Rate limited or another issue occurred: {e}")
            await sleep(600)
            continue
        await sleep(60 + additional_wait)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await change_server_icon()

client.run(TOKEN)
