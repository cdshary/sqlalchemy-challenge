#!/usr/bin/env python
# coding: utf-8

# In[51]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[52]:


import numpy as np
import pandas as pd


# In[53]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[54]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[55]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[56]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[57]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[58]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[59]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Climate Analysis

# In[60]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from the last data point in the database

# Perform a query to retrieve the data and precipitation scores

# Save the query results as a Pandas DataFrame and set the index to the date column

# Sort the dataframe by date

# Use Pandas Plotting with Matplotlib to plot the data

latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
latest_date

last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
last_twelve_months

p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).                    filter(Measurement.date >= last_twelve_months).                    group_by(Measurement.date).all()
p_results


# In[61]:


precipitation_df = pd.DataFrame(p_results, columns=['Date', 'Precipitation'])
precipitation_df.set_index('Date', inplace=True)
precipitation_df.head()


# In[62]:


ax = precipitation_df.plot(kind='bar', width=3, figsize=(12,8))
plt.locator_params(axis='x', nbins=6)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.tick_params(axis='y', labelsize=16)
ax.grid(True)
plt.legend(bbox_to_anchor=(.3,1), fontsize="16")
plt.title("Precipitation Last 12 Months", size=20)
plt.ylabel("Precipitation (Inches)", size=18)
plt.xlabel("Date", size=18)
plt.show


# ![precipitation](Images/precipitation.png)

# In[63]:


# Use Pandas to calcualte the summary statistics for the precipitation data
#I cant get the statistics for total count other than this because I isolated 365 days (12 months)
precipitation_df.describe()


# ![describe](Images/describe.png)

# In[64]:


# Design a query to show how many stations are available in this dataset?
session.query(Station.id).count()


# In[65]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.

s_results = session.query(Measurement.station, func.count(Measurement.station)).            group_by(Measurement.station).            order_by(func.count(Measurement.station).desc()).all()
s_results


# In[66]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
best_station = s_results[0][0]
session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).                filter(Measurement.station == best_station).all()


# In[67]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
t_results = session.query(Measurement.station, Measurement.tobs).                filter(Measurement.station == best_station).                filter(Measurement.date >= last_twelve_months).all()
tobs_df = pd.DataFrame(t_results)


tobs_df.plot.hist(by='station', bins=12, figsize=(12,8))
plt.grid(True)
plt.title("Temperature Observations for Station " + best_station, fontsize=20)
plt.xlabel("Temperature Reported", fontsize=16)
plt.legend(bbox_to_anchor=(1,1), fontsize=16)

plt.show


# ![precipitation](Images/station-histogram.png)

# In[68]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    c_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).                    filter(Measurement.date >= start_date).                    filter(Measurement.date <= end_date).all()
    return c_results
calc_temps('2017-01-01', '2017-12-31')


# In[69]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
trip_results = calc_temps('2017-07-02', '2017-07-08')
trip_results


# In[70]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
trip_df = pd.DataFrame(trip_results, columns=['Min Temp', 'Avg Temp', 'Max Temp'])
avg_temp = trip_df['Avg Temp']
min_max_temp = trip_df.iloc[0]['Max Temp'] - trip_df.iloc[0]['Min Temp']
avg_temp.plot(kind='bar', yerr=min_max_temp, figsize=(6,8), alpha=0.5, color='coral')
plt.title("Trip Avg Temp", fontsize=20)
plt.ylabel("Temp (F)")
plt.xticks([])
plt.grid(True)
plt.show()


# In[46]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
Results = Session.query(Measurement.station


# ## Optional Challenge Assignment

# In[47]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")


# In[48]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[49]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[50]:


# Plot the daily normals as an area plot with `stacked=False`


# In[ ]:





# In[ ]:





# In[ ]:




