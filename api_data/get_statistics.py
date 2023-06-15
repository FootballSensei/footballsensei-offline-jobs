
from secrets import AUTH_TOKEN
import requests 
import pandas as pd
import time

def get_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0
    
def get_form_points(string):
    sum = 0
    for letter in string:
        sum += get_points(letter)
    return sum    
    

def getTeamPointsInMatchday(team_id, matchday):
    uri = 'https://api.football-data.org/v4/competitions/2021/standings?matchday=' + matchday + '&season=2022'
    headers = { 'X-Auth-Token': AUTH_TOKEN }

    if matchday == '0':
        return 0

    response = requests.get(uri, headers=headers)
    
    for poz in response.json()['standings'][0]['table']:
        if poz['team']['id'] == team_id:
            return poz['points']
        
def getFormInMatchday(team_id, matchday):
    uri = 'https://api.football-data.org/v4/competitions/2021/standings?matchday=' + matchday + '&season=2022'
    headers = { 'X-Auth-Token': AUTH_TOKEN }

    if matchday == '0':
        return 'M', 'M', 'M', 'M', 'M'

    response = requests.get(uri, headers=headers)
    
    for poz in response.json()['standings'][0]['table']:
        if poz['team']['id'] == team_id:
            form = poz['form'].split(',')
            if len(form) < 5:
                rest = (5 - len(form)) * ['M']
                form = form + rest
            return form[0], form[1], form[2], form[3], form[4]

def getGoalDifferenceMatchday(team_id, matchday):
    uri = 'https://api.football-data.org/v4/competitions/2021/standings?matchday=' + matchday + '&season=2022'
    headers = { 'X-Auth-Token': AUTH_TOKEN }

    if matchday == '0':
        return 0

    response = requests.get(uri, headers=headers)
    
    for poz in response.json()['standings'][0]['table']:
        if poz['team']['id'] == team_id:
            return poz['goalDifference']
        
def calculateHMandAM(HM1, HM2, HM3, AM1, AM2, AM3):
    if HM1 == 'W':
        HM1_L = 0
        HM1_D = 0
        HM1_W = 1
        HM1_M = 0
    elif HM1 == 'D':
        HM1_L = 0
        HM1_D = 1
        HM1_W = 0
        HM1_M = 0
    elif HM1 == 'L':
        HM1_L = 1
        HM1_D = 0
        HM1_W = 0
        HM1_M = 0
    else:
        HM1_L = 0
        HM1_D = 0
        HM1_W = 0
        HM1_M = 1
        
    if HM2 == 'W':
        HM2_L = 0
        HM2_D = 0
        HM2_W = 1
        HM2_M = 0
    elif HM2 == 'D':
        HM2_L = 0
        HM2_D = 1
        HM2_W = 0
        HM2_M = 0
    elif HM2 == 'L':
        HM2_L = 1
        HM2_D = 0
        HM2_W = 0
        HM2_M = 0
    else:
        HM2_L = 0
        HM2_D = 0
        HM2_W = 0
        HM2_M = 1
        
    if HM3 == 'W':
        HM3_L = 0
        HM3_D = 0
        HM3_W = 1
        HM3_M = 0
    elif HM3 == 'D':
        HM3_L = 0
        HM3_D = 1
        HM3_W = 0
        HM3_M = 0
    elif HM3 == 'L':
        HM3_L = 1
        HM3_D = 0
        HM3_W = 0
        HM3_M = 0
    else:
        HM3_L = 0
        HM3_D = 0
        HM3_W = 0
        HM3_M = 1
        
    if AM1 == 'W':
        AM1_L = 0
        AM1_D = 0
        AM1_W = 1
        AM1_M = 0
    elif AM1 == 'D':
        AM1_L = 0
        AM1_D = 1
        AM1_W = 0
        AM1_M = 0
    elif AM1 == 'L':
        AM1_L = 1
        AM1_D = 0
        AM1_W = 0
        AM1_M = 0
    else:
        AM1_L = 0
        AM1_D = 0
        AM1_W = 0
        AM1_M = 1
        
    if AM2 == 'W':
        AM2_L = 0
        AM2_D = 0
        AM2_W = 1
        AM2_M = 0
    elif AM2 == 'D':
        AM2_L = 0
        AM2_D = 1
        AM2_W = 0
        AM2_M = 0
    elif AM2 == 'L':
        AM2_L = 1
        AM2_D = 0
        AM2_W = 0
        AM2_M = 0
    else:
        AM2_L = 0
        AM2_D = 0
        AM2_W = 0
        AM2_M = 1
         
    if AM3 == 'W':
        AM3_L = 0
        AM3_D = 0
        AM3_W = 1
        AM3_M = 0
    elif AM3 == 'D':
        AM3_L = 0
        AM3_D = 1
        AM3_W = 0
        AM3_M = 0
    elif AM3 == 'L':
        AM3_L = 1
        AM3_D = 0
        AM3_W = 0
        AM3_M = 0
    else:
        AM3_L = 0
        AM3_D = 0
        AM3_W = 0
        AM3_M = 1
        
    return HM1_L, HM1_D, HM1_W, HM1_M, HM2_L, HM2_D, HM2_W, HM2_M, HM3_L, HM3_D, HM3_W, HM3_M, AM1_L, AM1_D, AM1_W, AM1_M, AM2_L, AM2_D, AM2_W, AM2_M, AM3_L, AM3_D, AM3_W, AM3_M



