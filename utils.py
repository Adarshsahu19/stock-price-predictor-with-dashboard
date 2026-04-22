from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def get_dashboard_metrics(stock_data: pd.DataFrame, forecast_data: pd.DataFrame) -> dict:
    latest_close = float(stock_data["Close"].iloc[-1])
    future_forecast = forecast_data[forecast_data["y"].isna()].copy()
    final_forecast = float(future_forecast["yhat"].iloc[-1])
    predicted_change_pct = ((final_forecast - latest_close) / latest_close) * 100

    if predicted_change_pct > 2:
        trend_label = "Uptrend"
    elif predicted_change_pct < -2:
        trend_label = "Downtrend"
    else:
        trend_label = "Sideways"

    return {
        "latest_close": latest_close,
        "forecast_close": final_forecast,
        "predicted_change_pct": predicted_change_pct,
        "trend_label": trend_label,
    }


def create_historical_chart(stock_data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=stock_data["Date"],
            y=stock_data["Close"],
            mode="lines",
            name="Close Price",
            line={"color": "#1f77b4", "width": 2},
        )
    )
    fig.update_layout(
        title="Historical Closing Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def create_forecast_chart(forecast_data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=forecast_data["ds"],
            y=forecast_data["y"],
            mode="lines",
            name="Actual Close",
            line={"color": "#2ca02c", "width": 2},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_data["ds"],
            y=forecast_data["yhat"],
            mode="lines",
            name="Forecast",
            line={"color": "#d62728", "width": 2},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_data["ds"],
            y=forecast_data["yhat_upper"],
            mode="lines",
            line={"width": 0},
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_data["ds"],
            y=forecast_data["yhat_lower"],
            mode="lines",
            line={"width": 0},
            fill="tonexty",
            fillcolor="rgba(214, 39, 40, 0.15)",
            name="Forecast Range",
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title="Actual vs Forecasted Stock Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig
