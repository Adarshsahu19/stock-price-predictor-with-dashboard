from __future__ import annotations

import pandas as pd
from prophet import Prophet


def prepare_prophet_data(stock_data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert stock data into Prophet's required format:
    ds -> date column
    y  -> target value to forecast
    """
    prophet_df = stock_data[["Date", "Close"]].copy()
    prophet_df.columns = ["ds", "y"]
    prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])
    prophet_df["y"] = pd.to_numeric(prophet_df["y"], errors="coerce")
    prophet_df = prophet_df.dropna().sort_values("ds")

    if len(prophet_df) < 60:
        raise ValueError("Not enough historical data is available to train the forecast model.")

    return prophet_df


def train_prophet_model(prophet_data: pd.DataFrame) -> Prophet:
    """
    Train a Prophet model on historical closing prices.
    """
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
    )
    model.fit(prophet_data)
    return model


def forecast_stock_prices(stock_data: pd.DataFrame, periods: int = 30) -> pd.DataFrame:
    """
    Train the model and forecast future prices for the given number of days.
    """
    prophet_data = prepare_prophet_data(stock_data)
    model = train_prophet_model(prophet_data)

    # Prophet builds a future dataframe using the trained time frequency.
    future_dates = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future_dates)

    forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper", "trend"]].copy()
    forecast["ds"] = pd.to_datetime(forecast["ds"])

    # Merge actual historical prices so we can compare actual vs forecast on one chart.
    forecast = forecast.merge(prophet_data, on="ds", how="left")
    return forecast
