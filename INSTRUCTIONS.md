# data-eng-exam

project
---
Implement a sync worker that collects historical and forecast weather data. Collected data will need to be re-shaped and inserted into a PostgreSQL database; you are additionally responsible for the schema of this database. The worker will be expected to collect weather data for a dynamic number of locations.

The sync worker is expected to run on a continuous schedule, updating historical and forecast weather data **once per hour**. The sync worker should be insulated against API or deployment outages, such that if the worker fails to run for a number of hours, whenever it is able to resume it is ready to backfill all missing data (or as much as possible to recover via the given API). Aside from delays in new updates, the database should never be in an intermediate or otherwise corrupted state in terms of data integrity.

api
---
You will need to pull a variety of datapoints from [Open-Meteo](https://open-meteo.com/en). This is a free API that has no `api-key` or `OAuth` requirements.

From **Open-Meteo**, you'll need to pull the following **hourly** datapoints for all currently available `lat,lng` coordinates:
- temperature_2m (°F)
- relativehumidity_2m
- dewpoint_2m (°F)
- pressure_msl
- cloudcover
- precipitation (inch)
- weathercode

This API is limited to returning only the past **2 days** of historical data, so upon initializing a new coordinate the sync worker is only expected to backfill that limited window of historical data. Otherwise, as the sync worker runs, it should be continuously updating a **historical** collection of the above datapoints, as well as caching the next 7 days of **forecast** data. To this end, you'll be expected to design a schema that robustly captures these two growing collections.

materials
---
The sync worker should expect to connect to the PostgreSQL database by way the following environment variables:
```
export PGHOST=...
export PGUSER=...
export PGDATABASE=...
export PGPASSWORD=...
export PGPORT=...
```
Additionally, you will be provided a `data.csv` containing `lat,lng` pairs. This is the initial workload of locations for the sync worker.

deliverable
---
The deliverable here should be a **Python** program that polls the API and writes to the given PostgreSQL database. All dependencies for this program should be packaged via a `requirements.txt` and a `Dockerfile`. The worker should be expected to run on **Linux** inside a **Docker** container.

Additionally, you are expected to provide a `.sql` script that captures all of the `CREATE TABLE` and associated expressions required to initialize the database to the desired schema.

Please include instructions in `README.md` on how to launch the application as well as to run tests, if any.

Project should be uploaded by way of a **pull-request** created for this repo. Ideally, the work is staged in a series of incremental commits that document the implementation process. Please try to avoid a single, all-encompassing commit that includes the entire implementation.
