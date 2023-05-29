import requests
import pandas as pd

def get_item(item_id):
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
        "itemId": item_id
    }    
  })

  res = req.json()
  return res['data']['item']

def get_item_df(item):
  df = pd.DataFrame(item['prices'])
  df['createdAt'] = df["createdAt"].astype(int)
  df['createdAt'] = pd.to_datetime(df['createdAt'], unit='ms')
  df.rename(columns={'price': 'Price', 'createdAt': 'Date'}, inplace=True)
  return df