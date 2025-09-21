from pathlib import Path
import pandas as pd

# Base folder = folder where this script lives
BASE_DIR = Path(__file__).resolve().parent

# Paths to the files
country_path = BASE_DIR / "data" / "Country-Code.xlsx"  # <-- .xlsx
zomato_path = BASE_DIR / "data" / "zomato.csv"

print("Looking for:", country_path)
print("Looking for:", zomato_path)

# Check if files exist
if not country_path.exists():
    raise FileNotFoundError(f"Country code file not found: {country_path}")
if not zomato_path.exists():
    raise FileNotFoundError(f"Zomato file not found: {zomato_path}")

# Load files
country_df = pd.read_excel(country_path)  # read Excel
zomato_df = pd.read_csv(zomato_path, encoding="latin-1")

# Merge on Country Code
df = zomato_df.merge(country_df, how="left", on="Country Code")

print(df.head())
