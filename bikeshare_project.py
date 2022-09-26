import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#lists for month and day to check user input validity
month_list=['january', 'february', 'march', 'april', 'may', 'june','all']
weekday_list=['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

#function to validate user input
def check_user_input(user_input,input_type):
    while True:
        input_user_entered=input(user_input).lower()
        try:
            if input_user_entered in ['chicago','new york city','washington'] and input_type == 'c':
                break
            elif input_user_entered in month_list and input_type == 'm':
                break
            elif input_user_entered in weekday_list and input_type == 'd':
                break
            else:
                if input_type == 'c':
                    print("Invalid Input!, input must be: chicago, new york city, or washington")
                if input_type == 'm':
                    print("Invalid Input!, input must be: january, february, march, april, may, june or all")
                if input_type == 'd':
                    print("Invalid Input!, input must be: sunday, ... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_user_entered

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington), and check user input validity
    city = check_user_input("Would you like to see the data for chicago, new york city or washington?\n",'c')
    # get user input for month (all, january, february, ... , june), and check user input validity
    month = check_user_input("For filtering data by specific mounth please enter month name from (january, february, march, april, may, june) otherwise enter 'all'\n", 'm')
    # get user input for day of week (all, monday, tuesday, ... sunday), and check user input validity
    day = check_user_input("For filtering data by specific day please enter day name from (sunday, monday, tuesday, wednesday, thursday, friday, saturday) otherwise enter 'all'\n", 'd')

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
        d_frame - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    d_frame = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    d_frame['Start Time'] = pd.to_datetime(d_frame['Start Time'])

    # extract month, day of week and Hour from Start Time to create new columns
    d_frame['month'] = d_frame['Start Time'].dt.month
    d_frame['day_of_week'] = d_frame['Start Time'].dt.weekday_name
    d_frame['hour'] = d_frame['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        d_frame = d_frame[d_frame['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        d_frame = d_frame[d_frame['day_of_week'] == day.title()]

    return d_frame

def time_stats(d_frame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = d_frame['month'].mode()[0]
    print('Most Common Month is: ', most_common_month)

    #display the most common day of week
    most_common_day = d_frame['day_of_week'].mode()[0]
    print('Most Common Day Of Week is: ', most_common_day)

    #display the most common start hour
    most_common_hour = d_frame['hour'].mode()[0]
    print('Most Common Start Hour Of Day is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(d_frame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_commo_start_station = d_frame['Start Station'].mode()[0]
    print('Most Common Start Station is: ', most_commo_start_station)

    #display most commonly used end station
    most_common_end_station = d_frame['End Station'].mode()[0]
    print('Most Common End Station is: ', most_common_end_station)

    #display most frequent combination of start station and end station trip
    #here we can't use mode, instead we will use group
    #but the result won't be sorted, and for the most frequent combination we need the result to be descending order
    combination_group=d_frame.groupby(['Start Station','End Station'])
    most_frequent_combination_station = combination_group.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip is: ', most_frequent_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(d_frame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = d_frame['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)


    #display mean travel time
    mean_travel_time = d_frame['Trip Duration'].mean()
    print('Mean Travel Time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(d_frame,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('User Types in Data are: ',d_frame['User Type'].value_counts())


    #because columns Gender and Birth Year aren't in washington data, we have to ensure that the city is not washington
    if city != 'washington':
        #Display counts of gender
        print('Counts Of Gender: ',d_frame['Gender'].value_counts())

        #Display earliest, most recent, and most common year of birth
        earliest_year = d_frame['Birth Year'].min()
        print('Earliest Year is: ',earliest_year)

        most_recent_year = d_frame['Birth Year'].max()
        print('Most Recent Year is: ',most_recent_year)

        most_common_year = d_frame['Birth Year'].mode()[0]
        print('Most Common Year is: ',most_common_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#view raw data to user
def show_row_data(d_frame):
    row=0
    while True:
        view_raw_data = input("Would you like to see the raw data? for 'Yes' enter 'Y' and for 'No' enter 'N'.\n").lower()
        #row = 0
        if view_raw_data == "y":
            print(d_frame.iloc[row : row + 6])
            row += 6
        elif view_raw_data == "n":
            break
        else: #validate user input
            print("Sorry! You entered Wrong Input, Kindly try Again!")


def main():

    while True:
        city,month,day = get_filters()
        d_frame = load_data(city,month,day)

        time_stats(d_frame)
        station_stats(d_frame)
        trip_duration_stats(d_frame)
        user_stats(d_frame,city)
        show_row_data(d_frame)
        restart = input('\nWould you like to restart? Enter "y" for yes or "n" for no.\n').lower()
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
