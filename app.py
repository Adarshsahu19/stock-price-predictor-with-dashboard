import streamlit as st

from data import fetch_stock_data
from model import forecast_stock_prices
from utils import (
    create_forecast_chart,
    create_historical_chart,
    format_currency,
    get_dashboard_metrics,
)


st.set_page_config(
    page_title="Stock Price Predictor Dashboard",
    page_icon="📈",
    layout="wide",
)


def render_intro() -> None:
    st.title("Stock Price Predictor Dashboard")
    st.write(
        "Analyze the last 5 years of stock prices and forecast the next 30 days "
        "with Prophet, Plotly, and Streamlit."
    )


def render_sidebar() -> tuple[str, bool]:
    st.sidebar.header("Dashboard Controls")
    ticker = st.sidebar.text_input(
        "Enter stock ticker",
        value="AAPL",
        help="Examples: AAPL, TSLA, TCS.NS",
    ).strip().upper()
    run_prediction = st.sidebar.button("Run Prediction", type="primary")

    st.sidebar.markdown("### What this app does")
    st.sidebar.write("- Fetches 5 years of historical data from Yahoo Finance")
    st.sidebar.write("- Trains a Prophet forecasting model")
    st.sidebar.write("- Predicts the next 30 days of closing prices")

    return ticker, run_prediction


def render_metrics(metrics: dict) -> None:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest Close", format_currency(metrics["latest_close"]))
    col2.metric("30-Day Forecast", format_currency(metrics["forecast_close"]))
    col3.metric("Predicted Change", f"{metrics['predicted_change_pct']:.2f}%")
    col4.metric("Trend", metrics["trend_label"])


def render_historical_section(stock_data) -> None:
    st.subheader("Historical Data")
    st.dataframe(stock_data.tail(20), use_container_width=True)
    st.plotly_chart(create_historical_chart(stock_data), use_container_width=True)


def render_forecast_section(forecast_data) -> None:
    st.subheader("Prediction Results")
    preview_columns = ["ds", "yhat", "yhat_lower", "yhat_upper"]
    st.dataframe(forecast_data[preview_columns].tail(30), use_container_width=True)
    st.plotly_chart(create_forecast_chart(forecast_data), use_container_width=True)


def main() -> None:
    render_intro()
    ticker, run_prediction = render_sidebar()

    if not run_prediction:
        st.info("Choose a stock ticker from the sidebar and click 'Run Prediction'.")
        return

    if not ticker:
        st.error("Please enter a valid stock ticker.")
        return

    try:
        with st.spinner(f"Fetching data and training the model for {ticker}...", show_time=True):
            stock_data = fetch_stock_data(ticker)
            forecast_data = forecast_stock_prices(stock_data, periods=30)
            metrics = get_dashboard_metrics(stock_data, forecast_data)
    except ValueError as exc:
        st.error(str(exc))
        return
    except Exception as exc:
        st.error(
            "Something went wrong while processing the stock data. "
            "Please try another ticker."
        )
        st.exception(exc)
        return

    render_metrics(metrics)

    st.markdown("---")
    render_historical_section(stock_data)

    st.markdown("---")
    render_forecast_section(forecast_data)


if __name__ == "__main__":
    main()
