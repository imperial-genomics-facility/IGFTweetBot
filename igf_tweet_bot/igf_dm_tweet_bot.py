#!/usr/bin/env python
import twitter, json,re,copy,string
from sqlalchemy import create_engine
from db_tables import Base,Tweet_message
from db_scripts.create_db_tables import create_db_tables_in_sqlite
from db_scripts.data_load_to_db import load_data_to_sqlite_db

class IgfDmTweetBot:
  '''
  A class for creating tweet bot instance for replying through direct message
  
  :param config_file : Twitter api token file
  :param bot_id : Tweet bot user id
  :param quick_reply_json : A json file containing the quick reply options
  :param db_name : SQLite database name
  :param db_data : A json file containing reply messages for database
  '''
  def __init__(self,config_file,bot_id,quick_reply_json,db_name,db_data):
    self.config_file=config_file
    self.bot_id=bot_id
    self.db_name=db_name
    self.db_data=db_data
    self.quick_reply_json=quick_reply_json
    self.api=self._get_tweet_api()
    self.post_data=self._load_post_data()

  def _get_tweet_api(self):
    '''
    An internal method for creating tweet api
    '''
    try:
      with open(self.config_file,'r') as json_data:
        twep_token=json.load(json_data)

      api = twitter.Api(twep_token['consumer_key'],
                    twep_token['consumer_secret'],
                    twep_token['access_token_key'],
                    twep_token['access_token_secret'])
      return api
    except:
      raise

  def _load_post_data(self):
    '''
    An internal api for loading quick reply json data
    '''
    try:
      with open(self.quick_reply_json,'r') as json_data:
        quick_reply_data=json.load(json_data)

      post_data={'event': {
             "type": "message_create",
             "message_create": {
               "target": {
                 "recipient_id": None,
               },
               "message_data": {  
                 "text": None,
                 "quick_reply": quick_reply_data,
               },
              },
            }
          }
      return post_data
    except:
      raise


  def _get_sqlite_db_session(self):
    '''
    An internal method for creating a sqlalchemy database session
    '''
    try:
      if db_name != ':memory:' and not os.path.exists(db_name):
        raise IOError('SQLite database {0} not found'.format(db_name))

      db_url='sqlite:///{0}'.format(db_name)
      engine=create_engine(db_url)
      Session=sessionmaker(bind=engine)
      session=Session()
      return session
    except:
      raise

  @staticmethod
  def get_message_output(keyword,session):
    '''
    A static method for calculating reply output

    :param keyword : A text string sent by twitter users
    :param session : A SQLite database session

    :returns String
    '''
    try:
      keyword.strip()
      pattern1=re.compile('[{0}]+'.format(string.punctuation))
      keyword=re.sub(pattern1,'_',keyword)                                      # remove all punctuation chrs
      pattern2=re.compile(r'\s+')
      keyword=re.sub(pattern2,'_',keyword)                                      # remove all space
      message=session.query(Tweet_message).\
                      filter(Tweet_message.keyword==keyword).\
                      one_or_none()
      if message:
        return message.message_out
      else:
        return 'Please select one option from the menu'
    except:
      raise

  def create_sqlite_database(self):
    '''
    A helper method for creating SQLite database with required tables
    '''
    try:
      create_db_tables_in_sqlite(db_name=self.db_name)
    except:
      raise


  def load_reply_msg_to_database(self):
    '''
    A helper method for loading reply messages to database
    '''
    try:
      load_data_to_sqlite_db(db_name=self.db_name,
                             json_data=self.db_data)
    except:
      raise


  def start_dm_streaming_for_bot(self):
    '''
    A method for starting the user stream bot for checking direct messages
    '''
    try:
      api=self.api
      strm=api.GetUserStream()
      session=self._get_sqlite_db_session()
      url='{0}/direct_messages/events/new.json'.format(api.base_url)
      for strm_line in strm:
        for strm_key, strm_value in strm_line.items():
          if strm_key=='direct_message':
            sender_id=strm_value['sender_id']
            text_msg=strm_value['text']
            if sender_id != self.bot_id:
              temp_post_data=self.post_data
              post_data=copy.copy(temp_post_data)
              post_data["event"]["message_create"]["target"]["recipient_id"]=None        # reset recipient_id
              post_data["event"]["message_create"]["message_data"]["text"]=None          # reset reply message  
              msg=self.get_message_output(keyword=strm_value['text'],
                                          session=session)                               # calculate new reply message
              post_data["event"]["message_create"]["target"]["recipient_id"]=sender_id   # add new sender id
              post_data["event"]["message_create"]["message_data"]["text"]=msg           # add new reply message
              data=json.dumps(post_data)                                                 # dump data to json
              api._RequestUrl(url, 'POST', data=data)                                    # post data to Twitter
    except:
      session.close()
      raise