import discord
import json
from discord.ext import commands, tasks
import random
import datetime
import asyncio
from datetime import datetime
from discord_slash import SlashCommand

intents = discord.Intents()
intents.all()

client = commands.Bot(command_prefix="l.",intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


## login , status , ping

@slash.slash(description="show the bots latency") #example slash command
async def ping(ctx):
    embed=discord.Embed(description=(f'`{round(client.latency * 1000)} ms`'))
    await ctx.send(embed=embed)

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

#

## @client.command()
##async def ping(ctx):
##    await ctx.send(f'Ping : {round(client.latency * 1000)}ms')
## random massge

##@client.coomand







## commands

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
		"Members"               : Ctx.guild.member_count,
		"Members with out bot"  : len([member for member in Ctx.guild.members if not member.bot]),
		"Bots"                  : len([Member for Member in Ctx.guild.members if Member.bot]),   
		"categories"            : len(Ctx.guild.categories),
		"text channels"         : len(Ctx.guild.text_channels),
		"voice channels"        : len(Ctx.guild.voice_channels),
		"roles"                 : len(Ctx.guild.roles),
		"Banned members"        : len(await Ctx.guild.bans()),
	    "Most recent member"    : [Member for Member in Ctx.guild.members if Member.joined_at is max([Member.joined_at for Member in Ctx.guild.members])][0].display_name,
##		"...of which human"     : len([Member for Member in Ctx.guild.members if not Member.bot]),
##		"...of which bots"      : len([Member for Member in Ctx.guild.members if Member.bot]),           
##		"Nº of invites"         : len(await Ctx.guild.invites()),
# 
#    
	}
	table = header + "\n".join([f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
	await Ctx.send(f"```{table}```") ##	await Ctx.send(f"```{table}```{Ctx.guild.icon_url}
	return

@client.remove_command("help") ## turn of help 

## help custom

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

## mod commands

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

##

@client.command()
async def giveaway(ctx, title=None, winner=None, prize=None, time=None):
    if title == None:
        return await ctx.send('Please include a Title!')
    elif winner == None:
        return await ctx.send('Please include a winner!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    elif time == None:
        return await ctx.send('Please include a time!')
    embed = discord.Embed(title=f'{title}' ,description=f'react with 🎉 to enter!\n{winner} winner \nHosted by: {ctx.author.mention}\n\n**{prize}**',color=0x9013FE)
    time_convert = {"s":1, "m":60, "h":3600, "d": 86400}
    gawtime =int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f'React with 🎉 to enter • Ends at • {time}')  
    gaw_msg = await ctx.send(embed =embed)

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


## events

@client.event
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

#await bot.say(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)

#



@client.event
async def on_member_remove(member):
    channel = client.get_channel(858680947272581131)
    await channel.send(f"{member} has left the server")

## custom reaction role

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

## token

client.run('ODU0MTM0NDAyOTU0ODIxNjQz.YMfgpg.nAFyoLIAJ3K0jLFLEp0AAkJ6s9k')
