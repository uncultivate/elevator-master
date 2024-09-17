import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def wait_times_histogram(wait_times):
    plt.style.use('fivethirtyeight')
    # Create a frequency distribution chart (histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(wait_times, bins=range(0, max(wait_times) + 2), kde=False)
    
    # Add labels and title
    plt.xlabel('Wait Time')
    plt.ylabel('Frequency')
    plt.title('Elevator Wait Times Histogram')
    
    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_mean_floor_by_half_hour(df):
    """
    Plot the mean entry and exit floor values by half-hour intervals.

    This function creates a new column in the DataFrame representing half-hour intervals based on the 'Timestamp' column.
    It then calculates the mean 'Entry_Floor' and 'Exit_Floor' values for each half-hour interval and plots these values.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Timestamp', 'Entry_Floor', and 'Exit_Floor' columns.
        
    Returns:
        None
    """
    # Create a new column for half-hour intervals
    df['half_hour'] = df['Timestamp'].dt.floor('30min')

    # Group by the half-hour intervals and calculate the mean for 'Entry_Floor' and 'Exit_Floor'
    mean_values = df.groupby('half_hour')[['Entry_Floor', 'Exit_Floor']].mean()

    # Set the plot style
    plt.style.use('fivethirtyeight')

    # Plot the mean values
    plt.figure(figsize=(10, 6))
    plt.plot(mean_values.index, mean_values['Entry_Floor'], marker='o', label='Mean Entry')
    plt.plot(mean_values.index, mean_values['Exit_Floor'], marker='o', label='Mean Exit')

    # Add labels and title
    plt.xlabel('Time of Day')
    plt.ylabel('Floor')
    plt.title('Mean Entry and Exit Values by Half-Hour Interval')
    plt.xticks(mean_values.index, labels=mean_values.index.strftime('%H:%M'), rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Display the plot
    plt.show()

# Function to award points based on inverse index
def award_points(df):
    # Sort by Average Wait in ascending order
    df_sorted = df.sort_values(by='Average Wait').reset_index(drop=True)
    # Award points based on the inverse of the index
    df_sorted['Points'] = range(len(df_sorted)-1, -1, -1)
    final_df = df_sorted[['Name', 'Points']].sort_values('Points', ascending=False)
    final_df.index = final_df.index + 1
    return final_df