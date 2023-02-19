import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is ready :)')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(error)


# Creating a channel
# $crt_TextChl nameOfTheChannel Categorie( optional ) 
# Discribtion : the function creates a Channel 

@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def crt_textChl(ctx,*arg):
    
    category_name = " ".join(arg[1:]).title()
    categories_list = ctx.guild.categories 
    category_ = discord.utils.get(categories_list, name=category_name)

    if category_:
        channel_name = arg[0]
        channel_ = await ctx.guild.create_text_channel(channel_name, category=category_)
        await channel_.send(f'Bot created the {channel_.name}')
    else:
        await ctx.send("Category is not found :(")



# deleting a channel
# $del_TextChl nameOfTheChannel 
# Discribtion : the function deletes a channel, if not found return a string 

@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def del_textChl(ctx,arg):
    channel_name = arg
    textChannels_list = ctx.guild.text_channels
    channel_ = discord.utils.get(textChannels_list, name=channel_name)

    if not channel_:
        await ctx.send("Channel is not found :(")
    else:    
        await channel_.delete(reason=None)
        await ctx.send("Channel is deleted")


# kicking a member out of the guild
# $kick @member

@bot.command()
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx,arg):
    all_members = ctx.guild.members
    kicked_member = discord.utils.get(all_members,mention=arg)

    if kicked_member:
        await kicked_member.kick()
        await ctx.send(f'{kicked_member.name} is kicked')
    else:
        await ctx.send("Member is not found :(")

# muting all members in a channel
# $mute_all
# all members in a current voice cahnnel are muted
    
@bot.command()
@commands.has_guild_permissions(mute_members=True)
async def mute_all(ctx):
    voice_state = ctx.author.voice
    if voice_state:
        members = voice_state.channel.members
        for member in members:
            if member != ctx.author:    
                await member.edit(mute=True)
        await ctx.send("All members have been muted.")
    else:
        await ctx.send("You must be in a voice channel to use this command.")

# unmuting all members in a channel
# $unmute_all
# all members in a current voice cahnnel are unmuted

@bot.command()
@commands.has_guild_permissions(mute_members=True)
async def unmute_all(ctx):
    voice_state = ctx.author.voice
    if voice_state:
        members = voice_state.channel.members
        for member in members:
            await member.edit(mute=False)
        await ctx.send("All members have been unmuted.")
    else:
        await ctx.send("You must be in a voice channel to use this command.")

# mute a spcifed members
# mute @member @member @member
# all members that are spcifyed are muted

@bot.command()
@commands.has_guild_permissions(mute_members=True)
async def mute(ctx,*members_):
    members_ = list(members_)
    members_in_VC = ctx.channel.members
    for i in range(len(members_)):
        copy_member = members_[i]
        members_[i] =  discord.utils.get(members_in_VC,mention=members_[i])
        if members_[i]:
            await members_[i].edit(mute=True)
            await ctx.send(f'{members_[i].name} is muted :) ')
        else:
            await ctx.send(f'member with the name {copy_member} is not found :[')

# unmute a spcifed members
# unmute @member @member @member
# all members that are spcifyed are unmuted

@bot.command()
@commands.has_guild_permissions(mute_members=True)
async def unmute(ctx,*members_):
    members_ = list(members_)
    members_in_VC = ctx.channel.members
    for i in range(len(members_)):
        copy_member = members_[i]
        members_[i] =  discord.utils.get(members_in_VC,mention=members_[i])
        if members_[i]:
            await members_[i].edit(mute=False)
            await ctx.send(f'{members_[i].name} is unmuted :) ')
        else:
            await ctx.send(f'member with the name {copy_member} is not found :[')





bot.run(os.getenv('Token'))