import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.skysports.com/premier-league-results/2024-25"

# Try-except block for error handling
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# List to store extracted data
data = []

# Find all occurrences of fixres__header1 (month and year)
months = soup.find_all('h3', class_='fixres__header1')

# Loop through each month section
for month_section in months:
    # Extract month and year
    month_year_text = month_section.text.strip()
    month_name, year = month_year_text.split()
    year = int(year)
    
    # Convert month name to month number
    month = pd.to_datetime(month_name, format='%B').month

    # Find all games within this month section
    current_header = month_section.find_next_sibling('h4', class_='fixres__header2')

    while current_header and current_header.name == 'h4':
        # Extract date from the header
        date_text = current_header.text.strip()
        day = int(date_text.split()[1][:-2])  # Extracting the day number

        # Formatted Date
        match_date = f"{month:02d}/{day:02d}/{year}"

        # Find the corresponding match information
        match_item = current_header.find_next_sibling('div', class_='fixres__item')

        if match_item:
            home_team = match_item.find('span', class_='matches__participant--side1').find('span', class_='swap-text__target').text.strip()
            away_team = match_item.find('span', class_='matches__participant--side2').find('span', class_='swap-text__target').text.strip()

            home_goals = int(match_item.find_all('span', class_='matches__teamscores-side')[0].text.strip())
            away_goals = int(match_item.find_all('span', class_='matches__teamscores-side')[1].text.strip())

            # Determine FTR (Full-Time Result)
            if home_goals > away_goals:
                ftr = 'H'
            elif away_goals > home_goals:
                ftr = 'A'
            else:
                ftr = 'D'

            # Append the extracted information to the data list
            data.append({
                'Season_End_Year': year,
                'wk': None,
                'Date': match_date,
                'Home': home_team,
                'HomeGoals': home_goals,
                'AwayGoals': away_goals,
                'Away': away_team,
                'FTR': ftr
            })

        # Move to the next game or month section
        current_header = match_item.find_next_sibling('h4', class_='fixres__header2') if match_item else None

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('premier_league_results.csv', index=False)

print("Data has been written to 'premier_league_results.csv'.")

