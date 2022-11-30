#!/usr/bin/env python

import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()

TARGET_PATH = os.getenv('TARGET_PATH')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

def create_connection():
    engine = sqlalchemy.create_engine(f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
    connection = engine.connect()
    return connection

def extract(connection):
    people_df = pd.read_sql_table('people', connection, schema=None, index_col='place_of_birth', coerce_float=True, parse_dates='date_of_birth', columns=None, chunksize=None)
    places_df = pd.read_sql_table('places', connection, schema=None, index_col='city', coerce_float=True, parse_dates=None, columns=None, chunksize=None)
    return people_df, places_df

def transform(people_df, places_df):
    joined_df = people_df.join(places_df, on=None, how='left', lsuffix='', rsuffix='', sort=False, validate=None)
    count_df = joined_df.groupby(['country']).size().sort_values(ascending=False)
    return count_df
    
def load(result_df):
    result_file = os.path.abspath(f"{TARGET_PATH}/result.json")
    result_df.to_json(path_or_buf=result_file)

if __name__ == '__main__':
   db_connection = create_connection()
   people_df, places_df = extract(db_connection)
   result_df = transform(people_df, places_df)
   load(result_df)
   
