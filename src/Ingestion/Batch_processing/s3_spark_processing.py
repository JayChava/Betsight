'''Reading files from S3 bucket and emforcing schema on them before sendign them to postgreSQL'''

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# bucket details
region = 'us-east-1'
bucket = 'betsight'

# path to files
key1 = 'data/database.csv'
key2 = 'data/CS_data.csv'

# Initializing spark 
sc = SparkContext()
sc._jsc.hadoopConfiguration().set('fs.s3a.endpoint', f's3.amazonaws.com')
spark = SparkSession(sc)

# Reading in the files
def read_file(key):

    s3file = f's3a://{bucket}/{key}'
    df = spark.read.csv(s3file, header= True)
    return(df)
    
df1 = read_file(key1)
df2 = read_file(key2)    

# enforcing schema for first games file
oldColumns = df1.schema.names
newColumns = ['game_id', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D',
              'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA',
              'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'season', 'country', 'date',
              'year', 'week', 'Gameweek_id']

df1 = reduce(lambda df1, idx: df1.withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)), df1)


# enforcing schema for clickstream file
oldcols = df2.schema.names
newcols = ['game_id', 'name', 'session', 'time_spent', 'number_clicks', 'amount','bet_company', 'bet_type', 'odds']

df2 = reduce(lambda df2, idx: df2.withColumnRenamed(oldcols[idx], newcols[idx]), range(len(oldcols)), df2)

# Reading out files to disk
df1.write.csv('file1.csv')
df2.write.csv('file2.csv')
spark.stop()