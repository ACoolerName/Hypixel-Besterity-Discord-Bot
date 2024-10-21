## Arachne Hypixel Discord Bot By @t_cr1ck (discord) | @ACoolerName (github)
### Readme Updated: Release 2.1

1. Install requirements with "pip install -r requirements.txt"

2. Put hypixel api key "api_key.txt", discord bot token in "discord_bot_token.txt", hypixel guild id in "guild_id.txt"

3. Remove the "REMOVEME.txt" files from the following directories: "/userdata/" "/userkills/" "/userkills_old/" "/weeklykills/"
_These files are used to stop github from removing the empty directories from the repo._

4. Run main.py

**WARNING:** DO NOT - share this project WITHOUT removing the hypixel apikey from apikey.txt AND the discord bot token from discord_bot_token.txt

### List of commands:
**Leaderboard:**
/alldaily
/allweekly
/alltotal
/t1daily
/t1weekly
/t1total
/t2daily
/t2weekly
/t2total

**Profit Calculator:**
/t1profit
/t2profit

**Other:**
/check
/info
/copypasta


### Current features:
- [x] guild bestiary leaderboard
- [x] profit calculator
- [x] automatic api requests every 15mins

### TODO:
- [ ] Add 'disabled' to buttons
- [ ] Fix multithreading
- [ ] Fix old user data clearing
- [ ] Optimisations
