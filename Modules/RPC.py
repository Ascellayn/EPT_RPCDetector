""" General Imports """
from Common import *;





async def Scan_Members() -> None:
	Log.Info(f"Checking...");
	G: discord.Guild | None = BOT.get_guild(Cfg["ID"]["Guild"]);
	if (not G): raise Exception(f"Guild not found: \"{Cfg["ID"]["Guild"]}\"");
	for m in G.members:
		if (not m.activities): continue;
		if (m.id in Cfg["Whitelist"]): continue;

		skip: bool = False if (-1 in Cfg["Checklist"]) else True;
		for r in m.roles:
			if (r.id in Cfg["Checklist"]): skip = False;
			if (r.id in Cfg["Whitelist"]): skip = True;
		if (m.id in Cfg["Checklist"]): skip = False;
		if (skip): continue;

		for a in m.activities:
			if (a.type == discord.ActivityType.playing and type(a) == discord.Activity):
				print(f"Found Activity by {m.name}: {a}");
				asyncio.create_task(Signal(a, m));
	Log.Awaited().OK();



class RPCd(commands.Cog):
	RPCd = app_commands.Group(
		name="rpcd",
		description="Manage RPC Detector",
	);

	@RPCd.command(
		name="scan",
		description="Scans all users and reports who are running a game in the configured channel."
	)
	@app_commands.allowed_installs(guilds=True, users=False)
	@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
	@commands.has_permissions(administrator=True)
	async def scan(self, C: discord.Interaction) -> None:
		await C.response.send_message("Manually retriggered RPC Scan.");
		await Scan_Members();



	@RPCd.command(
		name="toggle",
		description="Flag to tell RPCd if it should automatically scan for users or not."
	)
	@app_commands.describe(
		active="Specify whenever to enable the automatic scans or not.",
	)
	@app_commands.allowed_installs(guilds=True, users=False)
	@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
	@commands.has_permissions(administrator=True)
	async def toggle(self, C: discord.Interaction, active: bool) -> None:
		Cfg["Active"] = active;
		File.JSON_Write("Config.json", Cfg);
		await C.response.send_message("RPCd will now automatically scan for members." if (active) else "RPCd's automatic scan has been disabled.");





	@tasks.loop(seconds=Cfg["Cooldown"])
	async def RPCd_T(self) -> None:
		if (not Cfg["Active"]): return;
		Log.Warning("Triggering automatic RPC Scan.");
		await Scan_Members();

		C: discord.Thread | None = cast(discord.Thread | None, BOT.get_channel(Cfg["ID"]["Channel"]));
		if (not C): raise Exception(f"Unable to acquire Channel ID \"{Cfg["ID"]["Channel"]}\"");
		await C.send(content=f"Waiting until <t:{Time.Get_Unix() + Cfg["Cooldown"]}:R> before next automatic scan.");



	# Task Handling
	@RPCd_T.before_loop
	async def Wait_OnReady(self): await BOT.wait_until_ready();
	async def cog_load(self) -> None: self.RPCd_T.start();
	async def cog_unload(self) -> None: self.RPCd_T.stop();



async def setup(BOT: commands.Bot) -> None: await BOT.add_cog(RPCd(BOT));