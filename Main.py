import discord
import json
from discord.ext import commands, tasks
import random
import datetime
import asyncio
from datetime import datetime, timedelta
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents()
intents.all()

client = commands.Bot(command_prefix="l.",intents=discord.Intents.all())
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



def convert(time):
    pos = ["s","m","h","d"]

    time_detect = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_detect[unit]


@client.command()
#@commands.has_permissions(administrator=True)
async def giveaways(ctx):
    await ctx.send("let")

    questions = {"test1",
                 "test2",
                 "test3"}

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('test4\'ddad')
            return
        else:
            answers.append(msg.content)

    
    try:
        c_id = int(answers[0][2:-1])
    except: 
        await ctx.send('test4')
        return


    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"test5")
        return
    elif time == -2:
        await ctx.send(f"test6")

    prize = answers[2]

    embed = discord.Embed(title=f'test' ,description=f'react with 🎉 to enter!\n<a:giveawayhost:859660981101395968>winner\n<:S_CuteGWave:859660564996816907>Hosted by: {ctx.author.mention}\n\n**{prize}**',color=0x9013FE,)
    embed.set_footer(text=f'Ends at •{answers[1]}')

    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    newEmbed = discord.Embed(title=f'{winner}',description=f'Winner: {winner.mention}\nHosted By:{ctx.author.mention}', color=0x000001 )
    newEmbed.set_footer(text=f'The giveaway has ended 🎉') 

    msg = await ctx.channel.fetch_message(my_msg.id)

    await msg.edit(embed = newEmbed)
    await ctx.send(f'your won giveaway {winner}')


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
