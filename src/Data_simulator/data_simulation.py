''' File to simulate fake clickstream and orders data on C5 instance and send it back to s3 '''
#pip install tqdm (record time of simulation)
#pip install faker (generate fake names)
#pip install boto3 (sending data to S3)


import numpy as np
import pandas as pd
import datetime
import random
from tqdm import tqdm
import warnings
from faker import Faker
import boto3
warnings.filterwarnings('ignore')


# reading in data from s3 to simulate 
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
my_bucket = resource.Bucket('betsight') 

# reading odds and games Data
obj = client.get_object(Bucket='betsight', Key='data/database.csv')
data = pd.read_csv(obj['Body'])
 

# Generating list of 10000 unique users for website
fake = Faker('en_US')
names= []
while((len(set(names)) < 10000)):
    names.append(fake.name())
    
list_names = set(names)
list_names = list(list_names)


# Function to generate fake data 
def data_simulator(df, year):
    """ input: df -> dataframe of games played and all odds displayed(database)
               year -> year to geenrate data 
       
        output: final dataset(game_id, bet_type, bet_company, amount, number_clicks, amount, time_spent, user_names, session_id)
        
        Generating 50,000 bets and sessions per year
    """
    
    #initializing dataframe    
    clickstream_data = pd.DataFrame()
    df = df[df.year ==  year]

    #unique games for the year
    games = list(df.game_id)
    Game_id = []
    
    #kinds of bets
    bet_type = ['H', 'A', 'D']
    bet = []
    
    #all companies
    companies = ['B365','BW','IW','PS','VC','WH']
    bet_company = []
    
    
    amount  = []
    number_clicks  = []
    time_spent  = []
    user_names = []
    
    # simulating data 
    for _ in range(50000):
        user_names.append(random.choice(list_names))
        time_spent.append(random.randrange(100, 2500, 50))
        number_clicks.append(random.randrange(5, 30))
        amount.append(random.randrange(50, 8000, 50))
        bet_company.append(random.choice(companies))
        bet.append(random.choice(bet_type))
        Game_id.append(random.choice(games))
    
    # simulating 50,000 unique session ID's
    session_id = []
    while(len(set(session_id)) < 50000):
        session_id.append(random.randrange(1892377, 32903499))
    
    list_sessions = set(session_id)
    list_sessions = list(list_sessions)
    
    
    clickstream_data['game_id'] = Game_id
    clickstream_data['name'] = user_names
    clickstream_data['session'] = list_sessions
    clickstream_data['time_spent'] = time_spent
    clickstream_data['number_clicks'] = number_clicks
    clickstream_data['amount'] = amount
    clickstream_data['bet_company'] = bet_company
    clickstream_data['bet_type'] = bet
    
    
    return(clickstream_data)
    

# running simulation for all years
CS = pd.DataFrame()
for i in tqdm(range(2000,2021)):
    data = data_simulator(database, 2000)
    CS = CS.append(data)
 
# appending purchased odds data to simulated web sessions
final = pd.DataFrame()
CS = CS.sort_values(by = ['game_id'])
games = set(CS['game_id'])
for game in games:
    df = database[database.game_id == game]
    new_df = CS[CS.game_id ==  game]
    new_df = new_df.reset_index(drop = True)
    odds = []
    for i in range(len(new_df)):
        bets = str(new_df['bet_company'][i] + new_df['bet_type'][i])
        odds.append(df[bets])
    
    new_df['odds'] = odds
    final= final.append(new_df)
    
# storing copy on instance
final.to_csv('path/simulated_data.csv')

# sending data back to S3
obj = client.put_object(Bucket='betsight', Key='path/simulated_data.csv')


