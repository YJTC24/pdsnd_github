import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_mode():

    """Starts with greeting of User and is followed by assessing the request of exploration,
     whether user likes to check out the raw data or prefiltered Deep Dive """
    
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        mode = input ("What would you like to explore? Enter 'Raw Data' or 'Deep Dive': ").strip().casefold()
        if mode in ['raw data', 'deep dive']:
            return mode
        else:
            print("Invalid input. Please try again.")

def get_filters():

    """Function to set up filters for Deep Dive Data exploration"""

    """Valid Options"""
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april','may','june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    """CITY INPUT LOOP"""
    while True:
        city = input("Please choose a city (Chicago, New York City, Washington):").strip().casefold()
        if city in valid_cities:
            break
        else:
            print("Invalid input. Please try again.")

    """MONTH INPUT LOOP"""
    while True:
        month = input("Please choose a month (all, January-June):  ").strip().casefold()
        if month in valid_months:
            break
        else:
            print("Invalid input. Please try again.")

    """DAY INPUT LOOP"""
    while True:
        day = input("Please choose a day (all, Sunday-Saturday)").strip().casefold()
        if day in valid_days:
            break
        else:
            print("Inavild input. Please try again.")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """Read the data"""
    df= pd.read_csv(CITY_DATA[city])


    df['Start Time']=pd.to_datetime(df['Start Time'])

    """Extract Month and Day of the week"""
    df['month']=df['Start Time'].dt.month
    df ['day_of_week']=df['Start Time'].dt.day_name()

    """Apply Filter for Month"""
    if month != 'all':
        months=['january','february','march', 'april', 'may', 'june']
        month_index = months.index(month)+1

        df= df[df['month']==month_index]

    """Day Filter"""
    if day != 'all':
        df=df[df['day_of_week'].str.lower()==day]

    return df

def show_raw_data():
    """Displays raw data in chunks of 5 rows."""
    df_raw= pd.concat([
        pd.read_csv(CITY_DATA['chicago']),
        pd.read_csv(CITY_DATA['new york city']),
        pd.read_csv(CITY_DATA['washington'])
    ])

    start = 0
    show_data = input("Would you like to see raw data? Enter yes or no: ").strip().casefold()
    
    while show_data == 'yes':
        print(df_raw.iloc[start:start+5])
        start += 5
        
        show_data = input("Do you want to see the next 5 rows? Enter yes or no: ").strip().casefold()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """display the most common month"""
    most_common_month=df['month'].mode()[0]
    print("Most common month: ", most_common_month)

    """display the most common day of week"""
    most_common_day=df['day_of_week'].mode()[0]
    print("Most common day: ",most_common_day)


    """display the most common start hour"""
    df['hour']=df['Start Time'].dt.hour
    most_common_hour=df['hour'].mode()[0]
    print("Most common start hour: " , most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """display most commonly used start station"""
    most_common_start = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", most_common_start)

    """display most commonly used end station"""
    most_common_end = df['End Station'].mode()[0]
    print("Most commonly used end station: ", most_common_end)


    """display most frequent combination of start station and end station trip"""
    df['trip']=df['Start Station'] + " -> " + df['End Station']
    most_common_trip=df['trip'].mode()[0]
    print("Most frequent trip: ", most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """display total travel time"""
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel_time)


    """ display mean travel time"""
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """Display counts of user types"""
    user_type= df['User Type'].value_counts()
    print("User Types: ", user_type)

    """Display counts of gender"""

    
    if 'Gender' in df.columns:
        gender= df['Gender'].value_counts()
        print("Gender counts: ",gender)
    else:
        print("There is no gender data available")

    """Display earliest, most recent, and most common year of birth"""
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent= int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])

        print ("Earliest birth year: ", earliest)
        print ("Most recent birth year: ", most_recent)
        print ("Most common birth year: ", most_common)
    else: 
        print("There is no birth year data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""main function gathers all functions and puts them into the correct sequence"""

def main():
    while True:
        mode = get_mode()

        if mode == 'raw data':
           show_raw_data()
        else:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

