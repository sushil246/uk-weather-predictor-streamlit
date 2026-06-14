# UK Weather Predictor

This Streamlit app uses historical London weather data from the Open-Meteo archive API to train a simple temperature prediction model.

## What it does

- Downloads hourly 2025 temperature data for London from Open-Meteo
- Cleans the CSV and adds time-based features
- Trains a simple regression model using `scikit-learn`
- Allows the user to select a date and hour for a temperature prediction
- Displays dataset preview, model performance metrics, and a daily temperature trend plot

## Files

- `app.py` - the Streamlit application
- `requirements.txt` - Python dependencies for deployment
- `README.md` - this documentation

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

3. Open the URL shown by Streamlit in your browser.

## Deploy to Streamlit Cloud

1. Push the `uk_weather_app` folder to a public GitHub repository.
2. Go to https://share.streamlit.io/ and sign in.
3. Create a new app, select the repo, branch, and set the path to `uk_weather_app/app.py`.
4. Deploy and use the public URL.
