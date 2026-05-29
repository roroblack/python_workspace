import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd
code = get_company_code('경동나비엔')
price_data = fdr.DataReader(code, '2001-01-01', '2023-12-31’)
# 2차원 데이터로 가공
dates = price_data.index
close_prices = price_data['Close']
new_df = pd.DataFrame({'Date': dates, 'Close': close_prices})
new_df['Year'] = new_df['Date'].dt.year
new_df['Month'] = new_df['Date'].dt.month
average_close = new_df.groupby(['Year', 'Month'])['Close'].mean( )
average_close.head( )
average_close_pivot = average_close.reset_index( ).pivot(index='Month’,
columns='Year', values='Close’)
# 히트맵
plt.imshow(average_close_pivot,
cmap='viridis',
interpolation='nearest')
plt.title("Heatmap using Matplotlib")
plt.colorbar( )
plt.show( )