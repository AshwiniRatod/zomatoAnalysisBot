import pandas as pd

# Load the country code Excel file
country_df = pd.read_excel(r'data/Country-Code.xlsx')

# Load the Zomato CSV file
zomato_df = pd.read_csv(r'data/zomato.csv', encoding='latin-1')

# Merge datasets on Country Code
df = zomato_df.merge(country_df, how='left', on='Country Code')
#print(df.head())

#Remove duplicates
df.drop_duplicates(inplace = True)
print(df.isnull().sum())

