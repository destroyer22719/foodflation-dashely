import requests
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import datetime

itemId = "09c325f8-2fc0-483b-a33d-92851d96b525"

req = requests.post("https://545xzt1qw1.execute-api.us-east-1.amazonaws.com",
  json={
    "query": """
      query getItem($itemId: ID!) {
        item(id: $itemId) {
          name
          imgUrl
          prices {
            createdAt
            price
          }
        }
      }
    """,
    "variables": {
        "itemId": itemId
    }    
  }
)

res = req.json()


df = pd.DataFrame(res['data']['item']['prices'])


df['createdAt'] = df["createdAt"].astype(int)
df['createdAt'] = pd.to_datetime(df['createdAt'], unit='ms')
df.rename(columns={'price': 'Price', 'createdAt': 'Date'}, inplace=True)

print(df.head())

app = Dash(__name__)
app.layout = html.Div([
    html.H1(f"Price History for {res['data']['item']['name']}"),
    html.Img(src=res['data']['item']['imgUrl']),
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='dropdown',
        value='all'
    )
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(days):
    if days == 'all':
        return px.line(df, x="Date", y="Price", title='Price History')
    else:
        return px.line(df[df['Date'] > datetime.datetime.now() - datetime.timedelta(days=int(days))], x="Date", y="Price", title='Price History')
    
if __name__ == '__main__':
    app.run_server(debug=True)