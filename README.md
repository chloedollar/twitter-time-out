# twitter-time-out

**NOTE: After the change in management, I no longer use Twitter. Feel free to use as a reference, but I will not be maintaining these scripts**

Simple script to temporarily mute Twitter users

I wrote this script for my own personal use, but I am publishing it in case others find it useful. This script comes with no warranty or guarantee. Use at your own risk

While a bit hacky and unsafe, I'm just storing muted users in a json file `~/.twitter_time_out.json`. I only use my mute list for temporary mutes, so I'm not concerned with potential data loss. I can just manually unmute everyone and start over. As the script is currently written, there's a chance that you will need to manually unmute someone. If you are uncomfortable with this and/or worried about a temporary mute becoming permanent, either don't use this script or extend it yourself

See `--help` for usage information

## Authentication
I am using OAuth V1 for my use because it is simple, and I'm only operating on my personal account. You'll need to generate your own Twitter dev account and credentials. Provide the following through environmental variables:
- CONSUMER_KEY
- CONSUMER_SECRET
- ACCESS_TOKEN
- ACCESS_SECRET

I store these environmental variables in `.twitter` and run the script through an alias: `alias twitter-time-out=". $HOME/.twitter && /path/to/twitter-time-out/twitter_time_out.py"`

## Automation
This script will unmute users whose mutes have expired every run. Have cron run the script with no arguments to automate unmuting
