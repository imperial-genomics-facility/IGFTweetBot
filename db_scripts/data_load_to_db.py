#!/usr/bin/env python
import pandas as pd
from sqlalchemy import create_engine
from db_tables import Base,Tweet_message

def insert_dataframe_row(session, table, df):
  '''
  A function for loading data to table
  
  :param session, active database session
  :param table, a table name for loading data
  :param df, input data as dataframe
  '''
  df=df.fillna('')
  df_dict=df.to_dict()
  try:
    df_dict={ key:value for key, value in df_dict.items() if value}             # filter any empty value
    obj=table(**df_dict)
    session.add(obj)
    session.flush()
  except Exception as e:
    print("Failed to insert row, error: {}".format(e))
    session.rollback()

def load_data_to_sqlite_db(db_name,json_data):
  '''
  A utility function for loading data to sqlite database
  
  :param db_name, Name of the SQLite database
  :param json_data, A json file containing input data
  '''
  try:
    if db_name != ':memory:' and not os.path.exists(db_name):
      raise IOError('SQLite database {0} not found'.format(db_name))

    db_connected=0
    db_url='sqlite:///{0}'.format(db_name)
    engine=create_engine(db_url)
    Session=sessionmaker(bind=engine)
    session=Session()
    db_connected=1
    message_data=pd.read_json(json_data)
    message_data.apply(lambda x: insert_dataframe_row(session,Tweet_message, x), axis=1);
    session.commit()
  except Exception as e:
    print("Failed to load data, error: {}".format(e))
    if db_connected==1:
      session.rollback()