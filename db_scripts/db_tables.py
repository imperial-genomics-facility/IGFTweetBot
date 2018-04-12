#!/usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Column,Integer,String,TEXT,create_engine,UniqueConstraint

Base = declarative_base()

class Tweet_message(Base):
  '''
  Table schema for quick reply message
  '''
  __tablename__ = 'tweet_message'
  __table_args__ = ( UniqueConstraint('keyword'),)

  message_id  = Column(Integer, primary_key=True, nullable=False)
  keyword     = Column(String(100), nullable=False)
  message_out = Column(TEXT())
    
  def __repr__(self):
    return "Tweet_message(message_id = '{self.message_id}', " \
                    "keyword = '{self.keyword}'," \
                    "message_out = '{self.message_out}')".format(self=self)