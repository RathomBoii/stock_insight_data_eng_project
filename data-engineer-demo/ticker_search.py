import yfinance as yf

tech = yf.Sector("technology")
print(tech.top_companies)   # DataFrame ของ ticker ในกลุ่ม