# Flight Delay Analysis Web App

A Django-powered web application for exploring flight schedules, integrating weather forecasts, and analyzing flight-delay patterns. It brings together structured flight data, data processing, configurable delay scoring, and an interactive web interface in a single Python application.

## Overview

Flight delays are influenced by a combination of operational and environmental factors. This application provides a workflow for searching flights, examining departure and arrival weather, and comparing delay-related indicators across routes and airlines.

The backend uses **Django** for request handling and session management, **pandas** for tabular analysis, and the **OpenWeather API** for optional forecast enrichment. Delay scores are calculated from predefined weather, temperature, and airline weights rather than a trained predictive model.

## Features

| Feature | Description |
| --- | --- |
| **Flight Search** | Filter flight schedules by departure airport, destination, travel date, and optional airline. |
| **Weather Integration** | Fetch five-day forecasts and daily temperature ranges for selected cities via OpenWeather. |
| **Delay Scoring** | Combine weather conditions, temperature ranges, and airline-specific factors using a weighted, rule-based scoring method. |
| **Flight Favorites** | Save and remove flights using Django sessions; the backend also computes counts by airline and destination airport. |
| **Route Analysis** | Process route and aircraft-type records from a configurable historical spreadsheet. |
| **Airline Ranking** | Sort airline delay indicators and display a configurable top-N list from an analysis dataset. |

## Technology Stack

| Area | Technologies |
| --- | --- |
| Backend | Python, Django |
| Data processing | pandas, openpyxl |
| Data storage | SQLite for Django session persistence; CSV and Excel for flight data |
| Weather | OpenWeather forecast API, Requests |
| Frontend | HTML, CSS, Django templates, JavaScript |
| Configuration | Environment variables, python-dotenv |

## Application Workflow

```text
              Flight schedule (CSV / Excel)
                          |
                          v
                Flight search filters
               /                  \
              v                    v
       Selected flights      Weather forecast
              |              (when configured)
              |                    |
              +----------+---------+
                         |
                         v
              Rule-based delay score
                         |
                         v
                Search results page
                         |
                         v
               Session-based favorites

      Additional data inputs (Excel)
                   |
              +----+----+
              v         v
         Route analysis  Airline ranking
```

### Flight Search and Delay Scoring

Flight records are loaded with pandas and filtered by the criteria provided in the search form. If weather data is available for the selected date, the application enriches the matching records with departure and arrival forecasts and computes a weighted indicator using:

- Departure and arrival weather conditions
- Minimum and maximum temperatures at both endpoints
- Airline-specific weighting factors

The resulting **delay score is a heuristic indicator**, not a statistically calibrated probability. When a required weather observation is unavailable, the interface displays the score as unavailable instead of inventing a value.

### Data Analysis

The analysis views read structured spreadsheets to support route-specific comparisons and airline rankings. Historical route analysis filters by route and aircraft type, while the ranking view orders airlines by an input delay-rate indicator. Dataset paths are configurable, allowing different compatible data sources to be used without changing application code.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- `pip` and a Python virtual environment
- An OpenWeather API key for optional weather enrichment

### 1. Clone the repository

```bash
git clone https://github.com/Chloe-Xia/Flight-Delay-Analysis-Web-App.git
cd Flight-Delay-Analysis-Web-App
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

### 3. Configure environment variables

```bash
cp .env.example .env
```

Configure your local `.env` file:

```dotenv
DJANGO_SECRET_KEY=replace_with_a_unique_random_value
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Optional: enrich search results with a five-day weather forecast
OPENWEATHER_API_KEY=

# Optional: load your own flight and analysis datasets
# FLIGHT_SCHEDULE_PATH=/absolute/path/to/flights.csv
# FLIGHT_ANALYSIS_PATH=/absolute/path/to/route_weather.xlsx
# AIRLINE_RANKING_PATH=/absolute/path/to/airline_delays.xlsx
```

Keep `.env` private; the repository includes `.env.example` for configuration reference.

### 4. Start the application

```bash
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** to open the web interface.

## Try the Included Demo Data

The repository includes `data/sample_flights.csv`, a small **fictional dataset** for exploring the flight search and favorites workflow without requiring external datasets.

1. Open the **Search** page.
2. Choose **Beijing Daxing International Airport (PKX)** as the departure airport.
3. Choose **Shanghai Hongqiao International Airport (SHA)** as the destination.
4. Select **2026-11-09** and submit the search.
5. Save a matching flight and open the **Favorites** page.

The sample records use fictional `DEMO` flight numbers. Live forecast enrichment is optional and operates on the dates available from the weather provider.

## Data Inputs

| Environment variable | Expected data |
| --- | --- |
| `FLIGHT_SCHEDULE_PATH` | CSV or Excel file containing flight date, origin, destination, airline, flight number, and scheduled times. |
| `FLIGHT_ANALYSIS_PATH` | Excel workbook containing route, aircraft type, weather, temperature, and scheduled-time fields for route analysis. |
| `AIRLINE_RANKING_PATH` | Excel workbook containing airline names and delay-rate indicators. |

The flight search expects the following source columns:

```text
date, departure_airport, destination, airline, flight_number, STD, STA
```

See [`data/README.md`](data/README.md) for the input schemas and field names used by the data-processing views.

## Project Structure

```text
Flight-Delay-Analysis-Web-App/
├── main.py 
├── manage.py                     # Django management commands
├── requirements.txt              # Python dependencies
├── .env.example                  # Configuration template
├── .gitignore
├── delayflightProject/
│   ├── settings.py               # Environment-based Django settings
│   ├── urls.py                   # Application URL routes
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── views.py                  # Search, weather, scoring, favorites, analysis
│   ├── models.py
│   ├── tests.py                  # Django smoke tests
│   ├── templates/                # Page templates
│   ├── static/css/app.css        # Interface styles
│   └── migrations/
└── dataset/
```

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Home page |
| `/search/` | Flight search form |
| `/search_flight/` | Search and weather-enriched results |
| `/weather/<city_name>/` | City weather view |
| `/favorite/` | Saved flights |
| `/analysis/` | Route-level analysis |
| `/ranking/` | Airline ranking |

## Testing

Run the included Django smoke tests:

```bash
python manage.py test users
```

The tests cover home-page rendering, search using the bundled sample data, favorites initialization, and handling missing ranking datasets.

## Further Exploration

This application provides a foundation for exploring aviation datasets, combining weather and schedule information, and extending flight analysis workflows with additional data sources and analytical methods.
