# -*- coding: utf-8 -*-

import pandas as pd

# Grab the example orders data from a published Google Sheet tab (File > Publish to the web ... > Comma-separated values (.csv))
orders = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vSJqWQejvfq9iLypDVsUc6GLC8ZvJ8TCCTU9n0Nqq2ogxpbHEnsdIWOyJkTXY9K-l2gLeAJJyPJNRx0/pub?gid=0&single=true&output=csv",
    parse_dates=["Start", "End"])

# Data overview
orders.info()
orders.tail()



# Build timeseries dataframe

# Build Timeseries of dates
timeseries_array = [orders.Start.min()]

# Add one day to last entry in array
while timeseries_array[-1] < orders.End.max():
  timeseries_array.append( timeseries_array[-1] + pd.Timedelta("1 days") )

del timeseries_array[timeseries_array.index(max(timeseries_array))]
  
# Add orders count column
order_count = []
for i in timeseries_array:
  order_count.append(None)

timeseries = pd.DataFrame(data = {"Date": timeseries_array, "Orders": order_count})

timeseries.head()

# Count open orders per date in timeseries
for index, row in timeseries.iterrows():
   
  count = 0
  
  for ind, r in orders.iterrows():
    
    cond_1 = r.Start <= row.Date  # Order started on or before date
    cond_2 = r.End >= row.Date    # Order ended on or after date
    cond_3 = r.End == pd.NaT      # Order does not have an end date (remains active)
    
    if cond_1 and (cond_2 or cond_3):
      count += 1

  timeseries.at[index, "Orders"] = count
  
timeseries.info()
timeseries.head()
