# Fever Events Microservice

## Goal

Our mission is to develop and expose just one endpoint, and should respect the following Open API spec, with the formatted and normalized data from the external provider: https://app.swaggerhub.com/apis-docs/luis-pintado-feverup/backend-test/1.0.0
This endpoint should accept a "starts_at" and "ends_at" param, and return only the events within this time range.

- It should only return the events that were available at some point in the provider's endpoint(the sell mode was online, the rest should be ignored)
- We should be able to request this endpoint and get events from the past (events that came in previous API calls to the provider service since we have the app running) and the future.
- The endpoint should be fast in hundreds of ms magnitude order, regardless of the state of other external services. For instance, if the external provider service is down, our search endpoint should still work as usual.

Example: If we deploy our application on 2021-02-01, and we request the events from 2021-02-01 to 2022-07-03, we should see in our endpoint the events 291, 322 and 1591 with their latest known values.

## Requirements

- The service should be as resource and time efficient as possible.
- The Open API specification should be respected.
- Use PEP8 guidelines for the formatting
- Add a README file that includes any considerations or important decision you made.
- If able, add a Makefile with a target named run that will do everything that is needed to run the application.

## What We have Build

### Features

- Fetch and parse event data from an external provider's XML API
- Normalize and store event data in a `MySQL` database
- Expose an API endpoint using `FastAPI` to query events
- Use `Celery/Redis` for periodic data fetching and task scheduling
- `Logs` any exception occured in the system

### Considerations

- We have used fast API - A Fastest Python Web Development Framwork due to it's feature rich and light weight.
- We have used MySQL as we are getting structured data from the provider API.
- We have used Celery/ Redis for running scheduling task to get Past and Future events from the Provider API and store in our
  MySQL database.

### Setup

#### Prerequisites

- Python 3.10+
- MySQL
- Redis Server

#### Commands

1. **MySQL Database Setup:**

- Create a database named `fever_events` on MySQL Localhost

2. **Redis Server:**

- Redis server should be up and running on port 6379
  ( How to install Redis :- [https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/))

3. **Run command to create virtual environment, create required tables in MySQL database using Makefile: ( Run for first Time only, not needed once environment has been set up )**

   ```bash
   make env-setup
   ```

4. **Run command to create required tables in MySQL database using Makefile: ( Run for first Time only, not needed to run once tables has been created )**

   ```bash
   make migration
   ```

5. **Run command to start celery worker for executing scheduled task using Makefile: ( Every Time we want to run the project, run in new command line )**

   ```bash
   make celery-worker
   ```

6. **Run command to start celery beat for scheduing task using Makefile: ( Every Time we want to run the project, run in new command line )**

   ```bash
   make celery-beat
   ```

7. **Run command to start API project using Makefile: ( Every Time we want to run the project, run in new command line)**

   ```bash
   make api
   ```

#### Usage

Access the GET API at [http://localhost:8000/search](http://localhost:8000/search)

##### Query Parameters:

- `starts_at`: Events that starts after this date
- `ends_at`: Events that finishes before this date

## Future Improvements

- If we have 50/60k events We can add server side pagination, searching, sorting for the list of events we are getting from search API to reduce the API response time.
- We can add multi threading while parsing the XML if we have large XML data to be parsed.
- We can include server side caching
