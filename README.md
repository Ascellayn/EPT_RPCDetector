# Setup
- Create a new bot on [The Discord Development Portal](https://discord.com/developers/applications)
	- Make sure the bot has **Presence Intent and Server Members Intent permissions enabled**.
	- In the Installation Tab, make sure to give it the `bot` scope and the following permissions:
		- Embed Links
		- Send Messages
		- Send Messages in Threads
		- View Channels (If you're too lazy to manually configure the channel's permissions if the channel is not publicly viewable)
	- Finally, invite the bot to your Discord Server.
- Create a `.env` file:
```env
TOKEN="{Discord Bot Token}"
```
- Create a `Config.json` file:
```json
{
  "Debug": true,
  "Active": true, # If RPCd's automatic scan should be on
  "Cooldown": 500, # How long in seconds until RPCd automatically rescans for all members
  "ID": {
    "Guild": 501708824990711830, # Your server's Guild ID
    "Channel": 1283506671150174250 # The channel to post the reports
  },
  "Whitelist": [
  311057290562371586,
  ...
  ] # The list of users that reports shouldn't be sent if they get detected by RPCd
}
```
- Install dependencies inside of a venv
	- `python3 -m venv /tmp/venv`
	- `source /tmp/venv/bin/activate`
	- `pip install -R requirements.txt`
- Run RPCd
	- `python3 Main.py`