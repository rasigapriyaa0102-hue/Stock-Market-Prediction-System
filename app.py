from flask import Flask, render_template, request
from predict import forecast_stock

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/forecast", methods=["POST"])
def forecast():

    stock = request.form["stock"]

    forecast_dates, forecast_prices, current_price = forecast_stock(stock)

    return render_template(
        "forecast.html",
        stock=stock,
        current_price=current_price,
        dates=forecast_dates,
        prices=forecast_prices,
        
    )


if __name__ == "__main__":
    app.run(debug=True)