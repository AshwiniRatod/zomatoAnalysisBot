import pandas as pd

def preprocess_zomato_data(zomato_file, country_file, output_file="cleaned_zomato.csv"):
    # Load the country code Excel file
    country_df = pd.read_excel(country_file)

    # Load the Zomato CSV file
    zomato_df = pd.read_csv(zomato_file, encoding='latin-1')

    # Merge datasets on Country Code
    df = zomato_df.merge(country_df, how='left', on='Country Code')

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing Cuisines
    df['Cuisines'] = df['Cuisines'].fillna("Not Available")

    # Map binary columns to 0/1
    binary_cols = ['Has Table booking', 'Has Online delivery', 'Is delivering now']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    # Map rating text to numeric score
    rating_map = {
        "Excellent": 5,
        "Very Good": 4,
        "Good": 3,
        "Average": 2,
        "Poor": 1
    }
    df["Rating score"] = df["Rating text"].map(rating_map)

    # Extract primary cuisine
    df['Primary Cuisine'] = df['Cuisines'].apply(lambda x: x.split(",")[0] if x != "Not Available" else "Not Available")

    # Rename country column
    df.rename(columns={"Country": "Country Name"}, inplace=True)

    # Normalize currency (optional)
    df['Currency'] = df['Currency'].str.strip()

    # Define price bucket
    def price_bucket(cost):
        if cost < 500:
            return "Low"
        elif cost < 1500:
            return "Medium"
        else:
            return "High"

    df['Price Bucket'] = df['Average Cost for two'].apply(price_bucket)

    # Calculate popularity score
    df['Popularity Score'] = df['Votes'] * df['Aggregate rating']

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Preprocessing complete! Cleaned dataset saved as {output_file}")

    return df


# Run the pipeline
cleaned_df = preprocess_zomato_data("data/zomato.csv", "data/Country-Code.xlsx")
print(cleaned_df.head())
