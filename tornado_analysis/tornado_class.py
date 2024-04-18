import pandas as pd

class tornado_class:
    def __init__(self, file_name):
        """
        Initialises tornado_class. Reads tornado data from csv file to Pandas dataframe and applies 
        clean_data method each time a new instance of the class is made. 

        Args:
            file_name (str): The path to the csv file containing tornado data.
        """
        self.df = pd.read_csv(file_name, index_col=0)
        self.clean_data()

    def clean_data(self):
        """
        Cleans the dataframe by converting datetime column to datetime datatype, converting any 
        alternative longitude values to the conventional format and removing 'F' or 'EF' prefixes 
        from the fujita_scale column.

        Modifies the dataframe in place.
        """
        self.df['datetime'] = pd.to_datetime(self.df['datetime'], errors='coerce')
        self.df['lon'] = self.df['lon'].apply(lambda x: x-360 if x > 180 else x)
        self.df['fujita_scale'] = self.df['fujita_scale'].astype(str)
        self.df['fujita_scale'] = self.df['fujita_scale'].str.replace(r'(EF|F)', '', regex=True)
        self.df['fujita_scale'] = pd.to_numeric(self.df['fujita_scale'], errors='coerce')

    def date_filter(self, start_date, end_date):
        """
        Filters the dataframe to give rows within a specified date range.

        Args:
            start_date (str): The start date of the desired date range, inclusive.
            end_date (str): The end date of the desired date range, inclusive.

        Returns:
            Pandas dataframe: A filtered dataframe within the specified date range.
        """
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = self.df[(self.df['datetime'] >= start_date) & (self.df['datetime'] <= end_date)]
        return df

    def worst_tornadoes(self, start_date, end_date):
        """
        For a given date range, finds the tornado within that range with the highest Fujita scale
        rating and returns a dataframe containing all rows (including lon, lat, grid_id and datetime) 
        with an equivalently high Fujita rating, sorted by date in descending order.

        Args:
            start_date (str): The start date of the desired date range, inclusive.
            end_date (str): The end date of the desired date range, inclusive.

        Returns:
            Pandas dataframe: A dataframe of the worst historical tornadoes within the input date 
            range, sorted by date.
        """

        df = self.date_filter(start_date, end_date)
        max_fuj = df['fujita_scale'].max()
        df = df[df['fujita_scale'] == max_fuj]
        df = df.sort_values(by='datetime', ascending=False)
        return df

    def multiple_grid_count(self, start_date, end_date):
        """
        Counts the number of unique tornado events that have moved through multiple grids.

        Args:
            start_date (str): The start date of the desired date range, inclusive.
            end_date (str): The end date of the desired date range, inclusive.

        Returns:
            int: The number of unique tornadoes that have moved through more than one grid.
        """
        df = self.date_filter(start_date, end_date)
        grid_counts = df.groupby('event_id')['grid_id'].nunique()
        moving_ind = grid_counts[grid_counts > 1].index
        multiple_grid_count = len(moving_ind)
        return multiple_grid_count

    def grid_severity_probability(self, grid_id, fujita_scale, start_date, end_date):
        """
        Calculates the probability of a tornado occurring with at least a certain Fujita scale rating in 
        a specified grid, given the formula in the task description.

        Args:
            grid_id (int): The grid_id to calculate the probability for.
            fujita_scale (int): The minimum Fujita rating to calculate the probability for.
            start_date (str): The start date of the desired date range, inclusive.
            end_date (str): The end date of the desired date range, inclusive.

        Returns:
            float: The probability of a tornado occurrence in the given grid_id with at least the given 
            Fujita scale.
        """
        df = self.date_filter(start_date, end_date)
        df = df[df['grid_id'] == grid_id]
        df = df[df['fujita_scale'] >= fujita_scale]
        unique_event_count = df['event_id'].nunique()
        day_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1 #(inclusive of last day)
        probability = unique_event_count / day_count
        return probability