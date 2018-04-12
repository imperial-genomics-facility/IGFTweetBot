#!/usr/bin/env python
import argparse
from igf_tweet_bot.igf_dm_tweet_bot import IgfDmTweetBot

parser=argparse.ArgumentParser()
parser.add_argument('-d','--db_name', required=True, help='SQLite db name')
parser.add_argument('-f','--quick_reply_data', required=True, help='Quick reply data json file')
parser.add_argument('-m','--message_data', required=True, help='Message data json file')
parser.add_argument('-i','--bot_id', required=True, help='Bot twitter id')
parser.add_argument('-t','--token_file', required=True, help='Twitter api token file')
args=parser.parse_args()

db_name=args.db_name
quick_reply_data=args.quick_reply_data
bot_id=args.bot_id
token_file=args.token_file
message_data=args.message_data

try:
  bot=IgfDmTweetBot(config_file=token_file,
                    bot_id=bot_id,
                    quick_reply_json=quick_reply_data,
                    db_name=db_name,
                    db_data=message_data)
  bot.create_sqlite_database()
  bot.load_reply_msg_to_database()
  bot.start_dm_streaming_for_bot()
except KeyboardInterrupt:
    print('stopped bot')
except Exception as e:
  raise
  print('Error: {0}'.format(e))