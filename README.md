# Zomato Chatbot Web Application

A web-based chatbot that helps users find restaurants using Zomato data. Users can filter by cuisine, city, price range, ratings, table booking, and online delivery options.

---

## Features

- **Restaurant Search**: Filter restaurants by cuisine, city, price bucket (Low/Medium/High), minimum rating, table booking, and online delivery.
- **Popularity-based Ranking**: Restaurants are ranked by popularity score (`Votes × Aggregate rating`).
- **Modern Web UI**: Clean and responsive interface with search functionality.
- **Data Preprocessing**: Handles missing values, duplicates, rating conversion, price bucketing, and primary cuisine extraction.

---

## Tech Stack

- **Backend**: Python 3.x, Flask
- **Data Handling**: Pandas, NumPy
- **Frontend**: HTML, CSS (inline / modern design)

---

## Project Structure

zomatoAnalysisBot/
│
├─ app.py # Flask application
├─ FeatureEngineering.py # Preprocessing and filtering functions
├─ data/
│ ├─ zomato.csv # Zomato restaurant dataset
│ └─ Country-Code.xlsx # Country code reference dataset
└─ templates/
└─ index.html # Web page interface


---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YourUsername/zomatoAnalysisBot.git
cd zomatoAnalysisBot
```
2.Create and activate a virtual environment:
python -m venv env
env\Scripts\activate      # Windows
# source env/bin/activate # Mac/Linux

3.Install required packages:

pip install -r requirements.txt

4.Start the Flask server:

python app.py
