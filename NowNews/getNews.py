import os
from dotenv import load_dotenv
import requests
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

NEWS_URL = "https://newsapi.org/v2/top-headlines"

def setup_articles(category):
    params = {
        "country": "us",
        "category": category,
        "apiKey": API_KEY
    }
    return get_articles(params)

def get_articles(params):
    response = requests.get(NEWS_URL, params=params)
    if response.status_code != 200:
        print(f"Error fetching articles: {response.status_code}")
        return []

    all_news = response.json().get('articles', [])
    articles = [
        {
            "title": news["title"],
            "description": news["description"],
            "source": news["source"]["name"],
            "url": news["url"],
        }
        for news in all_news
    ]
    return articles

def prepare_data():
    categories = ["technology", "business", "health", "science"]
    data = []
    for category in categories:
        articles = setup_articles(category)
        for article in articles:
            data.append({"Category": category, "Source": article["source"]})
    return pd.DataFrame(data)


data_df = prepare_data()

# Creating Dash app
app = Dash(__name__)

# Create bar chart for article count by category
category_fig = px.bar(
    data_df.groupby("Category").size().reset_index(name="Article Count"),
    x="Category",
    y="Article Count",
    title="Article Count by Category",
    labels={"Article Count": "Number of Articles"}
)

# Create pie chart for sources
source_counts = data_df["Source"].value_counts().reset_index(name="Count")
source_counts.rename(columns={"index": "Source"}, inplace=True)

source_fig = px.pie(
    source_counts,
    values="Count",
    names="Source",  # Use the renamed column
    title="Source Distribution"
)

# Defining layout
app.layout = html.Div(children=[
    html.H1(children="NowNews Dashboard"),
    html.Div(children="Visualizing trending topics and sources."),
    dcc.Graph(
        id="category-graph",
        figure=category_fig
    ),
    dcc.Graph(
        id="source-graph",
        figure=source_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
