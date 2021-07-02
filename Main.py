import discord
import json
from discord.ext import commands, tasks
import random
import datetime
import asyncio
import re
from config import *
from datetime import datetime, timedelta
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents()
intents.all()

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True,intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

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
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'l.help')) #(f'LATTE Online : {len(client.guilds)-1} Server')) 
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

@client.command(name='avatar')
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url

    embed = discord.Embed(title = f"{member.name}'s avatar", color = 0xc4cfcf)
    embed.set_image(url = userAvatar) # Shows the avatar
    embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)


""" ------------ Moderator commands ------------ """

@client.command(description="ban member")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    try:
        await member.ban(reason=reason)
        await ctx.message.delete()
        await ctx.channel.send(f'{member.name} has been banned from server'
                               f'Reason: {reason}')
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission to ban someone. Upgrade the Permissions")

@client.command(description="unban member")
@commands.has_permissions(kick_members=True)
async def unban(ctx, *,member):
    banner_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

@client.command(description="kick member")
@commands.has_permissions(kick_members=True)
async def kick(self, ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been Kicked')

@client.command(pass_context=True,description="clear message")
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) + 1))

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
#
    mutedRole = discord.utils.get(ctx.guild.roles, name="୭ muted ୭") 

    if not mutedRole:
        muteRole = await guild.create_role(name="୭ muted ୭")

        for channel in guild.channels:
            await chennel.set_permission(mureRole, speak=False, send_messages=False, read_message=False) # when don't have role muted

    embed = discord.Embed(title='Muted')
    await ctx.send (embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f'you have beed muted for {ctx.guild.name} Reason: {reason} ')

@client.command()
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="୭ muted ୭")

    await member.remove_roles(mutedRole)

@client.command()
async def tick(ctx, member: discord.Member, reason=None):
    await ctx.send("Please specify a Member! | `tick member reason`")
    
    if reason == None:
        return await ctx.send('Please specify a Reason! | `tick member reason`')

    embed = discord.Embed(title="เอาไป 1 ติ๊ก",color=0xFFFFFF,timestamp=datetime.utcnow())
    embed.set_footer(text=f'สาเหตุ : {reason}')
    await member.send(embed=embed)

@client.command(aliases='sv')
async def servers(ctx):
    embed = discord.Embed(title=f"**SERVER COUNT**",description=f"♡ ꒷ Bot is online **{len(client.guilds)-1}** servers︰𓂃 ꒱\n\n⸝⸝﹒[`invite bot link`](https://discord.com/api/oauth2/authorize?client_id=854134402954821643&permissions=8&scope=bot%20applications.commands) ꒱",color=0xFFFFFF,timestamp=datetime.utcnow())
    embed.set_footer(text=f'Req by {ctx.author}', icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_image(url=ctx.guild.banner_url)
    await ctx.send(embed=embed)

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

#    logchannel = ctx.guild.get_channel(channel id)  #
#    await logchannel.send(embed=logembed)

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color=discord.Color(0x6f2da8), # random color (color=discord.Color(random.randint(0x000000, 0xFFFFFF)),
                           title=f"LATTE GIVEAWAY", timestamp=futuredate,
                           description=f'React with 🎉 to enter!\nWinner(s) : **{winerscount}**\nHosted by: {ctx.author.mention}\n\n`{msg4.content}`\n')

    embed1.set_footer(text=f"Ends at")
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

    newEmbed = discord.Embed(title=f'🎉GIVEAWAY ENDED🎉',description=f'Winner(s) : **{winnerstosend}**\nHosted By :{ctx.author.mention}\n\n`{msg4.content}`\n', color=0x2f3136,timestamp=futuredate)
    newEmbed.set_footer(text=f'Ends at')

    win = await msg.edit(embed=newEmbed)
    await ctx.send(f"You won giveaway **{winnerstosend}** Please contact Host **{ctx.author.mention}**")

                                             
