#!/usr/bin/env python3
import os
import json
import pytwitter
import argparse
import datetime
import shutil

DEFAULT_CONFIG = {
    "users": {}
}


def get_config():
    config_path = os.path.expanduser(os.environ.get("TWITTER_TIME_OUT_CONFIG", "~/.twitter_time_out.json"))

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG


def save_config(config):
    config_path = os.path.expanduser(os.environ.get("TWITTER_TIME_OUT_CONFIG", "~/.twitter_time_out.json"))
    backup_path = f"{config_path}.bak"

    shutil.copy(config_path, backup_path)

    try:
        with open(config_path, "w") as f:
            json.dump(config, f)
    except Exception:
        print("Write failed. Restoring from Backup. Check integrity before rerunning")
        shutil.copy(backup_path, config_path)
        exit(1)


def unmute_expired(twitter_client):
    config = get_config()
    today = datetime.datetime.today()
    expired = []

    for k, v in config["users"].items():
        expire_time = datetime.datetime.strptime(v["expire"], "%y-%m-%d")
        if expire_time < today:
            expired.append(k)

    for user in expired:
        try:
            user_payload = twitter_client.get_user(username=user)
            print(twitter_client.unmute_user(user_id=twitter_client.auth_user_id, target_user_id=user_payload.data.id))
        except pytwitter.error.PyTwitterError as e:
            print(e)
            print(f"User {user} not found or could not be un-muted. Unmute manually if necessary")
        config["users"].pop(user)

    save_config(config)


def mute_users(twitter_client, users, days):
    config = get_config()
    expiration_date = datetime.date.today() + datetime.timedelta(days=days)
    expiration_date_formatted = expiration_date.strftime("%y-%m-%d")

    for user in users:
        try:
            user_payload = twitter_client.get_user(username=user)
            twitter_client.mute_user(user_id=twitter_client.auth_user_id, target_user_id=user_payload.data.id)
            print(f"{user} muted")
            config["users"][user] = {"expire": expiration_date_formatted}
        except pytwitter.error.PyTwitterError as e:
            print(e)
            print(f"User {user} not found or could not be muted")

    save_config(config)


def unmute_manual(twitter_client, users):
    config = get_config()

    for user in users:
        try:
            user_payload = twitter_client.get_user(username=user)
            print(twitter_client.unmute_user(user_id=twitter_client.auth_user_id, target_user_id=user_payload.data.id))
        except pytwitter.error.PyTwitterError as e:
            print(e)
            print(f"User {user} not found or could not be un-muted. Unmute manually if necessary")

        if config["users"].get(user):
            config["users"].pop(user)
        else:
            print(f"User {user} not currently muted")

    save_config(config)


if __name__ == "__main__":

    args = argparse.ArgumentParser(
        description="Twitter Time-Out: Temporary twitter mute. Each run will unmute users whose time-outs have expired"
    )
    args.add_argument("-m", "--mute", action="append", help="User to put in time-out (repeatable)")
    args.add_argument("-u", "--unmute", action="append", help="User to remove from time-out early (repeatable)")
    args.add_argument("-d", "--days", default=30, type=int, help="How many days to put users in time-out this run")
    args = args.parse_args()

    twitter_client_main = pytwitter.Api(
        consumer_key=os.environ.get("CONSUMER_KEY"),
        consumer_secret=os.environ.get("CONSUMER_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_secret=os.environ.get("ACCESS_SECRET")
    )

    unmute_expired(twitter_client_main)

    if args.mute:
        mute_users(twitter_client_main, args.mute, args.days)

    if args.unmute:
        unmute_manual(twitter_client_main, args.unmute)
