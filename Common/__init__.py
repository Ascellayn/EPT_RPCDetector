from TSN_Abstracter import *;

import asyncio;
import discord;
from discord import app_commands;
from discord.ext import commands, tasks;

BOT: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=discord.Intents.all(), help_command=None);



class RPCd_JSON_ID(TypedDict):
	Guild: int;
	Channel: int;

class RPCd_JSON(TypedDict):
	Debug: bool;
	Active: bool;
	Cooldown: int;
	ID: RPCd_JSON_ID
	Whitelist: list[int];
	Checklist: list[int];

Cfg: RPCd_JSON = cast(RPCd_JSON, File.JSON_Read("Config.json"));
if (Cfg == {}):
	Cfg = {
		"Debug": False,
		"Active": True,
		"Cooldown": 300,
		"ID": {
			"Guild": -1,
			"Channel": -1
		},
		"Whitelist": [],
		"Checklist": [-1]
	};
	File.JSON_Write("Config.json", Cfg);
	raise Exception("Please configure the ID entries in Config.json");

DEBUG: bool = Cfg["Debug"];









""" Miscellaneous Functions (Discordpy) """
def Color_Tuple(Color: tuple[int, int, int]) -> discord.Color:
	""" Converts a tuple (preferably from TSN_Abstractor/TSNDL.[COLOR]) and returns a discord.Color object."""
	return discord.Color.from_rgb(Color[0], Color[1], Color[2]);



""" RPCd Functions """
@commands.has_permissions(administrator=True)
async def Signal(A: discord.Activity, U: discord.Member) -> None:
	C: discord.Thread | None = cast(discord.Thread | None, BOT.get_channel(Cfg["ID"]["Channel"]));
	if (not C): raise Exception(f"Unable to acquire Channel ID \"{Cfg['ID']['Channel']}\"");

	PLATFORM: str = A.platform.capitalize() if A.platform else "[Unknown]";
	DETAILS: str = ":\n" + A.details if (A.details) else "";

	await C.send(
		embed=discord.Embed(
			color=Color_Tuple(TSNDL.Color.Sun.Red),
			description=f"### <@{U.id}> ({U.name}) is playing \"{A.name}\"\n**Platform: {PLATFORM}**{DETAILS}"
		).set_thumbnail(url=U.avatar)
	);