uri = 'https://api.football-data.org/v4/competitions/2021/matches?season=2022'
headers = {'X-Auth-Token': AUTH_TOKEN}

response = requests.get(uri, headers=headers)
pl_matches = response.json()['matches']

df = pd.DataFrame(columns=['MATCHDATE', 'FTR', 'HTP', 'ATP', 'HM1_L', 'HM1_D', 'HM1_W', 'HM1_M',
                            'HM2_L', 'HM2_D', 'HM2_W', 'HM2_M', 'HM3_L', 'HM3_D', 'HM3_W', 'HM3_M',
                           'HTGD', 'ATGD','DiffFormPts'])

for i in range(127):
    match = pl_matches[i]
    if match['status'] == 'FINISHED':
        if match['score']['winner'] == 'HOME_TEAM':
            FTR = 'H'
        else:
            FTR = 'NH'
    else:
        FTR = 'NA'

    matchday = str(int(match['matchday']) - 1)
    
    matchdate = match['utcDate'][0:10]

    HTP = getTeamPointsInMatchday(match['homeTeam']['id'], matchday)
    ATP = getTeamPointsInMatchday(match['awayTeam']['id'], matchday)
    HM1, HM2, HM3, HM4, HM5 = getFormInMatchday(match['homeTeam']['id'], matchday)
    AM1, AM2, AM3, AM4, AM5 = getFormInMatchday(match['awayTeam']['id'], matchday)
    HTFormString = HM1 + HM2 + HM3
    ATFormString = AM1 + AM2 + AM3
    HTGD = getGoalDifferenceMatchday(match['homeTeam']['id'], matchday)
    ATGD = getGoalDifferenceMatchday(match['awayTeam']['id'], matchday)

    ATFormPts = get_form_points(ATFormString)
    HTFormPts = get_form_points(HTFormString)
    DiffFormPts = HTFormPts - ATFormPts
    
    HM1_L, HM1_D, HM1_W, HM1_M, HM2_L, HM2_D, HM2_W, HM2_M, HM3_L, HM3_D, HM3_W, HM3_M, AM1_L, AM1_D, AM1_W, AM1_M, AM2_L, AM2_D, AM2_W, AM2_M, AM3_L, AM3_D, AM3_W, AM3_M = calculateHMandAM(HM1, HM2, HM3, AM1, AM2, AM3)
    
    new_row = {'MATCHDATE': matchdate, 'FTR': FTR, 'HTP': HTP, 'ATP': ATP, 'HM1_L': HM1_L, 'HM1_D': HM1_D, 'HM1_W': HM1_W, 'HM1_M': HM1_M, 'HM2_L': HM2_L, 'HM2_D': HM2_D, 'HM2_W': HM2_W, 'HM2_M': HM2_M, 'HM3_L': HM3_L, 'HM3_D': HM3_D, 'HM3_W': HM3_W, 'HM3_M': HM3_M, 
                'AM1_L': AM1_L, 'AM1_D': AM1_D, 'AM1_W': AM1_W, 'AM1_M': AM1_M, 'AM2_L': AM2_L, 'AM2_D': AM2_D, 'AM2_W': AM2_W, 'AM2_M': AM2_M, 'AM3_L': AM3_L, 'AM3_D': AM3_D, 'AM3_W': AM3_W, 'AM3_M': AM3_M, 'HTGD': HTGD, 'ATGD': ATGD, 'DiffFormPts': DiffFormPts}

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    time.sleep(60)
    
df.to_csv('matchdata1.csv', index=False)

matchdata1 = pd.read_csv('matchdata1.csv')
matchdata2 = pd.read_csv('matchdata2.csv')
matchdata3 = pd.read_csv('matchdata3.csv')

matchdata = pd.concat([matchdata1, matchdata2, matchdata3], ignore_index=True)

matchdata.to_csv('matchdata.csv', index=False)

from sklearn.preprocessing import scale

normalized_cols = ['HTP', 'ATP', 'HTGD', 'ATGD', 'DiffFormPts']

matchdata_normalized = matchdata.copy()

for col in normalized_cols:
    matchdata_normalized[col] = scale(matchdata_normalized[col])
    
matchdata_normalized.to_csv('matchdata_normalized.csv', index=False)

df = pd.read_csv('matchdata_normalized.csv')

# Create empty lists to store the team names
home_team_names = []
away_team_names = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    match = pl_matches[index]
    home_team_names.append(match['homeTeam']['name'])
    away_team_names.append(match['awayTeam']['name'])

# Add the team name lists as new columns in the DataFrame
df['HomeTeamName'] = home_team_names
df['AwayTeamName'] = away_team_names

df.to_csv('PL_Match_Data.csv', index=False)
    