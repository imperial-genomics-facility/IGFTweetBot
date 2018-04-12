#!/usr/bin/env python
import os
from db_scripts.db_tables import Base
from sqlalchemy import create_engine

def create_db_tables_in_sqlite(db_name=':memory:'):
  '''
  A utility function for creating sqlite database tables
  
  :param db_name, A SQLite database file name, default is :memory:
  '''
  try:
    if db_name != ':memory:' and os.path.exists(db_name):
      raise IOError('SQLite database {0} is already present'.format(db_name))

    db_url='sqlite:///{0}'.format(db_name)
    engine=create_engine(db_url)
    Base.metadata.create_all(engine)
  except:
    raise