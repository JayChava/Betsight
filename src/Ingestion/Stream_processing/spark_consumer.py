''' code to read data from kafka topic run streaming functions and sending it to postgreSQl '''

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

pg_usr = os.getenv('PGSQL_USER')
pg_pw = os.getenv('PGSQL_PW')
pg_url = os.getenv('PGSQL_URL')

print("Kafka topic strtuctured streaming application starting")

# initializing spark session
spark = SparkSession \
        .builder \
        .appName("Structuredstreaming") \
        .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Creating DataFrame representing the stream of input
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "ec2-18-205-239-177.compute-1.amazonaws.com:9092") \
  .option("subscribe", "new") \
  .option("startingOffsets", "earliest") \
  .load()


print("schema df:")
df.printSchema()

df1 = df.selectExpr("CAST(value AS STRING)", "timestamp")

# function to write to database
def write_db(df,table):

    df.write \
    .format("jdbc") \
    .option("url", "pg_url") \
    .option("dbtable", table) \
    .option("user", "pg_usr") \
    .option("password",'pg_pw') \
    .option("driver", "org.postgresql.Driver") \
    .mode("append").save()




# Defining Schema of data
gameweek_table_schema = StructType() \
                .add("dataid", StringType())\
                .add("AwayTeam", StringType())\
                .add("Date", StringType())\
                .add("FTAG", StringType())\
                .add("FTHG", StringType())\
                .add("Gameweek_id", StringType())\
                .add("HomeTeam", StringType())\
                .add("amount", StringType())\
                .add("bet_company", StringType())\
                .add("bet_type", StringType())\
                .add("country", StringType())\
                .add("game_id", StringType())\
                .add("name", StringType())\
                .add("number_clicks", StringType())\
                .add("odds", StringType())\
                .add("season", StringType())\
                .add("session", StringType())\
                .add("time_spent", StringType())\
                .add("week", StringType())\
                .add("year", StringType())\
                .add("winnings", StringType())

# creating dataframe from stream
df2 = df1.select(from_json(col("value"), gameweek_table_schema).alias("gameweek_details"), "timestamp")
df3 = df2.select("gameweek_details.*", "timestamp")
print('schema df3')
df3.printSchema()



def write_postgresql_main(df, epochId):
    df.persist()

    changedTypedf = df.withColumn("dataid", df["dataid"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("AwayTeam", df["AwayTeam"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("HomeTeam", df["HomeTeam"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("winnings", df["winnings"].cast('integer'))
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

    write_db(changedTypedf, 'clickstream')   

    df.unpersist()

    pass


query_main = df3.writeStream \
            .foreachBatch(write_postgresql_main)\
            .outputMode("update")\
            .start()

#query_main.awaitTermination(20)

#bets placed per gameweek
df_bp = df3.groupby("Gameweek_id","timestamp").count()
df_bp.printSchema()


def write_postgresql_count(df, epochId):
    df.persist()

    changedTypedf = df.withColumn("Gameweek_id", df["Gameweek_id"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("count", df["count"].cast('integer'))

    write_db(changedTypedf, 'gameweek_count') 

    df.unpersist()

    pass


query1 =  df_bp.writeStream \
            .foreachBatch(write_postgresql_count)\
            .outputMode("update")\
            .start()

query1.awaitTermination(20)


# total amount spent by user for gameweek

df_am = df3.groupby("Gameweek_id","timestamp").agg({"amount": "sum"}).select("Gameweek_id","timestamp", col("sum(amount)").alias("total amount"))
print('schema total amount spent by users for gameweek')
df_am.printSchema()

def write_postgresql_gw_amt(df, epochId):
    df.persist()

    changedTypedf = df.withColumn("Gameweek_id", df["Gameweek_id"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("total_amount", df["total_amount"].cast('integer'))

    write_db(changedTypedf, 'gameweek_amount')

    df.unpersist()

    pass


query2 =  df_am.writeStream \
            .foreachBatch(write_postgresql_gw_amt)\
            .outputMode("update")\
            .start()

query2.awaitTermination(20)

# total profit for gameweek
df_gw = df3.groupby("Gameweek_id",'timestamp').agg({"winnings": "sum"}).select("Gameweek_id","timestamp", col("sum(winnings)").alias("total profit"))
print('schema total profit for gameweek')
df_gw.printSchema()

def write_postgresql_gw_win(df, epochId):
    df.persist()

    changedTypedf = df.withColumn("Gameweek_id", df["Gameweek_id"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("profit", df["profit"].cast('integer'))

    write_db(changedTypedf, "gameweek_profit")
    
    df.unpersist()
    pass


query3 =  df_gw.writeStream \
            .foreachBatch(write_postgresql_gw_win)\
            .outputMode("update")\
            .start()

query3.awaitTermination(20)

# total profit per company
df_bc = df3.groupby("bet_company","timestamp").agg({"winnings": "sum"}).select("bet_company","timestamp",col("sum(winnings)").alias("profit"))
print('schema total profit per company')
df_bc.printSchema()


def write_postgresql_com_win(df, epochId):

    df.persist()

    changedTypedf = df.withColumn("bet_company", df["bet_company"].cast('varchar(30)'))
    changedTypedf = changedTypedf.withColumn("profit", df["profit"].cast('integer'))

    write_db(changedTypedf, "company_profit")

    df.unpersist()

    pass


query4 =  df_bc.writeStream \
            .foreachBatch(write_postgresql_com_win)\
            .outputMode("update")\
            .start()


#total profit for company per gameweek
df_bcgw = df3.groupby(["Gameweek_id","bet_company"]).agg({"winnings": "sum"})
print("total profit for company per gameweek")
df_bcgw.printSchema()

query5 = df_bcgw.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query5.awaitTermination(20)


# Mean Number of clicks per gameweek
df_clicks = df3.groupby("Gameweek_id").agg({"number_clicks": "mean"})
print('schema Mean Number of clicks per gameweek')
df_clicks.printSchema()

query6 = df_clicks.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query6.awaitTermination(20)

# Mean time spent per gameweek
df_TS = df3.groupby("Gameweek_id").agg({"time_spent": "mean"})
print('schema Mean time spent per gameweek')
df_TS.printSchema()

query7 = df_TS.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query7.awaitTermination(20)


# Mean Number of clicks per country
df_nc = df3.groupby("country").agg({"number_clicks": "mean"})
print('schema Mean Number of clicks per country')
df_nc.printSchema()

query8 = df_nc.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query8.awaitTermination(20)


# Mean time spent per country
df_tc = df3.groupby("Gameweek_id").agg({"time_spent": "mean"})
print('schema Mean time spent per country')
df_tc.printSchema()

query9 = df_tc.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query9.awaitTermination(20)



# total amount for country
df_ta = df3.groupby("country").agg({"amount": "sum"}).select("country", col("sum(amount)").alias("total amount"))
print('schema total amount for country')
df_ta.printSchema()

query10 = df_ta.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

query10.awaitTermination(20)




# betsWithWatermark = df_bp.withWatermark("betstime", "2 hours")
# amountWithWatermark = df_am.withWatermark("amounttime", "2 hours")

# joined_df = betsWithWatermark.join(
#   amountWithWatermark, expr(""Gameweek_id = Gameweek_id AND
#   betstime >= amounttime AND
#   betstime <= amounttime + interval 1 hour
#     ""),
#   "inner"
# )

# queryjoin = joined_df.writeStream \
#         .outputMode("complete") \
#         .format("console") \
#         .start()
