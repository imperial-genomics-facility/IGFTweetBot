import twitter, json,re,copy
from sqlalchemy import create_engine
from db_tables import Base,Tweet_message

class IgfDmTweetBot:
  '''
  '''
  def __init__(self,config_file,bot_id,quick_reply_json,db_name):
    self.config_file=config_file
    self.bot_id=bot_id
    self.db_name=db_name
    self.quick_reply_json=quick_reply_json

    self.db_session=self._get_sqlite_db_session()
    self.api=self._get_tweet_api()
    self.post_data=self._load_post_data()

  def _get_tweet_api(self):
    '''
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
    '''
    try:
      keyword.strip()
      pattern=re.compile(r'\s+')
      keyword=re.sub(pattern,'_',keyword)
      message=session.query(Tweet_message).filter(Tweet_message.keyword==keyword).one_or_none()
      if message:
        return message.message_out
      else:
        return 'Please select one option from the menu'
    except:
      raise


  def start_dm_streaming_for_bot(self):
    '''
    '''
    try:
      api=self.api
      strm=api.GetUserStream()

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
                                          session=self.session)                         # calculate new reply message
              post_data["event"]["message_create"]["target"]["recipient_id"]=sender_id   # add new sender id
              post_data["event"]["message_create"]["message_data"]["text"]=msg           # add new reply message
              data=json.dumps(post_data)                                                 # dump data to json
              api._RequestUrl(url, 'POST', data=data)                                    # post data to Twitter
    except:
      raise