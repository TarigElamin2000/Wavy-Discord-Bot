from reddit_bot import reddit
from Token import Token 
import discord
from discord.ext import commands



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)


    

@bot.event
async def on_guild_join(guild):
    # create a discord channel and display all the mapped voice_channels
    mapping(guild.voice_channels)

# helper function that maps all voice_channels to number
mapped_vocie_channels = {}



# the function simply maps voice_channels to number 
def mapping(voice_channels:list):
    for num in range(len(voice_channels)):
        mapped_vocie_channels[num] = voice_channels[num]
    return " Done "

# the helper function simply changes the key of the voice_channel
# to a string set by the user
def set_voice_channel_key (key_:int,voice_channel_name:str):
    if key_ in mapped_vocie_channels.keys():
        voice_channel = mapped_vocie_channels[key_]
        del mapped_vocie_channels[key_]
        mapped_vocie_channels[voice_channel_name] = voice_channel
        return True
    else:
        return False
    
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

    channel_name = arg[0]
    channel_ = await ctx.guild.create_text_channel(channel_name, category=category_)
    await channel_.send(f'Bot created the {channel_.name}')
    


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

# the command displays all the mapped voice_channels in guild
# return a formated string 
@bot.command()
async def Display_Vc_name(ctx):
    # a string variable to print put keys and values of voice_channels to the user to be set by the user
    formated_voice_channel_name =""
    for key,value in mapped_vocie_channels.items():
        formated_voice_channel_name += f'\nchannel key: {key} ---> Channel name is: {value.name}.\n'
    
    formated_voice_channel_name += "\n You can change the Key of the voice channel use $Ckey channel_current_key channel_name. \n"
    await ctx.send(formated_voice_channel_name)

# the command takes the channel current key the name to be set 

@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def Ckey(ctx,*massege):
    
    massege = list(massege)
    channel_name = massege.pop()
    channel_key = massege.pop()      

    if set_voice_channel_key(int(channel_key),channel_name):
        await ctx.send(" channel name has been changed ")
    else:
        await ctx.send(" key is not found... ")


    

# the command enables the user to move other user between channels 
@bot.command()
@commands.has_guild_permissions(move_members=True)
async def move(ctx,*members):
    members = list(members)
    channel_key = members.pop()

    # turn string of name members to object memebrs
    for i in range(len(members)):
        members[i] = discord.utils.get(ctx.guild.members,mention=members[i])
    
    # move members to spacifiyed channel 
    for member in members:
        if not member:
            await ctx.send(f'{member} is regonized as a member in the server')
        else:
            await member.move_to(mapped_vocie_channels[int(channel_key)],reason=None)



# retrives certine posts from reddit accodring to the user
# search_reddit seach_terms

@bot.command()
async def search_reddit(ctx, *search_terms):
    # Join the search terms into a string with spaces
    search_query = " ".join(search_terms)

    # Ask the user for the number of posts to return
    await ctx.send("How many search results would you like to see? (1-10)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    
    msg = await bot.wait_for("message", timeout=10.0, check=check)
    if not msg:
        await ctx.send("You took too long to respond.")
        return
    try:
        num_posts = int(msg.content)
    except Exception as e:
        await ctx.send(f"Invalid number of search results specified.")

        return
    if num_posts < 1 or num_posts > 10:
        await ctx.send("Invalid number of search results specified. Please enter a number between 1 and 10.")
        return

    # Search for posts in all subreddits matching the search query
    try:
        results = reddit.subreddit("all").search(search_query, limit=num_posts)
    except Exception as e:
        await ctx.send(f"An error occurred while searching: {e}")
        return
    
    # Display the titles and URLs of the search results
    if results:
        #save all the posts in a array
        posts = []
        for submission in results:
            # Format the post title in bold and the URL in monospace font
            post = f"\n**{submission.title}\n**\n{submission.url}\n"
            posts.append(post)

        for pst in posts:
            # Send the formatted post title and URL to the channel
            await ctx.send(pst)
    else:
        await ctx.send(f"No search results found for '{search_query}'")





bot.run(Token)