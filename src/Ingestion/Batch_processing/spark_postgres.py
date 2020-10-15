''' code to write the data into the database '''

import os
from pyspark.sql import SparkSession

# postgreSQL parameters
pg_usr = os.getenv('PGSQL_USER')
pg_pw = os.getenv('PGSQL_PW')
pg_url = os.getenv('PGSQL_URL')


# initializing spark
spark = SparkSession \
   .builder \
   .appName("Sending data to postgres") \
   .config("spark.jars", "/home/ubuntu/postgresql-42.2.16.jar") \
   .getOrCreate()


# betting odds data
df1 = spark.read.csv('files1.csv', header = True)
df1  = df1.drop('B365H', 'B365D','B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA','WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA')

# Changing data types to match created table in database
def odds_data_type(df):

    changedTypedf = df.withColumn("dataid", df["dataid"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("AwayTeam", df["AwayTeam"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("FTAG", df["FTAG"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("HomeTeam", df["HomeTeam"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("week", df["week"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("FTAG", df["FTAG"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("FTHG", df["FTHG"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("Gameweek_id", df["Gameweek_id"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("amount", df["amount"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("bet_company", df["bet_company"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("bet_type", df["bet_type"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("country", df["country"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("game_id", df["game_id"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("name", df["name"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("number_clicks", df["number_clicks"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("odds", df["odds"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("season", df["season"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("session", df["session"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("Time_spent", df["Time_spent"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("year", df["year"].cast('integer'))
    changedTypedf = changedTypedf.withColumn("Date", df["Date"].cast('varchar(30)'))
    
    return(changedTypedf)


newdf = odds_data_type(df1)

# writing to database
newdf.write \
   .format("jdbc") \
   .option("url", pg_url) \
   .option("dbtable", "table1") \
   .option("user", pg_usr) \
   .option("password",pg_pw) \
   .option("driver", "org.postgresql.Driver") \
   .mode('overwrite').save()

# printing schema for validation
newdf.printSchema()


# clickstream Data
df2 = spark.read.csv('files2.csv', header = True)

# Changing data types to match created table in database
def clickstream_data_type(df):

    changedTypedf2 = df2.withColumn("game_id", df2["game_id"].cast('integer'))
    changedTypedf2 = changedTypedf2.withColumn("session", df["session"].cast('integer'))
    changedTypedf2 = changedTypedf2.withColumn("time_spent", df["time_spent"].cast('integer'))
    changedTypedf2 = changedTypedf2.withColumn("number_clicks", df["number_clicks"].cast('integer'))
    changedTypedf2 = changedTypedf2.withColumn("amount", df["amount"].cast('integer'))
    changedTypedf2 = changedTypedf2.withColumn("odds", df["odds"].cast('integer'))

    return(changedTypedf2)

new_df2 = clickstream_data_type(df2)

# writing to database
new_df2.write \
   .format("jdbc") \
   .option("url", pg_url) \
   .option("dbtable", "table2") \
   .option("user", pg_usr) \
   .option("password", pg_pw) \
   .option("driver", "org.postgresql.Driver") \
   .mode('append').save()

# printing schema for validation
new_df2.printSchema()