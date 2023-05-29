from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from item_util import get_item_df, get_item

app = Dash(__name__,)

app.layout = html.Div([
  dcc.Dropdown(
    id='dropdown',
    value='None',
    placeholder="Select an item",
    options=[
      {
        'label': 'Beef Braising Short Ribs',
        'value': '09c325f8-2fc0-483b-a33d-92851d96b525'
      },
      {
        "label": "Kalbi Beef Short Ribs",
        "value": "0f3111e0-1541-4c4c-98c6-a2f07cd61d2f"
      },
      {
        "label": "Beef Short Ribs, Boneless",
        "value": "1ce7624c-60a4-4361-a10f-94aa5f2eb8c7"
      }
    ]
  ),
  html.Div(id='item-info'),
  dcc.Graph(id='graph'),
])

@callback(
  Output('graph', 'figure'),
  Input('dropdown', 'value')
)
def update_graph(item_id):
  if (item_id == "None"):
    return px.line(pd.DataFrame(columns=["Date", "Price"]), x="Date", y="Price")
  item = get_item(item_id)
  return px.line(get_item_df(item), x="Date", y="Price")


@callback(
  Output('item-info', 'children'),
  Input('dropdown', 'value')
)
def update_item_info(item_id):
  if (item_id == "None"):
    return html.Div()
  item = get_item(item_id)
  return html.Div([
    html.H1(item['name']),
    html.Img(src=item['imgUrl'])
  ])


if __name__ == '__main__':
  app.run_server(debug=True)
