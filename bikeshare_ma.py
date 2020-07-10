import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
   
    while True:
        city = input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n")
        if city.title() not in ('New York City', 'Chicago', 'Washington'):
            print("Please type in the city you want to filter by again.")
            continue
        else:
            break

    # get user input for month (all)

    month_list=['January','February','March','April','May','June','July','August','September','October','November','December','All']
    while True:
        month =input("\nWhich month would you like to filter by?\nType 'all' if you don't want to filter by month.\n") 
        month=month.title()
        if month not in month_list:
            print("Please type in your preference correctly.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nAre you looking for a particular day?\nType 'all' if you don't want to filter by a particular day.\n")
        day = day.title()
        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'):
            print("Please type in your preference correctly.")
            continue
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June','july','august','september','october','november','december']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    month_mode = df['month'].mode()[0]
    print('Most Common Month:', month_mode)

    # display the most common day of week

    day_mode = df['day_of_week'].mode()[0]
    print('Most Common day:', day_mode)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    hour_mode = df['hour'].mode()[0]
    print('Most Common Hour:', hour_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', start_station)

    # display most commonly used end station

    end_station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip

    combination_station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Commonly used combination of start and end station trips:', start_station, " & ", end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time/86400, " Days")

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    # Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth

    try:
      earliest_year = df['Birth Year'].min()
      print('\nEarliest Year:', earliest_year)
    except KeyError:
      print("\nEarliest Year is not available for this month.")

    try:
      most_recent_year = df['Birth Year'].max()
      print('\nMost Recent Year:', most_recent_year)
    except KeyError:
      print("\nMost Recent Year is not available for this month.")

    try:
      most_common_year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', most_common_year)
    except KeyError:
      print("\nMost Common Yearis not available for this month.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
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