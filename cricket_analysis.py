import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define path where your CSV files are stored
data_path = r'E:\Education\3rd Year\3-2\Data Science Lab\Cricket_Data_Analysis'

# Load CSV files
odi_matches = pd.read_csv(os.path.join(data_path, 'odi_Matches_Data.csv'))
odi_fow = pd.read_csv(os.path.join(data_path, 'odi_Fow_Card.csv'))
odi_partnership = pd.read_csv(os.path.join(data_path, 'odi_Partnership_Card.csv'))
players_info = pd.read_csv(os.path.join(data_path, 'players_info.csv'))
odi_batting = pd.read_csv(os.path.join(data_path, 'odi_Batting_Card.csv'))
odi_bowling = pd.read_csv(os.path.join(data_path, 'odi_Bowling_Card.csv'))

# Data inspection
print(odi_matches.shape)
print(odi_matches.columns)
print(odi_matches.dtypes)

print(odi_fow.shape)
print(odi_partnership.shape)
print(players_info.shape)
print(odi_batting.shape)
print(odi_bowling.shape)

print(odi_matches.head())
print(players_info.head())

# Check for missing values
print(odi_matches.isnull().sum())
print(odi_fow.isnull().sum())
print(odi_partnership.isnull().sum())
print(players_info.isnull().sum())
print(odi_batting.isnull().sum())
print(odi_bowling.isnull().sum())

# Fill missing values
odi_matches['Team1 Name'] = odi_matches['Team1 Name'].fillna('Unknown')
odi_matches['Team2 Name'] = odi_matches['Team2 Name'].fillna('Unknown')

# Drop rows with missing values
odi_matches = odi_matches.dropna()

# Remove duplicates
odi_matches = odi_matches.drop_duplicates()
odi_fow = odi_fow.drop_duplicates()
odi_partnership = odi_partnership.drop_duplicates()
players_info = players_info.drop_duplicates()
odi_batting = odi_batting.drop_duplicates()
odi_bowling = odi_bowling.drop_duplicates()

# Top 10 Teams Played Most Matches
teams = pd.concat([odi_matches['Team1 Name'], odi_matches['Team2 Name']])
top_teams = teams.value_counts().head(10)
print(top_teams)

# Total Matches Per Year
odi_matches['Match Date'] = pd.to_datetime(odi_matches['Match Date'])
odi_matches['Year'] = odi_matches['Match Date'].dt.year

matches_per_year = odi_matches['Year'].value_counts().sort_index()
print(matches_per_year)

# Line Graph - Matches Played Per Year
plt.figure(figsize=(10,5))
sns.lineplot(x=matches_per_year.index, y=matches_per_year.values)
plt.title('Matches Played Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Matches')
plt.show()

# Bar Chart - Top Teams
plt.figure(figsize=(10,5))
sns.barplot(x=top_teams.index, y=top_teams.values)
plt.title('Top 10 Teams with Most Matches')
plt.xlabel('Teams')
plt.ylabel('Number of Matches')
plt.xticks(rotation=45)
plt.show()

# Data types
print("odi_matches:\n", odi_matches.dtypes)
print("odi_batting:\n", odi_batting.dtypes)
print("odi_bowling:\n", odi_bowling.dtypes)
print("odi_partnership:\n", odi_partnership.dtypes)
print("odi_fow:\n", odi_fow.dtypes)
print("players_info:\n", players_info.dtypes)

# Convert dob to datetime
players_info['dob'] = pd.to_datetime(players_info['dob'], errors='coerce')

# Create dictionary for player ID to Name
player_dict = players_info.set_index('player_id')['player_name'].to_dict()

# Map to batting, bowling, partnership, fow datasets
odi_batting['Batsman Name'] = odi_batting['batsman'].map(player_dict)
odi_batting['Bowler Name'] = odi_batting['bowler'].map(player_dict)

odi_bowling['Bowler Name'] = odi_bowling['bowler id'].map(player_dict)

odi_partnership['Player 1'] = odi_partnership['player1'].map(player_dict)
odi_partnership['Player 2'] = odi_partnership['player2'].map(player_dict)

odi_fow['Player Name'] = odi_fow['player'].map(player_dict)

# Top 10 Run Scorers
top_scorers = odi_batting.groupby('Batsman Name')['runs'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_scorers.values, y=top_scorers.index)
plt.title('Top 10 ODI Run Scorers')
plt.xlabel('Runs Scored')
plt.ylabel('Batsman')
plt.show()

