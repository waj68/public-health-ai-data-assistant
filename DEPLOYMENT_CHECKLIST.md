
# Deployment Checklist — Public Health AI Data Assistant

## Required Files

- [x] app.py
- [x] requirements.txt
- [x] README.md
- [x] data/facilities.csv
- [x] data/outbreak_events.csv
- [x] data/weekly_respiratory_activity.csv
- [x] data/lab_testing.csv

## App Checks

- [x] Final Phase 3 app.py cell retained
- [x] Only one active %%writefile app.py cell in notebook
- [x] app.py syntax check completed
- [x] Required data files confirmed
- [x] requirements.txt created
- [x] README.md created
- [x] Deployment file structure confirmed

## Safety Checks

- [x] Uses synthetic/semi-synthetic data only
- [x] No real patient-level data included
- [x] SQL safety checker included
- [x] Only safe SELECT-style queries intended
- [x] Rule-based workflow clearly described
- [x] No external AI/LLM API key required

## Before GitHub Upload

- [ ] Download app.py
- [ ] Download requirements.txt
- [ ] Download README.md
- [ ] Download data folder CSV files
- [ ] Create GitHub repository
- [ ] Upload files using correct folder structure
- [ ] Confirm repository file layout

## Before Streamlit Deployment

- [ ] Connect GitHub repository to Streamlit Community Cloud
- [ ] Select app.py as the main app file
- [ ] Confirm requirements.txt installs correctly
- [ ] Launch deployed app
- [ ] Test predefined questions
- [ ] Test supported free-text questions
- [ ] Confirm charts and tables display correctly

## Current Status

Phase 4 deployment preparation is in progress. Core deployment files have been created and confirmed in the Colab runtime.
