# FeatureEngineering.py
import pandas as pd

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

    df['Primary Cuisine'] = df['Cuisines'].apply(
        lambda x: x.split(",")[0] if x != "Not Available" else "Not Available"
    )
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


def filter_restaurants(
    df, cuisine=None, city=None, price=None,
    min_rating=0, table_booking=None, online_delivery=None
):
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

    return results[['Restaurant Name', 'City', 'Primary Cuisine', 
                    'Price Bucket', 'Aggregate rating', 'Votes']].head(10)
