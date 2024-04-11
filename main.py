import discord
from discord.ext import commands
import json
import asyncio

# Initialize bot
intents = discord.Intents.all()
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

EMPTY_CHANNEL_TIMEOUT = 15

# Your Discord Token
TOKEN = 'MTIyNzY0MDExNzcxNjQ1MTM2OA.GzIRt_.Uyk44702Z3GfZpiC4f4Kpz_242Gv-syhgT-Uqk'


# Dictionary to map emoji IDs to role names
emoji_to_role = {
    '🍎': 'NA-East',
    '🍐': 'NA-West',
    '🍏': 'NA-Central',
    '🐙': 'UK',
    '👀': 'EU',
    '🦘': 'AUS',
    '🧠': 'Zombies',
    '✅': 'Gamer',
    '🔫': 'Rust'
    # Add more emoji-role mappings here
}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

allowed_channel_id = 1227856602065797120

@bot.command()
async def lfg(ctx, map_name = None, players_needed = None, steam_id = None):
    # Check if the command is executed in the allowed channel
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Sorry, this command can only be executed in a specific channel.")
        return
    
        # Check if all arguments are provided
    if map_name is None or players_needed is None or steam_id is None:
        await ctx.send("Please use the format !lfg <map_name> <players_needed> <steamid>.")
        return

    
    # Formulate the message with the provided arguments
    message = f">>> ```**Looking for group:**\nMap: {map_name}\nPlayers Needed: {players_needed}\nSteam ID: {steam_id}```"
    
    # Reply to the sender of the command in the same channel
    await ctx.send(f"{ctx.author.mention}, {message}")



@bot.event
async def on_raw_reaction_add(payload):
    # Get the message and the emoji
    message_id = payload.message_id
    guild_id = payload.guild_id
    emoji = payload.emoji.name

    # Check if the reaction is on the specific message you want to handle
    if message_id == 1227653946781470831:
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if guild is not None:
            role_name = emoji_to_role.get(emoji)
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role is not None:
                    member = guild.get_member(payload.user_id)
                    await member.add_roles(role, reason="Reaction Role")
                    print(f'{member.name} has been given the role {role_name}')

        # Check if the reaction is on the specific message you want to handle
    if message_id == 1227792727178215434:
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if guild is not None:
            role_name = emoji_to_role.get(emoji)
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role is not None:
                    member = guild.get_member(payload.user_id)
                    await member.add_roles(role, reason="Reaction Role")
                    print(f'{member.name} has been given the role {role_name}')

@bot.event
async def on_raw_reaction_remove(payload):
    # Get the message and the emoji
    message_id = payload.message_id
    guild_id = payload.guild_id
    emoji = payload.emoji.name

    # Check if the reaction is on the specific message you want to handle
    if message_id == 1227653946781470831:
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if guild is not None:
            role_name = emoji_to_role.get(emoji)
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role is not None:
                    member = guild.get_member(payload.user_id)
                    await member.remove_roles(role, reason="Reaction Role Removed")
                    print(f'{member.name} has been removed from the role {role_name}')


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.channel.id == 1227864729595285524:
        guild = member.guild
        # Create a new voice channel with the name of the member
        new_channel = await guild.create_voice_channel(name=f"4p {member.name}", category=after.channel.category)
        await new_channel.edit(user_limit=4)
        
        # Define a task to delete the channel after 15 seconds if it's empty
        async def delete_channel():
            await asyncio.sleep(15)
            if len(new_channel.members) == 0:
                await new_channel.delete()

        # Move the member who triggered the creation of the new channel into it
        await member.move_to(new_channel)
        
        # Define a task to delete the channel after a certain period of inactivity
        async def delete_empty_channel():
            while True:
                await asyncio.sleep(EMPTY_CHANNEL_TIMEOUT)
                if len(new_channel.members) == 0:
                    await new_channel.delete()

        # Start the task to delete the channel when it's empty
        asyncio.create_task(delete_empty_channel())



# Run the bot
bot.run(TOKEN)