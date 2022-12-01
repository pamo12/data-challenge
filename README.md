# data-challenge

This repository includes a possible solution for a recruiting challenge aiming to showcase understanding of databases, data processing and python.

Challenge:
- Ingest data from 2 given csv files into MySQL, database schema has to be created first
- Output a summary of the data by loading the data from MySQL and aggregate information

Requirement:
- Solution runs in Docker

# Run the solution

## General
- Clone the repository: ```git clone git@github.com:pamo12/data-challenge.git```
- Create .env based on .env.example: ```cp .env.example .env```
- Build the Docker images: ```docker comppose build```
- Start database container: ```docker compose up database```

## data-ingestion
Data ingestion is handled in a separate container. Ingestion takes care of loading the data from CSV to MySQL. A re-creation of the MySQL schema is possible with each ingestions process.

There is two different ways to create the schema:
1. Use the *initialize.sql* script and pipe into MySQL instance </br>

    ```docker compose run --no-TTY database mysql --host=database --user=codetest --password=****** codetest < images/data-ingestion/initialize.sql```

2. Run data-ingestion container with initialize property, this will also trigger the ingestion </br>
    ```docker compose run data-ingestion initialize```

In case you decided for option 1., the ingestion has to be triggred by using:</br>
    ```docker compose run data-ingestion```

## data-pipeline
The data-pipeline container takes care of extracting, aggregating and loading the data to a result file. </br>
    ```docker compose run data-pipeline```

The result file is stored in *./data/summary_output.json*
