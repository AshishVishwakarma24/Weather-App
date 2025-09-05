from flask import Flask, render_template, request
from weather import main as get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """render main page with weather info"""
    data, forecast, error = None, None, None

    if request.method == "POST":
        city = request.form.get("cityName")
        state = request.form.get("stateName")
        country = request.form.get("countryName")
        units = request.form.get("units", "metric")  # default to Celsius

        try:
            data, forecast = get_weather(city, state, country, units)
            if not data:  # no data returned → invalid city
                error = f"Could not find weather for '{city}'. Try another city."
        except Exception as e:
            # catch network/API errors
            error = "Something went wrong. Please try again later."

    return render_template("index.html", data=data, forecast=forecast, error=error)


if __name__ == "__main__":
    app.run(debug=True)
