# Python libraries
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Local imports
from BitbayApi import Bitbay_Api

to_timestamp = datetime.now()
from_timestamp = to_timestamp - timedelta(days=1)
to_timestamp = int(datetime.timestamp(to_timestamp)*1000//1)
from_timestamp = int(datetime.timestamp(from_timestamp)*1000//1)

api = Bitbay_Api()
res = api.get(item=f'trading/candle/history/BTC-PLN/3600?from={from_timestamp}&to={to_timestamp}')
headers = list(res['items'][0][1].keys())
headers.insert(0,'Time')

items_list = []
for item in res['items']:
    item[0] = datetime.fromtimestamp(int(item[0])/1000)
    item.extend(list(item[1].values()))
    item.pop(1)
df = pd.DataFrame(res['items'], columns=headers)

fig = go.Figure(data=[go.Candlestick(x=df['Time'],
                                     open=df['o'],
                                     high=df['h'],
                                     low=df['l'],
                                     close=df['c'],
                                     )])
fig.update_layout(
    title='Bitcoin last 24h price',
    xaxis_title='Time',
    yaxis_title='Price [PLN]'
)
fig.write_image('summary_chart.svg')


Report_contents = f"""
<!DOCTYPE html>
<html>
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Test report</title>
    <link rel="stylesheet" href="df_style.css">
</head>
<body>
    <h1>Bitcoin 24h price report</h1>
    <h5>Created automatically using Python</h5>
    <h3>Report contain data in range: {datetime.fromtimestamp(int(from_timestamp/1000))} - {datetime.fromtimestamp(int(to_timestamp/1000))}</h1>
    <img src="summary_chart.svg" alt="Summary chart" width="800">
    <h3>Tabular data</h3>
    {df.to_html()}
</body>
</html>
"""

file = open("Report.html","w")
file.write(Report_contents)
file.close()