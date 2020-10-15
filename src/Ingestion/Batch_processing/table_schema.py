''' querying table schema from database '''
import os
from pyspark.sql import SparkSession


# postgreSQL parameters
pg_usr = os.getenv('PGSQL_USER')
pg_pw = os.getenv('PGSQL_PW')
pg_url = os.getenv('PGSQL_URL')


# initializing spark session
spark = SparkSession \
   .builder \
   .appName("schema pull") \
   .config("spark.jars", "/home/ubuntu/postgresql-42.2.16.jar") \
   .getOrCreate()

# reading in spark dataframe
df = spark.read \
   .format("jdbc") \
   .option("url", pg_url) \
   .option("dbtable", 'table_name') \
   .option("user", pg_usr) \
   .option("password",pg_pw) \
   .option("driver", "org.postgresql.Driver") \
   .load()

# printing schema
df.printSchema()