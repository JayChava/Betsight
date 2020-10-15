#########################################
# Useful Commands for the Kafka cluster #
#########################################


# Create two topics sessions and requests on kafka-cluster
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic topic1
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic topic2

# Change number of partitions for a topic
 /usr/local/kafka/bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic topic1--partitions 10
 
# Console producer to write messeages to a topic
/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic topic1

# console consumer to check the contents of a topic
/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic topic1

# delete a topic
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic1

# describe a topic
/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic topic1