
import yfinance as yf

apple = yf.ticker(“AAPL”)

print(apple.major_holders)
print(apple.institutional_holders)
print(apple.recommendations)

recommendations = apple.recommendations
recommendations[recommendations.index > ‘2022-01-01’]