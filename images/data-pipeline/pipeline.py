#!/usr/bin/env python

import pandas as pd
import sqlalchemy
import os

def create_connection():
    engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
    connection = engine.connect()
    return connection

def extract(connection):
    people_df = pd.read_sql_table('people', connection, schema=None, index_col='place_of_birth', coerce_float=True, parse_dates='date_of_birth', columns=None, chunksize=None)
    places_df = pd.read_sql_table('places', connection, schema=None, index_col='city', coerce_float=True, parse_dates=None, columns=None, chunksize=None)
    return people_df, places_df

def transform(people_df, places_df):
    joined_df = people_df.join(places_df, on=None, how='left', lsuffix='', rsuffix='', sort=False, validate=None)
    count_df = joined_df.groupby(['country']).size().sort_values(ascending=False)
    
def load(result_df):
    result_file = os.path.abspath('/data/result.json')
    result_df.to_json(path_or_buf=result_file)

if __name__ == '__main__':
   db_connection = create_connection()
   people_df, places_df = extract(db_connection)
   result_df = transform(people_df, places_df)
   load(result_df)
   
