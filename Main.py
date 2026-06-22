from Common import *;
import dotenv, os;



""" Core Variables """
BOT_Uptime: int = Time.Get_Unix();
Modules: list[str] = [];





""" Core Functions """
async def Load_Module(Pth: str) -> bool:
	global Modules;

	try:
		if (Pth not in Modules):
			Log.Debug(f"Loading ({Pth})...");
			await BOT.load_extension(Pth);
			Modules.append(Pth);
		else:
			Log.Debug(f"Reloading ({Pth})...");
			await BOT.reload_extension(Pth);
	except Exception as Except: Log.Awaited().EXCEPTION(Except); exit(1);

	Log.Awaited().OK();
	return True;



async def Load_Modules(Folder: str) -> None:
	Directory = File.List(Folder);
	Folder = Folder.replace("/", "."); # Discordpy requires using "." instead of "/"

	for Module in Directory[1]:
		if (Module.endswith(".py") and not Module.startswith("_")):
			await Load_Module(f"{Folder}.{Module[:-3]}");

	for Subfolder in Directory[0]:
		if (Subfolder != "__pycache__"):
			Log.TSN_Debug(f"Recursively loading additional Modules from Subfolder {Subfolder}");
			await Load_Modules(f"{Folder}/{Subfolder}");





async def Synchronize_Commands() -> int | Exception:
	#return 0;
	Log.Info("Refreshing Local Slash Commands...");
	if (Cfg["ID"]["Guild"]):
		await BOT.tree.sync(guild=discord.Object(Cfg["ID"]["Guild"]));
		Log.Awaited().OK();
	else: Log.Awaited().Status_Update("[SKIPPED]");

	Log.Info("Refreshing Global Slash Commands...");
	Commands = await BOT.tree.sync();
	Log.Awaited().OK();
	Command_Count = len(Commands);

	Log.Info(f"Synchronized {Command_Count} commands.");
	return Command_Count;





@BOT.tree.error
async def on_error(I: discord.Interaction, Error: Exception) -> None:
	C_Name: str = getattr(I.command, "qualified_name", "unknown_command");
	M_Embed = discord.Embed (
		title=f'❌  An unknown error occurred while running "{C_Name}"!',
		color=Color_Tuple(TSNDL.Color.Abyss.Red)
	); M_Embed.description = str(Error); # We can't declare description directly within the above because Big Typing gets mad
	M_Embed.set_thumbnail(url=I.user.avatar);

	M_Embed.description += "\n\nPlease report this error on [GitHub](https://github.com/Ascellayn/EPT_RPCDetector/issues).";
	await I.followup.send(embed=M_Embed, ephemeral=True);

	if (DEBUG): raise Error; # Make sure the traceback shows in the console if Debug Mode is enabled.





""" Ignition """
def Bootstrap() -> None:
	dotenv.load_dotenv();
	Token: str | None = os.getenv("TOKEN");
	if (not Token): Log.Critical("No \"TOKEN\" was found in the .env!"); exit(1);
	BOT.run(Token);


@BOT.event
async def setup_hook() -> None:
	Log.Info("Loading Modules...");
	try:
		await Load_Modules("Modules");
		Log.Awaited().OK(str(len(Modules)));
	except Exception as Except:
		Log.Awaited().EXCEPTION(Except);
		quit();

	await Synchronize_Commands();





""" Launch Sequence """
if (__name__ == '__main__'):
	TSN_Abstracter.App_Init(True);
	Config.Logger.Print_Level = 15 if (DEBUG) else 20;
	Bootstrap();

	Log.Critical(f"Goodbye.");