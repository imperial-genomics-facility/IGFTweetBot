### Usage
<pre><code>usage: run_tweet_dm_bot.py -h
                           -d DB_NAME 
                           -f QUICK_REPLY_DATA 
                           -m MESSAGE_DATA
                           -i BOT_ID 
                           -t TOKEN_FILE

optional arguments:
  -h, --help                                   Show this help message and exit
  -d ,--db_name DB_NAME                        SQLite db name
  -f ,--quick_reply_data QUICK_REPLY_DATA      Quick reply data json file
  -m ,--message_data MESSAGE_DATA              Message data json file
  -i ,--bot_id BOT_ID                          Bot twitter id
  -t ,--token_file TOKEN_FILE                  Twitter api token file
</code></pre>

### Quick reply data
Twitter has a specific structure for the [quick replies using direct messaging](https://developer.twitter.com/en/docs/direct-messages/quick-replies/api-reference/options). The data for the "quick_reply" post data senction can be provided using a json file.

#### An example json structure for quick reply data
<pre><code>{
          "type": "options",
          "options": [
            {
              "label": "Red Bird",
              "description": "A description about the red bird.",
              "metadata": "external_id_1"
            },
            {
              "label": "Blue Bird",
              "description": "A description about the blue bird.",
              "metadata": "external_id_2"
            },
            {
              "label": "Black Bird",
              "description": "A description about the black bird.",
              "metadata": "external_id_3"
            },
            {
              "label": "White Bird",
              "description": "A description about the white bird.",
              "metadata": "external_id_4"
            }
          ]
}
</code></pre>

### Message json data
The bot reply for the user tweets can be loaded to database using an json data file. There should be two entries present for each of the json data blocks, e.g. 'keyword' and 'message_out'. No white spache or any symbols (except "\_") are allowed for the 'keyword' section.

#### An example of the message data
<pre><code>[
  { "keyword":"White_Bird",
    "message_out":"A nice white bird"
   }
]
</code></pre>

### Twitter api token
The consumer and access token keys for the Twitter app should be provided using a json file. 
**Note: Twitter app should have permissions for sending direct messages**

#### An example token file
<pre><code>{
    "consumer_key":"AAAAAAAAAAAAAAAAAA",
    "consumer_secret":"BBBBBBBBBBBBBBBBBB",
    "access_token_key":"CCCCCCCCCCCCCCCCCC",
    "access_token_secret":"DDDDDDDDDDDDDDDDD"
}
</code></pre>

### Run IGFTweetBot using docker image
A docker image is available for running this tweet bot.
* [avikdatta/tweetbotdockerimage](https://hub.docker.com/r/avikdatta/tweetbotdockerimage/)

#### Pull docker image from Dockerhub
<pre><code>  docker pull avikdatta/tweetbotdockerimage
</code></pre>

#### Run tweetbot from docker image
<pre><code>docker run -d \
-v /host_dir/igf_bot_conf:/home/vmuser/igf_bot_conf:z \
avikdatta/tweetbotdockerimage python /home/vmuser/IGFTweetBot/scripts/run_tweet_dm_bot.py \
  -d /home/vmuser/tweetbot_db.sqlite \
  -f /home/vmuser/igf_bot_conf/quick_reply.json  \
  -m /home/vmuser/igf_bot_conf/reply_messages.json  \
  -t /home/vmuser/igf_bot_conf/twitter_api_token.json \
  -i bot_user_id
</code></pre>
