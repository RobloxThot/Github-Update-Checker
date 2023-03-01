botToken = "x.x.x"
channelId = 0
url = "https://github.com/a/b"

import requests
import discord
import time
from discord.ext import tasks, commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!?",intents=intents)

old = "(Bot/server was reset)"

def getCommitHash():
	response = requests.get(url)
	for line in response.text.split("\n"):
		if "commit" in line and "fragment" in line:
			commit = line.split("/")[4].split('"')[0]
			return commit

def getCommitMsg():
	response = requests.get(url)
	for line in response.text.split("\n"):
		if "commit-tease-commit-message" in line:
			commitMsg = line.split(">")[1].split("<")[0]
			return commitMsg

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="Looking for update :eyes:"))
	print("Bot is ready!")
	await my_loop.start()

@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

# @client.command(pass_context=True)
# @commands.has_role("Friends")
# async def cum(ctx):
# 	await ctx.send("Onii-Chan Don't Cum Inside Kyaa~😊")

@tasks.loop(seconds=60)
async def my_loop():
	global b,old
	time.sleep(10)
	print("Checking...")
	fullHash = getCommitHash()
	new = getCommitHash()[:7]
	if new != old:
		print("New update hash: ",fullHash)
		channel = client.get_channel(channelId)
		embed = discord.Embed(title="Repo updated:", description= "", color=0x7289da)
		embed.add_field(name="Old Commit", value="``"+old+"``", inline=True)
		embed.add_field(name="Last Commit", value="``"+new+"``", inline=True)
		embed.add_field(name="Commit msg", value="``"+getCommitMsg()+"``",inline=False)
		embed.add_field(name="Commit changes", value=f'[Link](https://github.com/7GrandDadPGN/VapeV4ForRoblox/commit/{fullHash})')
		old = new
		await channel.send(embed=embed)
	else:
		print("Nothin new")

@my_loop.before_loop
async def before_some_task():
  await client.wait_until_ready()



client.run(botToken)
#pyinstaller --clean --onefile --key "peepeepoopoo" main.py
