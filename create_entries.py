import random
from datetime import datetime, timedelta
import pandas as pd

def create_entries_df(num_entries, floors, start_date, end_date):
    """
    Create a DataFrame with simulated entries, where each entry contains a timestamp, entry floor, and exit floor.
    
    The entry and exit floors are biased based on the time of day:
        - Morning (before 10:00 AM) and post-lunch (1:00 PM - 2:00 PM) entries have a higher likelihood of being on floor 1.
        - Lunchtime (12:00 PM - 1:30 PM) and evening (after 3:30 PM) exits are also biased towards floor 1.
        - Other times have a lower bias towards floor 1.
    
    Parameters:
        num_entries (int): The number of entries to generate.
        floors (int): The total number of floors.
        start_date (datetime): The start of the time range for generating timestamps.
        end_date (datetime): The end of the time range for generating timestamps.
        
    Returns:
        pd.DataFrame: A DataFrame containing the generated entries, sorted by timestamp.
    """
    
    def random_date(start, end):
        """Generate a random datetime between `start` and `end`."""
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)
    
    def biased_floor_selection(floors, bias_floor, bias_probability):
        """Select a floor with a given bias probability for the bias_floor."""
        return bias_floor if random.random() < bias_probability else random.randint(2, floors)

    data = []
    
    for _ in range(num_entries):
        timestamp = random_date(start_date, end_date)
        
        # Determine bias based on time of day
        if timestamp.hour < 10 or 13 <= timestamp.hour < 14:
            entry_floor = biased_floor_selection(floors, 1, 0.7)
        else:
            entry_floor = biased_floor_selection(floors, 1, 0.2)
        
        if (timestamp.hour == 12 and timestamp.minute >= 0) or \
           (timestamp.hour == 13 and timestamp.minute <= 30) or \
           (timestamp.hour >= 15 and timestamp.minute >= 30):
            exit_floor = biased_floor_selection(floors, 1, 0.7)
        else:
            exit_floor = biased_floor_selection(floors, 1, 0.2)
        
        # Ensure entry_floor and exit_floor are not the same
        while entry_floor == exit_floor:
            exit_floor = random.randint(1, floors)
        
        data.append([timestamp, entry_floor, exit_floor])
    
    df = pd.DataFrame(data, columns=['Timestamp', 'Entry_Floor', 'Exit_Floor']).sort_values('Timestamp')
    return df