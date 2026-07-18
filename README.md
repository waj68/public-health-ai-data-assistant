
# Public Health AI Data Assistant

The Public Health AI Data Assistant is a prototype Streamlit application designed to explore how public health surveillance data can be queried, summarized, and visualized through a simple assistant-style interface.

This version uses semi-synthetic public health data and a safe rule-based free-text workflow. It does not use real patient data and does not currently connect to an external AI/LLM service.

## Current Version

Phase 5A completed prototype with expanded rule-based free-text question support and Streamlit deployment.

## What the App Does

The app allows users to:

- Select predefined public health questions
- Ask selected free-text public health questions
- Generate safe SQL queries using rule-based logic
- Run approved SELECT queries against local CSV data using DuckDB
- View results in tables
- See basic visual summaries
- Read plain-language interpretations of the results

## Data

The app uses semi-synthetic data created for demonstration purposes.

Included datasets:

- data/facilities.csv
- data/outbreak_events.csv
- data/weekly_respiratory_activity.csv
- data/lab_testing.csv

## Key Files

- app.py
- requirements.txt
- README.md
- data/

## How to Run Locally

Install the required packages:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py

## Current Free-Text Questions Supported

1. Which facility type had the highest total number of cases?
2. Which disease had the most outbreaks?
3. Which health zone had the highest average RSV percent positivity?

## Safety Notes

This prototype includes a basic SQL safety checker. It is designed to allow only safe SELECT queries and block potentially unsafe SQL operations such as DROP, DELETE, UPDATE, INSERT, and other modifying commands.

## Limitations

- The current free-text workflow is rule-based, not powered by a live AI/LLM model.
- Only selected question patterns are supported.
- The data are synthetic/semi-synthetic and should not be interpreted as real surveillance findings.
- The app is a prototype and not intended for operational public health decision-making.

## Future Development

Planned future improvements may include:

- Broader natural-language question handling
- Optional AI/LLM integration
- More public health indicators
- Additional charts and dashboards
- User-facing documentation
- Deployment through Streamlit Community Cloud

## Author

Developed by Abdul Wajid as part of a public health data science and AI assistant prototype project.
