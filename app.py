from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# ---------------- Preprocessing ----------------
def preprocess_zomato_data(zomato_file, country_file):
    country_df = pd.read_excel(country_file)
    zomato_df = pd.read_csv(zomato_file, encoding='latin-1')
    df = zomato_df.merge(country_df, how='left', on='Country Code')
    df = df.drop_duplicates()
    df['Cuisines'] = df['Cuisines'].fillna("Not Available")

    binary_cols = ['Has Table booking', 'Has Online delivery', 'Is delivering now']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    rating_map = {"Excellent": 5, "Very Good": 4, "Good": 3, "Average": 2, "Poor": 1}
    df["Rating score"] = df["Rating text"].map(rating_map)

    df['Primary Cuisine'] = df['Cuisines'].apply(lambda x: x.split(",")[0] if x != "Not Available" else "Not Available")
    df.rename(columns={"Country": "Country Name"}, inplace=True)
    df['Currency'] = df['Currency'].str.strip()

    def price_bucket(cost):
        if cost < 500:
            return "Low"
        elif cost < 1500:
            return "Medium"
        else:
            return "High"

    df['Price Bucket'] = df['Average Cost for two'].apply(price_bucket)
    df['Popularity Score'] = df['Votes'] * df['Aggregate rating']
    return df

# ---------------- Filtering ----------------
def filter_restaurants(df, cuisine=None, city=None, price=None, min_rating=0, table_booking=None, online_delivery=None):
    results = df.copy()
    if cuisine:
        results = results[results['Primary Cuisine'].str.contains(cuisine, case=False, na=False)]
    if city:
        results = results[results['City'].str.contains(city, case=False, na=False)]
    if price:
        results = results[results['Price Bucket'].str.lower() == price.lower()]

    results = results[results['Aggregate rating'] >= min_rating]

    if table_booking is not None:
        results = results[results['Has Table booking'] == table_booking]
    if online_delivery is not None:
        results = results[results['Has Online delivery'] == online_delivery]

    return results[['Restaurant Name','City','Primary Cuisine','Price Bucket','Aggregate rating','Votes']].head(10)

# ---------------- Load Data ----------------
cleaned_df = preprocess_zomato_data("data/zomato.csv", "data/Country-Code.xlsx")

# ---------------- Flask API Route ----------------
@app.route("/search", methods=["GET"])
def search():
    cuisine = request.args.get("cuisine")
    city = request.args.get("city")
    price = request.args.get("price")
    min_rating = float(request.args.get("min_rating", 0))
    
    table_booking = request.args.get("table_booking")
    if table_booking is not None:
        table_booking = True if table_booking.lower() == "yes" else False
    
    online_delivery = request.args.get("online_delivery")
    if online_delivery is not None:
        online_delivery = True if online_delivery.lower() == "yes" else False

    results = filter_restaurants(
        cleaned_df,
        cuisine=cuisine,
        city=city,
        price=price,
        min_rating=min_rating,
        table_booking=1 if table_booking else None,
        online_delivery=1 if online_delivery else None
    )

    return jsonify(results.to_dict(orient="records"))

# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(debug=True)
