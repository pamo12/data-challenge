#!/usr/bin/env python

import sys
import pandas as pd
import sqlalchemy
from sqlalchemy import Table, Column, Date, String
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_PATH = os.getenv('SOURCE_PATH')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

engine = sqlalchemy.create_engine(f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
connection = engine.connect()
metadata = sqlalchemy.schema.MetaData(engine)

def initialize():
    print("(Re-)creation of Schema started.")
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
    people_df = places_df = pd.DataFrame
    try:
        people_df = pd.read_csv(f"{SOURCE_PATH}/people.csv")
    except FileNotFoundError:
        print(f"File {SOURCE_PATH}/people.csv not found.")

    try:
        places_df = pd.read_csv(f"{SOURCE_PATH}/places.csv")
    except FileNotFoundError:
        print(f"File {SOURCE_PATH}/places.csv not found.")
    
    if not people_df.empty:
        people_df.to_sql('people', connection, chunksize=1000, dtype=None, method=None, schema=None, if_exists='append', index=False, index_label=None)
    if not places_df.empty:
        places_df.to_sql('places', connection, chunksize=1000, dtype=None, method=None, schema=None, if_exists='append', index=False, index_label=None)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == "initialize":
        initialize()
    ingest()