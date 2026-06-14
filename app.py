import streamlit as st
import pandas as pd
import requests
from io import StringIO
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_URL = (
    "https://archive-api.open-meteo.com/v1/archive?"
    "latitude=51.5074&longitude=-0.1278&start_date=2025-01-01&"
    "end_date=2025-12-31&hourly=temperature_2m&format=csv"
)


def load_weather_data(url: str) -> pd.DataFrame:
    """Fetch and parse the Open-Meteo London hourly temperature CSV."""
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    csv_text = response.text

    # The Open-Meteo archive CSV includes metadata lines before the header.
    df = pd.read_csv(StringIO(csv_text), skiprows=3, parse_dates=["time"])
    df.columns = [col.strip().replace(" (°C)", "") for col in df.columns]
    df = df.rename(columns={"temperature_2m": "temperature"})
    df = df.dropna(subset=["temperature"])
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hour"] = df["time"].dt.hour
    df["day_of_year"] = df["time"].dt.dayofyear
    df["month"] = df["time"].dt.month
    df["weekday"] = df["time"].dt.weekday
    return df


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    return load_weather_data(DATA_URL)


@st.cache_resource
def train_temperature_model(df: pd.DataFrame):
    df = add_time_features(df)
    X = df[["hour", "day_of_year", "month", "weekday"]]
    y = df["temperature"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", LinearRegression()),
        ]
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred),
    }
    return pipeline, metrics


def build_prediction_row(selected_date, selected_hour: int) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "hour": selected_hour,
                "day_of_year": selected_date.timetuple().tm_yday,
                "month": selected_date.month,
                "weekday": selected_date.weekday(),
            }
        ]
    )


def main():
    st.set_page_config(
        page_title="UK Weather Predictor",
        page_icon="☁️",
        layout="wide",
    )

    st.title("UK Weather Predictor")
    st.write(
        "Use historical London temperature data from Open-Meteo to train a simple model and predict hourly temperatures for a selected date and time."
    )

    data_load_state = st.text("Loading historical weather data...")
    df = get_data()
    data_load_state.text("Historical weather data loaded successfully.")

    st.subheader("Dataset Overview")
    st.write(
        "This dataset contains hourly temperature observations for London (UK) during 2025. "
        "The model uses time-based features to predict temperature." 
    )
    st.dataframe(df.head(), use_container_width=True)

    model, metrics = train_temperature_model(df)
    st.subheader("Model Performance")
    st.metric("Mean Absolute Error", f"{metrics['MAE']:.2f} °C")
    st.metric("R² Score", f"{metrics['R2']:.3f}")

    st.subheader("Predict Temperature")
    with st.form(key="prediction_form"):
        selected_date = st.date_input(
            "Select a date",
            value=pd.to_datetime("2025-06-01").date(),
            min_value=pd.to_datetime("2025-01-01").date(),
            max_value=pd.to_datetime("2025-12-31").date(),
        )
        selected_hour = st.slider("Select an hour", min_value=0, max_value=23, value=12)
        submitted = st.form_submit_button("Predict temperature")

    if submitted:
        input_row = build_prediction_row(selected_date, selected_hour)
        predicted_temp = model.predict(input_row)[0]
        st.success(
            f"Predicted temperature for {selected_date} at {selected_hour:02d}:00 is {predicted_temp:.1f} °C"
        )

    st.subheader("Visualizing Heat Trends")
    daily_mean = df.resample("D", on="time")["temperature"].mean().reset_index()
    st.line_chart(daily_mean.rename(columns={"time": "Date", "temperature": "Mean Temperature (°C)"}).set_index("Date"))

    st.markdown(
        "---\n"
        "**How it works:** The app downloads the Open-Meteo archive CSV, cleans the data, adds time-based features, trains a simple regression model, and predicts temperature for a selected hour."
    )


if __name__ == "__main__":
    main()
