# Script to analyze sleeper league transactions

import requests
import pandas as pd
import json
import os

vdfl_league_id = 650077529041907712
chfl_league_id = 605793964607500288

#user_id = 650077529041907712

# Test API call
##request_str = f"https://api.sleeper.app/v1/league/{vdfl_league_id}/transactions/3"
#request_str = f"https://api.sleeper.app/v1/league/{vdfl_league_id}/rosters"
#print(request_str)
#r = requests.get(request_str).json()
#
#print(r)

print('########################')
df = pd.json_normalize(r)

def userID(username):
    '''
    Gets user ID for a sleeper username
    '''
    url = f"https://api.sleeper.app/v1/user/{username}"
    r = requests.get(url).json()
    print(f'User ID [{username}]:', r['user_id'])
    
    return r['user_id']

#User: andrewbowen19
def getPlayers():
    '''
    Gets table of all players in the nfl
    
    The JSON response is pretty large (~5MB), so you should only call this
    function once and
    '''
    url = f"https://api.sleeper.app/v1/players/nfl"
    r = requests.get(url).json()
    
#    Writing to a file
    with open('players.json','w') as f:
        json.dump(r, f, indent=4)
        
#    Converting to pandas and writing to csv
    df = pd.DataFrame(r).T
    print(df.head())
    df.to_csv('nfl-players.csv')
    
    return df
    
def getDrafts(league_id):
    '''
    Gets drafts for a league
    '''
    url = f"https://api.sleeper.app/v1/league/{league_id}/drafts"
    r = requests.get(url).json()
    
    print(r)
    print(pd.json_normalize(r))
    print(r[0]['draft_id'])
    
    df = pd.json_normalize(r)
    return df
    
def userDrafts(user_id, season):
    '''
    returns draft data for a given user
    
    params:
        user_id: str or int; sleeper user ID number
    '''
    url = f"https://api.sleeper.app/v1/user/{user_id}/drafts/nfl/{season}"
    r = requests.get(url).json()
    
    print(r)
    print(pd.json_normalize(r))
#    print(r[0]['draft_id'])
    
    df = pd.json_normalize(r)
    return df
    
    

def getPicks(draft_id):
    '''
    Gets all picks in a draft
    '''
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"

    r = requests.get(url).json()
    
    df = pd.json_normalize(r)
    print(f'Draft: {draft_id}')
    print('Picks:')

    return df
    
def playerStats(first, last):
    '''
    Scrapes pro-football reference for an individual player's stats
    
    parameters:
        first : str; player first name
        last : str; player last name
        
    returns:
        df : pandas.DataFrame including categorical stats by week for an individual player
    '''
    print(first, last)
    name_cat = last[0]
    name_code = last[0:4] + first[0:2] + "00"
#    print(name_cat, name_code)
    url = f"https://www.pro-football-reference.com/players/{name_cat}/{name_code}.htm#receiving_and_rushing"
    print(url)
#    https://www.pro-football-reference.com/players/P/PittKy00.htm#receiving_and_rushing
    df = pd.read_html(url, header=1, displayed_only=False)[0]
    df = df.loc[:,~df.columns.str.startswith('Unnamed: ')]
#    df.columns = [' '.join(col).strip() for col in df.columns.values]
    print(df.columns)
    
#    print(df.loc[df['Date']=='Upcoming Games'])
#    df = df.loc[:,df.iloc[df['Date']=='Upcoming Games']]
    

    return df
    
    
if __name__=="__main__":
#    getPlayers()
    getDrafts(vdfl_league_id)
    
    draft2021 = 650077529041907713
    picks = getPicks(draft2021)
    userID('andrewbowen19')
#    picks['name'] = picks['metadata.first_name'] + " " + picks['metadata.last_name']
#    print(picks)
##    print(picks.columns)
#
#
#    df = playerStats("Kyle", "Pitts")
#
#    print(df)
#    print('############################################')
#
#    for index, row in picks.iterrows():
#        print(row['metadata.position'])
#        first = row['metadata.first_name']
#        last = row['metadata.last_name']
#
#        try:
#            dat = playerStats(first, last)
#            print(dat)
#            dat.to_csv(os.path.join('.','data', f'player-data-{first}-{last}.csv'))
#        except:
#            print('No stats found.')
#
#        print('-----------------------------------------------')


#Pro-football ref player page
#https://www.pro-football-reference.com/players/P/PittKy00.htm#stats
#https://www.pro-football-reference.com/players/{}/PittKy00.htm#stats


