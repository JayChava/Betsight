''' Code to breakdown directories and organize them gameweek wise '''
#aws s3 cp --recursive s3://betsight data (aws cli command to pull all files from bucket)

#pip install tqdm (record time of pre-processing)
#pip install boto3 (reading/writing data to S3)

import pandas as pd
import boto3
import os
import datetime
from tqdm import tqdm
import boto3
import warnings
warnings.filterwarnings('ignore')


# alternative method to pull all files from s3 

# low-level functional API
client = boto3.client('s3')

# high-level object-oriented API
resource = boto3.resource('s3') 
my_bucket = resource.Bucket('betsight') 

# download file into current directory
for s3_object in my_bucket.objects.all():

    # Need to split s3_object.key into path and file name, else it will give error file not found.
    path, filename = os.path.split(s3_object.key)
    my_bucket.download_file(s3_object.key, filename)



# initializing unique charceters across multiple scraped datasets 
country = ['England', 'Germany', 'Netherlands', 'Spain', 'Portugal', 'Greece', 'France', 'Italy', 'Scotland', "Turkey"] 
leagues = ['EPL','Bundesliga', 'Eredivisie', 'La_Liga','Liga_NOS','Super_league_Greece','Ligue_1','Serie_A', 'SPL', 'Super_lig']
item = ['E', 'D', 'N', 'S', 'P', 'G', 'F', 'I',"SC", 'T']
year = ['00','01','02','03','04', '05', '06','07', '08','09', '10', '11', '12', '13', '14', '15', '16' , '17' ,'18' ,'19','20', '21']

#final dataframe
complete = pd.DataFrame()

# iterating through each league
for i in tqdm(range(len(leagues))):
    print(leagues[i])
    
    # iterating through each year
    for j in range(len(year)):
        try:
            # path to file
            path = 'path/'+leagues[i]+'/'+item[i]+'_'+year[j]+'_'+year[j+1]+'.csv'
            data = pd.read_csv(path, error_bad_lines=False, encoding = 'latin1', warn_bad_lines=False)
            
            #dropping null values
            data = data.dropna()
            
            # dropping duplicate values
            data = data.drop_duplicates(subset = ['Div', 'Date', 'HomeTeam', 'AwayTeam'] , keep = 'first') 
        
        except:
            pass
        
        # initializing lists which will be the new cols in final dataframe    
        data['season'] = []
        data['country'] = []
        data['formatted_date'] = []
        data['year'] = []
        data['week'] = []
        
        # iterating through a year's data  to rectify and pre-process columns 
        for k in range(len(data)):
            time = data.Date[k]
            
            # pre-processing date, 8 is the standard length of time for most date formats
            if(len(time) == 8): 
                try:
                    if(time[6:8] == year[j]):
                        data['formatted_date'][k] = time[:6] +'20'+ year[j]
                    elif(time[6:8] == year[j+1]):
                        data['formatted_date'][k] = time[:6] + '20'+ year[j+1]
                    else:
                        pass
                except:
                     pass
                data['formatted_date'][k] = datetime.datetime.strptime(data['formatted_date'][k], '%d/%m/%Y')
            
            elif(time[2:3] == '/' ):
                data['formatted_date'][k] = datetime.datetime.strptime(data.Date[k], '%d/%m/%Y') 
            
            else:
                time = time[2:10]
                time = time.replace('-','/')
                try:
                    if(time[6:8] == year[j]):
                        data['formatted_date'][k] = time[:6] +'20'+ year[j]
                    elif(time[6:8] == year[j+1]):
                        data['formatted_date'][k] = time[:6] + '20'+ year[j+1]
                    else:
                        pass
                except:
                     pass
                data['formatted_date'][k] = datetime.datetime.strptime(data['formatted_date'][k], '%d/%m/%Y')
                
                
            try:    
                data['season'][k] = '20'+year[j]+ '-'+year[j+1]
            except:
                pass
            data['year'][k] = data['formatted_date'][k].year
            data['week'][k] = data['formatted_date'][k].strftime("%V")
            data['country'][k] = country[i]
    
        complete = complete.append(data)

# final dataset
complete = complete[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG','formatted_date', 'country', 'season', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA',
                     'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'season','week','year']]

# dropping duplicates
complete = complete.drop_duplicates(subset = ['HomeTeam', 'AwayTeam', 'formatted_date'])

# creating unique game_id columns
complete['game_id'] = list(range(1,len(df)+1))

# renaming 'formatted_date' column to 'Date'
complete = complete.rename(columns = {'formatted_date': 'Date'})

# storing a copy of the file locally 
complete.to_csv('path/complete.csv')

# sending data back to s3
client.put_object(Bucket='betsight', Key='path/complete.csv')
