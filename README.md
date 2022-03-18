# Description

This project implements a sync worker that can be run on an hourly 
basis to collect weather related data from [Open-Meteo](https://open-meteo.com/en/docs).
The data will be inserted into a PostgreSQL database.

# Database Setup

A `database.sql` file is provided in the `/database` folder. However, it
is unnecessary to manually initialize the database. Each time the sync 
worker runs, it will check if the database has been set up. If it has not, it
will automatically create the required database and tables. It will also seed
the `location` table with data provided in a file called `data.csv` located
in the root directory.

# Running the Sync Worker

To run the sync worker locally you will first need to create a `.env` file.
A sample `.env.example` file has been provided. Variables that begin with `PG`
refer to the PostgreSQL database credentials. `LOGLEVEL` determines the minimum log
level that will be written to the log file `app.log`. The default log level if none is 
provided is `ERROR`.

## Running Locally

To run the application locally, first install all requirements using the 
command:

> pip3 install -r requirements.txt

You will then be able to run the worker using the command:

> python3 worker.py

## Running on Docker

To run the application in Docker, first build the container:

> docker build . -t dataeng

Then you can either pass in environment variables using a `.env` file as described
above using the command:

> docker run --env-file=.env dataeng


Alternatively, you can pass environment variables into Docker's `run` command directly:

> docker run -e PGHOST=localhost -e PGUSER=postgres -e PGDATABASE=weather 
> -e PGPASSWORD=password -e PGPORT=5432 -e LOGLEVEL=INFO dataeng


# Running Tests

To run tests locally, follow the steps above for setting up your local environment. 
You can then use this command to run tests:

> python3 -m unittest


To run tests in Docker, use this command if using a `.env` file:

> docker run --env-file=.env dataeng python3 -m unittest

Or alternatively:

> docker run -e PGHOST=localhost -e PGUSER=postgres -e PGDATABASE=weather 
> -e PGPASSWORD=password -e PGPORT=5432 -e LOGLEVEL=INFO dataeng
> python3 -m unittest