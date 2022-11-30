#!/usr/bin/env python

import pandas as pd
import sqlalchemy
from sqlalchemy import Table, Column, Date, String, Index


engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()
metadata = sqlalchemy.schema.MetaData(engine)

def initialize():
    people = Table(
        "people",
        metadata,
        Column("given_name", String(255), nullable=False),
        Column("family_name", String(255), nullable=False),
        Column("date_of_birth", Date),
        Column("place_of_birth", String(255), nullable=False, index=True),
    )

    places = Table(
        "places",
        metadata,
        Column("city", String(255), nullable=False, index=True),
        Column("county", String(255), nullable=False),
        Column("country", String(255), nullable=False),
    )
    
    if sqlalchemy.inspect(engine).has_table("people"):
        print("Table people already exists, will be dropped.")
        people.drop()

    if sqlalchemy.inspect(engine).has_table("places"):
        print("Table places already exists, will be dropped.")
        places.drop()
    
    metadata.create_all()

def ingest():
    try:
        people_df = pd.read_csv('/data/people.csv')
    except FileNotFoundError:
        print("File /data/people.csv not found.")

    try:
        places_df = pd.read_csv('/data/places.csv')
    except FileNotFoundError:
        print("File /data/places.csv not found.")
    
    people_df.to_sql('people', connection, chunksize=1000, dtype=None, method=None, schema=None, if_exists='append', index=False, index_label=None)
    places_df.to_sql('places', connection, chunksize=1000, dtype=None, method=None, schema=None, if_exists='append', index=False, index_label=None)


if __name__ == '__main__':
    initialize()
    ingest()