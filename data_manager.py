
import pandas as pd
import os

DATA_FILE = 'habits.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return pd.DataFrame(columns=['habit', 'date', 'status'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_habit(habit_name):
    df = load_data()
    if habit_name not in df['habit'].unique():
        new_habit_df = pd.DataFrame({'habit': [habit_name], 'date': [pd.NaT], 'status': [pd.NA]})
        df = pd.concat([df, new_habit_df], ignore_index=True)
        save_data(df)
        return True
    return False

def update_habit_status(habit_name, date, status):
    df = load_data()
    # Remove existing entry for the same habit and date to avoid duplicates
    df = df[~((df['habit'] == habit_name) & (df['date'] == date))]
    
    new_entry = pd.DataFrame([{'habit': habit_name, 'date': date, 'status': status}])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

def get_habits():
    df = load_data()
    return df['habit'].unique().tolist()


