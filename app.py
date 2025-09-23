from flask import Flask, request, render_template
import pandas as pd
from FeatureEngineering import preprocess_zomato_data, filter_restaurants

app = Flask(__name__)

# Load Data once
cleaned_df = preprocess_zomato_data("data/zomato.csv", "data/Country-Code.xlsx")

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        cuisine = request.form.get("cuisine")
        city = request.form.get("city")
        price = request.form.get("price")
        min_rating = float(request.form.get("min_rating", 0))
        table_booking = request.form.get("table_booking") == "yes"
        online_delivery = request.form.get("online_delivery") == "yes"

        results = filter_restaurants(
            cleaned_df,
            cuisine=cuisine,
            city=city,
            price=price,
            min_rating=min_rating,
            table_booking=1 if table_booking else None,
            online_delivery=1 if online_delivery else None
        )

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
