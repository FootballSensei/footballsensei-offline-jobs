
import pyodbc, json, praw
from sentiment import SentimentAnalysis
from datetime import timedelta 
from credentials import * 

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
print(reddit.read_only)

conn = pyodbc.connect(CONNECTION_STRING, autocommit=True)
query = "select * from [dbo].[LineupData] WHERE MONTH(Date) = 8 AND ISNULL(home_sentiment, -1) = -1 ORDER BY Date"

cursor = conn.cursor()
cursor.execute(query)
for x in cursor.fetchall():
    team1_name = x[1]
    team2_name = x[2]
    team1_players = json.loads(x[3])
    team2_players = json.loads(x[4])
    match_date = x[0]
    date_since = match_date - timedelta(days=7)
    date_until = match_date - timedelta(days=2)
    sentim = SentimentAnalysis(team1_name, team2_name, team1_players, team2_players, date_since, date_until, reddit)
    team1_sentiment = sentim.get_team_sentiment(1)
    team2_sentiment = sentim.get_team_sentiment(2)
    team1_positive = sentim.get_team_biased_sentiment(1, 'Positive')
    team2_positive = sentim.get_team_biased_sentiment(2, 'Positive')
    team1_negative = sentim.get_team_biased_sentiment(1, 'Negative')
    team2_negative = sentim.get_team_biased_sentiment(2, 'Negative')
    print (team1_name, team2_name, team1_sentiment, team2_sentiment, team1_positive, team2_positive, team1_negative, team2_negative)
    query = "UPDATE [dbo].[LineupData] SET home_sentiment = ?, away_sentiment = ?, home_positive_score = ?, away_positive_score = ?, home_negative_score = ?, away_negative_score = ? WHERE Date = ? AND HomeTeam = ? AND AwayTeam = ?"
    cursor.execute(query, team1_sentiment, team2_sentiment, team1_positive, team2_positive, team1_negative, team2_negative, match_date, team1_name, team2_name)