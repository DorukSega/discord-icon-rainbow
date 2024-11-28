import discord
import asyncio
import random
import json
from io import BytesIO
from PIL import Image

# CREATE secret.json with info
with open("secret.json", "r") as config_file:
    config = json.load(config_file)
    TOKEN = config["TOKEN"]
    GUILD_ID = config["GUILD_ID"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to create a solid color image
def create_color_image(color: tuple):
    img = Image.new("RGB", (512, 512), color)
    byte_arr = BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    return byte_arr

def generate_random_color():
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
            print(f"Changed icon to random color {random_color}")
        except discord.errors.HTTPException as e:
            print(f"Rate limited or another issue occurred: {e}")
            await asyncio.sleep(60)  # Wait a minute if rate-limited
        await asyncio.sleep(60)  # Change icon every 60 seconds

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await change_server_icon()

client.run(TOKEN)