# Reroll command
@client.command()
@commands.has_permissions(manage_guild=True)
async def reroll(ctx):
    async for message in ctx.channel.history(limit=100, oldest_first=False):
        if message.author.id == client.user.id and message.embeds:
            reroll = await ctx.fetch_message(message.id)
            users = await reroll.reactions[0].users().flatten()
            users.pop(users.index(client.user))
            winner = random.choice(users)

            reEmbed = discord.Embed(title=f'🎉GIVEAWAY ENDED🎉',description=f'Winner(s) : {winner.mention}\nHosted By : {ctx.author.mention}\n', color=0x000001,timestamp=datetime.utcnow())
            reEmbed.set_footer(text=f'Ends at')
            
            await reroll.edit(embed=reEmbed)
            await ctx.send(f"You won giveaway **{winner.mention}** Please contact Host **{ctx.author.mention}**") #ctx.send(f"The new winner is {winner.mention}")
            break
    else:
        await ctx.send("No giveaways going on in this channel.")
        

""" --------- """

### Quick giveaways

@client.command()
@commands.has_permissions(administrator=True)
async def giveaways(ctx, prize=None, time=None):
    if prize == None:
        return await ctx.send('Please include a prize!')
    elif time == None:
        return await ctx.send('Please include a time!')   
    embed = discord.Embed(title=f'🎉 LATTE GIVEAWAY 🎉' ,description=f'react with 🎉 to enter!\nwinner: **1**\nHosted by: {ctx.author.mention}\n\n**{prize}**',color=0x9013FE,)
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

    newEmbed = discord.Embed(title=f'🎉 GIVEAWAY ENDED 🎉',description=f'Winner: {winners.mention}\nHosted By:{ctx.author.mention}', color=0x2f3136)
    newEmbed.set_footer(text=f'The giveaway has ended 🎉') 

    msg = await ctx.channel.fetch_message(gaw_msg.id)

    await msg.edit(embed = newEmbed)
    await ctx.send(f"You won giveaways **{winners.mention}** Please contact Host **{ctx.author.mention}**")


""" ------------ Events ------------ """


@client.event #member join alert
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="♢・welcome")
    if channel:
        embed=discord.Embed(
    description=f"ʚ˚̩̥̩ɞ ◟‧Welcome‧ *to* **{member.guild}!** <a:ab__purplestar:854958903656710144>\n　。\nෆ ₊˚don’t forget to check out . . .\n\n‧˚₊ ପ <:a_pink_dot:860493678723072000>︰<#840380566862823425> ଓ ♡ ˖˚˳\n♡ ꒷ get cute roles~︰𓂃 ꒱\n\n⸝⸝﹒{member.mention} ꒱ <a:S_wtfemoji:860490611048054845>", #⊹₊˚**‧Welcome‧**˚₊⊹ 
    timestamp=datetime.utcnow(),
    color=0xc4cfcf
    
    )
    embed.set_author(name=f"{member}", icon_url=member.avatar_url), 
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"You're our {member.guild.member_count} members ෆ"),

    await channel.send(embed=embed) #(content=f"||{member.mention}||", embed=embed) 

##@client.event  // auto role
##async def on_member_join(member):
##  role = get(member.guild.roles, id=role_id)
##  await member.add_roles(role)


@client.event #leave join alert
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="╰╮leave﹕₊")
    if channel:
        embed = discord.Embed(
            description=f"**See ya good bye\n`{member}`**",
            color=0xdbd7d2)
        embed.set_footer(text="—・𝗁𝗈𝗉𝖾 𝗒𝗈𝗎 𝖾𝗇𝗃𝗈𝗒𝖾𝖽 𝗒𝗈𝗎𝗋 𝗌𝗍𝖺𝗒")
        embed.timestamp = datetime.utcnow()

    await channel.send(embed = embed) 


#    await channel.send(f"{member} has left the server")

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

client.run(TOKEN, bot=True, reconnect=True)