# Top 10 Wicket Takers
top_bowlers = odi_bowling.groupby('Bowler Name')['wickets'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index)
plt.title('Top 10 ODI Wicket Takers')
plt.xlabel('Wickets Taken')
plt.ylabel('Bowler')
plt.show()

# Most Wins by Teams
team_wins = odi_matches['Match Winner'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=team_wins.values, y=team_wins.index)
plt.title('Top 10 Teams With Most ODI Wins')
plt.xlabel('Wins')
plt.ylabel('Team Name')
plt.show()

# Top 5 Highest Partnerships
top_partnerships = odi_partnership.sort_values(by='partnership runs', ascending=False).head(5)

print(top_partnerships[['Player 1', 'Player 2', 'partnership runs', 'Match ID']])

# Fall of Wickets Count (Top 10 Players)
wicket_counts = odi_fow['Player Name'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=wicket_counts.values, y=wicket_counts.index)
plt.title('Top 10 Most Frequent FOW Batsmen')
plt.xlabel('Times Out')
plt.ylabel('Player')
plt.show()

# Extras Given by Team
team_extras = odi_matches.groupby('Team1 Name')['Team1 Extras Rec'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=team_extras.values, y=team_extras.index)
plt.title('Top 10 Teams Giving Most Extras')
plt.xlabel('Extras')
plt.ylabel('Team Name')
plt.show()

# Toss Winner vs Match Winner
same = odi_matches[odi_matches['Toss Winner'] == odi_matches['Match Winner']]
same_percent = (len(same) / len(odi_matches)) * 100
print(f"Toss winner also won the match in {same_percent:.2f}% of cases")

# Country-wise Player Production
players_info['country_id'].unique()

country_mapping = {
    1.0: 'India',
    2.0: 'Australia',
    3.0: 'England',
    4.0: 'Pakistan',
    5.0: 'South Africa',
    6.0: 'New Zealand',
    7.0: 'Sri Lanka',
    8.0: 'West Indies',
    9.0: 'Bangladesh',
    10.0: 'Zimbabwe',
    11.0: 'Afghanistan',
    12.0: 'Ireland',
    13.0: 'Netherlands',
    14.0: 'Kenya',
    15.0: 'Scotland',
    16.0: 'UAE',
    17.0: 'Canada',
    18.0: 'USA'
}

players_info['country_name'] = players_info['country_id'].map(country_mapping)

country_players = players_info['country_name'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=country_players.values, y=country_players.index)
plt.title('Top 10 Countries Producing Most Players')
plt.xlabel('Number of Players')
plt.ylabel('Country')
plt.show()

# Most Popular Stadiums for ODIs
stadium_count = odi_matches['Match Venue (Stadium)'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=stadium_count.values, y=stadium_count.index)
plt.title('Top 10 Most Popular ODI Stadiums')
plt.xlabel('Number of Matches Hosted')
plt.ylabel('Stadium Name')
plt.show()

# Tamim Iqbal Career Analysis
selected_player = 'Tamim Iqbal'
player_id = players_info[players_info['player_name'] == selected_player]['player_id'].values[0]
print(f"Player ID of {selected_player} is: {player_id}")

player_batting = odi_batting[odi_batting['batsman'] == player_id]

total_runs = player_batting['runs'].sum()
total_balls = player_batting['balls'].sum()
batting_average = total_runs / player_batting[player_batting['isOut'] == 'Yes'].shape[0]
matches_played = player_batting['Match ID'].nunique()

print(f"Batting Analysis for {selected_player}:")
print(f"Total Matches Played: {matches_played}")
print(f"Total Runs Scored: {total_runs}")
print(f"Total Balls Faced: {total_balls}")
print(f"Batting Average: {round(batting_average, 2)}")

player_bowling = odi_bowling[odi_bowling['bowler id'] == player_id]

total_wickets = player_bowling['wickets'].sum()
total_overs = player_bowling['overs'].sum()

print(f"\nBowling Analysis for {selected_player}:")
print(f"Total Wickets: {total_wickets}")
print(f"Total Overs Bowled: {total_overs}")

plt.figure(figsize=(10,6))
sns.lineplot(x='Match ID', y='runs', data=player_batting, marker='o', label='Runs Scored')
plt.title(f"Tamim Iqbal's Career Runs Over Matches")
plt.xlabel('Match ID')
plt.ylabel('Runs Scored')
plt.show()

best_match = player_batting.loc[player_batting['runs'].idxmax()]
print(f"\nBest Match Performance for {selected_player}:")
print(f"Match ID: {best_match['Match ID']}")
print(f"Runs Scored: {best_match['runs']}")
