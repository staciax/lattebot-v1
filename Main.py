import discord
import json
from discord.ext import commands, tasks
import random
import datetime
import asyncio
import re
from datetime import datetime, timedelta
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents()
intents.all()

client = commands.Bot(command_prefix="l.", case_insensitive=True,intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

# seconds passed since epoch

## login , status , ping

@slash.slash(description="show the bots latency") #example slash command
async def ping(ctx):
    embed=discord.Embed(description=(f'`{round(client.latency * 1000)} ms`'))
    await ctx.send(embed=embed)

"""

@slash.slash(name="test")
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])

## example slash commands

""" 
"""------------ Example commands , event ------------ """

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('✧ LATTE BOT.'))
    print(f"we have logged in as {client.user}")

@client.command()
async def ping(ctx):
    embed=discord.Embed(description=(f'`{round(client.latency * 1000)} ms`'))
    await ctx.send(embed=embed)

@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")

""" ------------ Info commands ------------ """

@client.command(name="userinfo")
async def user_info(Ctx, *, user: discord.User = None):
	if user is None:
		user = Ctx.author

	header = f"User information - {user.display_name}\n\n"
	rows = {
		"Account name"     : user.name,
		"Disciminiator"    : user.discriminator,
		"ID"               : user.id,
		"Is bot"           : "Yes" if user.bot else "No",
		"Top role"         : user.top_role,
		"Nº of roles"      : len(user.roles),
		"Current status"   : str(user.status).title(),
		"Current activity" : f"{str(user.activity.type).title().split('.')[1]} {user.activity.name}" if user.activity is not None else "None",
		"Created at"       : user.created_at.strftime("%d/%m/%Y %H:%M:%S"),
		"Joined at"        : user.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
        "You are our"      : str(sorted(Ctx.guild.members, key=lambda m: m.joined_at).index(user)+1),
        
	}
	table = header + "\n".join([f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
	await Ctx.send(f"```{table}```") #await Ctx.send(f"```{table}```{user.avatar_url}")
	return


@client.command(name="serverinfo")
async def guild_info(Ctx):
	"""Displays server information."""
	header = f"Server information - {Ctx.guild.name}\n\n"
	rows = {
		"Name"                  : Ctx.guild.name,
		"ID"                    : Ctx.guild.id,
		"Region"                : str(Ctx.guild.region).title(),
		"Owner"                 : Ctx.guild.owner.display_name,
		"Shard ID"              : Ctx.guild.shard_id,
		"Created on"            : Ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S"),
		"joined"                : max([Member.joined_at for Member in Ctx.guild.members]).strftime("%d/%m/%y %H:%M:%S"),
		"Members with bots"     : Ctx.guild.member_count,
		"Members"               : len([member for member in Ctx.guild.members if not member.bot]),
		"Bots"                  : len([Member for Member in Ctx.guild.members if Member.bot]),   
		"categories"            : len(Ctx.guild.categories),
		"text channels"         : len(Ctx.guild.text_channels),
		"voice channels"        : len(Ctx.guild.voice_channels),
		"roles"                 : len(Ctx.guild.roles),
		"Banned members"        : len(await Ctx.guild.bans()),
	    "Most recent member"    : [Member for Member in Ctx.guild.members if Member.joined_at is max([Member.joined_at for Member in Ctx.guild.members])][0].display_name,          
		"invite link"           : len(await Ctx.guild.invites()),
# 
#    
	}
	table = header + "\n".join([f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
	await Ctx.send(f"```{table}```") ##	await Ctx.send(f"```{table}```{Ctx.guild.icon_url}
	return

## server info slash

@slash.slash(description="show server info") 
async def guild_info(Ctx):
	"""Displays server information."""
	header = f"Server information - {Ctx.guild.name}\n\n"
	rows = {
		"Name"                  : Ctx.guild.name,
		"ID"                    : Ctx.guild.id,
		"Region"                : str(Ctx.guild.region).title(),
		"Owner"                 : Ctx.guild.owner.display_name,
		"Shard ID"              : Ctx.guild.shard_id,
		"Created on"            : Ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S"),
		"joined"                : max([Member.joined_at for Member in Ctx.guild.members]).strftime("%d/%m/%y %H:%M:%S"),
		"Members with bots"     : Ctx.guild.member_count,
		"Members"               : len([member for member in Ctx.guild.members if not member.bot]),
		"Bots"                  : len([Member for Member in Ctx.guild.members if Member.bot]),   
		"categories"            : len(Ctx.guild.categories),
		"text channels"         : len(Ctx.guild.text_channels),
		"voice channels"        : len(Ctx.guild.voice_channels),
		"roles"                 : len(Ctx.guild.roles),
		"Banned members"        : len(await Ctx.guild.bans()),
	    "Most recent member"    : [Member for Member in Ctx.guild.members if Member.joined_at is max([Member.joined_at for Member in Ctx.guild.members])][0].display_name,         
		"invite link"           : len(await Ctx.guild.invites()),
# 
#    
	}
	table = header + "\n".join([f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
	await Ctx.send(f"```{table}```") ##	await Ctx.send(f"```{table}```{Ctx.guild.icon_url}
	return



""" ------------ Commands ------------ """

@client.remove_command("help") ## remove defaul hlep
@client.command(name="help")
async def help(Ctx):
    embed=discord.Embed(
    title=f"ยินดีต้อนรับเข้าสู่เซิฟเวอร์ ✧ LATTE.", 
    description=f"Thanks for joining!",
    timestamp=datetime.utcnow(),
    color=0xc4cfcf
) 
    embed.set_thumbnail(url=Ctx.guild.icon_url)

    await Ctx.channel.send(embed=embed)

@client.command(name='avatar', help='fetch avatar of a user')
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url

    embed = discord.Embed(title = f"{member.name}'s avatar", color = 0xc4cfcf)
    embed.set_image(url = userAvatar) # Shows the avatar
    embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)


""" ------------ Moderator commands ------------ """

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been Banned')

@client.command()
@commands.has_permissions(kick_members=True)
async def unban(ctx, *,member):
    banner_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(self, ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been Kicked')

@client.command(pass_context=True)
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) + 1))

""" ------------ Giveaways ------------ """

@client.command(aliases=['start', 'g'])
async def giveaway(ctx):
    await ctx.send("Select the channel, you would like the giveaway to be in.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg1 = await client.wait_for('message', check=check, timeout=30.0)

        channel_converter = discord.ext.commands.TextChannelConverter()
        try:
            giveawaychannel = await channel_converter.convert(ctx, msg1.content)
        except commands.BadArgument:
            return await ctx.send("This channel doesn't exist, please try again.")

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")

    if not giveawaychannel.permissions_for(ctx.guild.me).send_messages or not giveawaychannel.permissions_for(
            ctx.guild.me).add_reactions:
        return await ctx.send(
            f"Bot does not have correct permissions to send in: {giveawaychannel}\n **Permissions needed:** ``Add reactions | Send messages.``")

    await ctx.send("How many winners to the giveaway would you like?")
    try:
        msg2 = await client.wait_for('message', check=check, timeout=30.0)
        try:
            winerscount = int(msg2.content)
        except ValueError:
            return await ctx.send("You didn't specify a number of winners, please try again.")

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")

    await ctx.send("Select an amount of time for the giveaway.")
    try:
        since = await client.wait_for('message', check=check, timeout=30.0)

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")

    seconds = ("s", "sec", "secs", 'second', "seconds")
    minutes = ("m", "min", "mins", "minute", "minutes")
    hours = ("h", "hour", "hours")
    days = ("d", "day", "days")
    weeks = ("w", "week", "weeks")
    rawsince = since.content

    try:
        temp = re.compile("([0-9]+)([a-zA-Z]+)")
        if not temp.match(since.content):
            return await ctx.send("You did not specify a unit of time, please try again.")
        res = temp.match(since.content).groups()
        time = int(res[0])
        since = res[1]

    except ValueError:
        return await ctx.send("You did not specify a unit of time, please try again.")

    if since.lower() in seconds:
        timewait = time
    elif since.lower() in minutes:
        timewait = time * 60
    elif since.lower() in hours:
        timewait = time * 3600
    elif since.lower() in days:
        timewait = time * 86400
    elif since.lower() in weeks:
        timewait = time * 604800
    else:

        return await ctx.send("You did not specify a unit of time, please try again.")

    await ctx.send("What would you like the prize to be?")
    try:
        msg4 = await client.wait_for('message', check=check, timeout=30.0)

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again.")

#    logembed = discord.Embed(title="Giveaway Logged",
#                             description=f"**Prize:** ``{msg4.content}``\n**Winners:** ``{winerscount}``\n**Channel:** {giveawaychannel.mention}\n**Host:** {ctx.author.mention}",
#                             color=discord.Color.red())
#    logembed.set_thumbnail(url=ctx.author.avatar_url)

#    logchannel = ctx.guild.get_channel(859789105507598346)  # Put your channel, you would like to send giveaway logs to.
#    await logchannel.send(embed=logembed)

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color=discord.Color(random.randint(0x000000, 0xFFFFFF)),
                           title=f"🎉GIVEAWAY🎉\n`{msg4.content}`", timestamp=futuredate,
                           description=f'React with 🎉 to enter!\nHosted by: {ctx.author.mention}')

    embed1.set_footer(text=f"Giveaway will end")
    msg = await giveawaychannel.send(embed=embed1)
    await msg.add_reaction("🎉")
    await asyncio.sleep(timewait)
    message = await giveawaychannel.fetch_message(msg.id)
    for reaction in message.reactions:
        if str(reaction.emoji) == "🎉":
            users = await reaction.users().flatten()
            if len(users) == 1:
                return await msg.edit(embed=discord.Embed(title="Nobody has won the giveaway."))
    try:
        winners = random.sample([user for user in users if not user.bot], k=winerscount)
    except ValueError:
        return await giveawaychannel.send("not enough participants")
    winnerstosend = "\n".join([winner.mention for winner in winners])

    win = await msg.edit(embed=discord.Embed(title="WINNER",
                                             description=f"Congratulations {winnerstosend}, you have won **{msg4.content}**!",
                                             color=discord.Color.blue()))

                                             
# Reroll command, used for chosing a new random winner in the giveaway
@client.command()
@commands.has_permissions(manage_guild=True)
async def reroll(ctx):
    async for message in ctx.channel.history(limit=100, oldest_first=False):
        if message.author.id == client.user.id and message.embeds:
            reroll = await ctx.fetch_message(message.id)
            users = await reroll.reactions[0].users().flatten()
            users.pop(users.index(client.user))
            winner = random.choice(users)
            await ctx.send(f"The new winner is {winner.mention}")
            break
    else:
        await ctx.send("No giveaways going on in this channel.")

""" --------- """
"""
@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, title=None, winner=None, prize=None, time=None):
    if title == None:
        return await ctx.send('Please include a Title!')
    elif winner == None:
        return await ctx.send('Please include a winner!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    elif time == None:
        return await ctx.send('Please include a time!')
    embed = discord.Embed(title=f'{title}' ,description=f'react with 🎉 to enter!\nwinner**{winner}**\nHosted by: {ctx.author.mention}\n\n**{prize}**',color=0x9013FE,)
    time_convert = {"s":1, "m":60, "h":3600, "d":86400}
    gawtime =int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f'React with 🎉 to enter • Ends at • {time}')
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winners = random.choice(users)

    newEmbed = discord.Embed(title=f'{title}',description=f'Winner: {winners.mention}\nHosted By:{ctx.author.mention}', color=0x000001 )
    newEmbed.set_footer(text=f'The giveaway has ended 🎉') 

    msg = await ctx.channel.fetch_message(gaw_msg.id)

    await msg.edit(embed = newEmbed)
    await ctx.send("wtf is that")

"""


""" ------------ Events ------------ """


@client.event #member join alert
async def on_member_join(member):
    channel = client.get_channel(844462710526836756) #id test-bot
    embed=discord.Embed(
    description=f"⊹₊˚**‧Welcome‧**˚₊⊹ \nʚ˚̩̥̩ɞ ◟*to* **{member.guild}!** <a:ab__purplestar:854958903656710144> \n　。\nෆ ₊˚don’t forget to check out . . .", #⊹₊˚**‧Welcome‧**˚₊⊹ 
    timestamp=datetime.utcnow(),
    color=0xc4cfcf
    
    )
    embed.set_author(name=f"{member}", icon_url=member.avatar_url), 
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"You're our {member.guild.member_count} members ෆ"),

    await channel.send(content=f"||{member.mention}||", embed=embed) 

@client.event #leave join alert
async def on_member_remove(member):
    channel = client.get_channel(858680947272581131)
    await channel.send(f"{member} has left the server")

""" ------------ custom reaction role ------------ """

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    
@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(title="REACT GET ROLE", description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

""" ------------ TOKEN ------------ """

client.run('ODU0MTM0NDAyOTU0ODIxNjQz.YMfgpg.nAFyoLIAJ3K0jLFLEp0AAkJ6s9k')
