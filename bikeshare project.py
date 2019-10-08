import time
import math
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {
    'all':0,
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

DAY_DATA = {
    'all':0,
    'sunday': 1,
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in CITY_DATA:
        city = input('What city? ')

    print('city:', city)

    city_file = CITY_DATA.get(city.lower())
    print('city file:', city_file)

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in MONTH_DATA:
        month = input('What month? ')

    print('month:', month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.lower() not in DAY_DATA:
        day = input('What day? ')

    print('day:', day)

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    df['Start Station'] = df['Start Station']
    df['End Station'] = df['End Station']
    df['Start To End Station'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']

    b = 5
    
    while True:
        print(df[0:b])
        b += 5
        
        more_data = input('\nWould you like more rows? Enter yes or no.\n')
        if more_data.lower() != 'yes':
            break

    #print(df)
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print("\nTime Statistics:\n")
    print('Most Popular Month:', popular_month, )
    print('Most Popular Day of Week:', popular_dow)
    print('Most Popular Hour:', popular_hour)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


    return

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_es = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    popular_trip = df['Start To End Station'].mode()[0]

    print("\nStation Statistics:\n")
    print('Most Popular Start Station:', popular_ss)
    print('Most Popular End Station:', popular_es)
    print('Most Popular Trip:', popular_trip)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print()
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_tt = df['Trip Duration'].sum()

    # display mean travel time
    mean_tt = df['Trip Duration'].mean()

    print("\nDuration Statistics:\n")
    print('Total Travel Time:', total_tt, 'minutes')
    print('Mean Travel Time:', mean_tt, 'minutes')
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:    
        user_types = df['User Type'].value_counts()
    else:
        user_types = "There is no data associated with this Data Set for 'Subcription Status'"

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
    else:
        gender_types = "There is no data associated with this Dataset for 'Gender'"

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
    else:
        earliest_year = "N/A"
        recent_year = "N/A"
        common_year = "N/A"
        

    print("\nUser Statistics:\n")
    print(user_types)
    print()
    print(gender_types)
    print('Earliest Subscriber Birth Year:', earliest_year)
    print('Most Recent Subscriber Birth Year:', recent_year)
    print('Most Common Subscriber Birth Year:', common_year)
    print("This took %s seconds." % (time.time() - start_time))
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
