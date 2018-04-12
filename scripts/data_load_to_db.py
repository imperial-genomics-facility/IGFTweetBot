#!/usr/bin/env python
import argparse
from db_scripts.data_load_to_db import load_data_to_sqlite_db

parser=argparse.ArgumentParser()
parser.add_argument('-d','--db_name', required=True, help='SQLite db name')
parser.add_argument('-f','--json_data', required=True, help='Message data json file')
args=parser.parse_args()

db_name=args.db_name
json_data=args.json_data

try:
  load_data_to_sqlite_db(db_name,json_data)
except Exception as e:
  print('Error: {0}'.format(e))