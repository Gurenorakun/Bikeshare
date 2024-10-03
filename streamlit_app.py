import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the data
day = pd.read_csv('./sample_data/day.csv')
hour = pd.read_csv('./sample_data/hour.csv')

# Clean the data
day.drop(['holiday'], axis=1, inplace=True)
hour.drop(['holiday'], axis=1, inplace=True)

# Change column header names
day.rename(columns={'dteday':'dateday', 'yr':'year', 'mnth':'month', 'weekday':'day', 'weathersit':'weather',
                    'temp':'temperature', 'atemp':'temperature_a', 'hum':'humidity', 'casual':'casual_user',
                    'registered':'registered_user', 'cnt':'total_user'}, inplace=True)
hour.rename(columns={'dteday':'dateday', 'yr':'year', 'mnth':'month', 'weekday':'day', 'weathersit':'weather',
                    'temp':'temperature', 'atemp':'temperature_a', 'hum':'humidity', 'casual':'casual_user',
                    'registered':'registered_user', 'cnt':'total_user'}, inplace=True)

# Change data types
datetime_columns = ['dateday']
for column in datetime_columns:
  day[column] = pd.to_datetime(day[column])
  hour[column] = pd.to_datetime(hour[column])

# Change numeric to the corresponding values
def change_season(x):
    if x == 1:
        return 'Spring'
    elif x == 2:
        return 'Summer'
    elif x == 3:
        return 'Fall'
    else:
        return 'Winter'

day['season'] = day['season'].apply(change_season)
hour['season'] = hour['season'].apply(change_season)

change_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul',
                8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

day['month'] = day['month'].map(change_month)
hour['month'] = hour['month'].map(change_month)

day_change = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}

day['day'] = day['day'].map(day_change)
hour['day'] = hour['day'].map(day_change)

def change_year(x):
    if x == 0:
        return 2011
    else:
        return 2012

day['year'] = day['year'].apply(change_year)
hour['year'] = hour['year'].apply(change_year)

def change_workingday(x):
    if x == 0:
        return 'Weekend/Holiday'
    else:
        return 'Working day'

day['workingday'] = day['workingday'].apply(change_workingday)
hour['workingday'] = hour['workingday'].apply(change_workingday)

def change_weather(x):
    if x == 1:
        return 'Clear'
    elif x == 2:
        return 'Misty'
    elif x == 3:
        return 'Rain'
    else:
        return 'Heavy Rain'

day['weather'] = day['weather'].apply(change_weather)
hour['weather'] = hour['weather'].apply(change_weather)

# Create the app
st.title('Bike Sharing Dashboard')

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(['Hourly Bike Sharing', 'Daily Bike Sharing', 'Annual Bike Sharing', 'Weather Impact'])

# Tab 1: Hourly Bike Sharing
with tab1:
    fig = px.bar(hour, x='hr', y='total_user', color='workingday', barmode='group')
    st.write('Hourly Bike Sharing')
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Daily Bike Sharing
with tab2:
    sum_casual_user = day.groupby("day").casual_user.sum().sort_values( ascending=False).reset_index()
    sum_registered_user = day.groupby("day").registered_user.sum().sort_values(ascending=False).reset_index()
    daily_user = pd.merge(
        left=sum_casual_user,
        right=sum_registered_user,
        how="left",
        left_on="day",
        right_on="day"
    )
    daily_user_type = daily_user.melt(id_vars='day', var_name='user_type', value_name='user_count')
    fig = px.bar(daily_user_type, x='day', y='user_count', color='user_type', barmode='group')
    st.write('Daily Bike Sharing ')
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Annual Bike Sharing
with tab3:
    monthly_counts = day.groupby(by=["month","year"]).agg({
        "total_user": "sum"
    }).reset_index()
    fig = px.line(monthly_counts, x='month', y='total_user', color='year')
    st.write('Annual Bike Sharing')
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Weather Impact
with tab4:
    fig = px.bar(day, x='weather', y='total_user')
    st.write('Weather Impact')
    st.plotly_chart(fig, use_container_width=True)
    
    # Create a matplotlib plot
    fig, ax = plt.subplots()
    ax.bar(day['weather'], day['total_user'])
    ax.set_title('Weather Impact')
    ax.set_xlabel('Weather')
    ax.set_ylabel('Total User')
    st.pyplot(fig)