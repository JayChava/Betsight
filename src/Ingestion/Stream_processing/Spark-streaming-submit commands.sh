#########################
# Spark_submit commands #
#########################


# command to start consumer on spark streaming and send data to postgresql
spark-submit --jars ./postgresql-42.2.16.jar \
             --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.7,org.apache.kafka:kafka-clients:2.3.1 \
             --master spark://10.0.0.11:7077 spark_consumer.py