# BetSight
 _**Real-time web analytics**_


Online sport betting websites see a heavy flow of web traffic on game days, analyzing user engagement data in real-time, provides betting companies useful analysis of user behavior and profit margins.


![dashboard](https://github.com/JayChava/Betsight/blob/master/img/dashboard1.PNG)

## Table of Contents

* [About the Project](#about-the-project)
* [Architecture](#architecture)
* [Installation](#installation)
   * [Spark](#Spark-Cluster)
   * [Kafka](#Kafka-Cluster)
   * [PostgreSQL](#PostgreSQL-Database)
   * [Grafana](#Grafana-Installation)
* [Engineering Challenges](#Engineering-Challenges)
   * [Reducing Latency](#Reducing-Latency)
   * [Handling Late Data](#Handling-Late-Data)
* [Contact](#Contact)


## About the project 


_"Global Sports Betting Market Will Reach USD 155.49 Billion By 2024"_       **-Morgan Stanley**

The current market sits at roughly USD 52 Billion, the growth of the legal sports betting market has exceeded the expectations of many stakeholders and dramatically altered the relationship between sports leagues and the gambling industry. Football(soccer) at 54% owns the highest share of all sports in the betting market, it is extremely popular in the continent of Europe.

Online betting companies rely solely on the performance of their website for profits, data and metrics calculating user engagement, odds purchased and session level metrics are extremely important for making key business decisions. The idea behind the project is to build a real-time dashboard which gives them constant updates and supervision of their websites performance. This dashboard could potentially help people all the way from ground-level business analysts to stakeholders help them monitor and make key decision for their company.

[Slides](https://drive.google.com/file/d/1nSiRXTwhW1k_9Q-33aqQVbN-E3zSdt_r/view?usp=sharing), [Demo]()


## Architecture

![stack](https://github.com/JayChava/Betsight/blob/master/img/tech_stack.PNG)

The tech Stack has two pipelines:

 - Streaming pipeline
    - The streaming pipeline provides us real-time updates on the stream on a gameweek basis.
    - The database structure for the streaming pipeline is leaner and is easier to perform real-time anlaysis on.
    
 - Batching piepline
    - The batching pipeline is part of the future scope of the pipeline, it can allow the ingestion of different datasources which augment the clickstream data for the website.
    - The database created using the batching pipeline is more normalized and provides an easier framework to build an API on.
    

## Installation

![Python 3.8](https://img.shields.io/badge/python-3.7-green.svg)
![Spark](https://img.shields.io/badge/Spark-2.4.7-green)

All using AWS EC2 Instances. 

### Spark Cluster  
- 1 Master 
- 3 Workers

Step 1: Assigning the right Security Groups 
- To allow SSH (Inbound)
- Allow donwloads from internet (Outbound)
- Internal to open communication withing cluster (outbound)

Step 2: Install Java and Scala

```
$ sudo apt update
$ sudo apt install openjdk-8-jre-headless
$ sudo apt install scala   
```
Step 3: Download and Install spark

```
master> $ wget http://mirrors.ibiblio.org/apache/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz (select your own version)
master> $ scp spark-2.4.7-bin-hadoop2.7.tgz worker1:~/ (send to all workers)

Extract the files and move them to /usr/local/spark.

$ tar xvf spark-2.4.7-bin-hadoop2.7.tgz
$ sudo mv spark-2.4.7-bin-hadoop2.7/ /usr/local/spark
$ echo 'export PATH=/usr/local/spark/bin:$PATH' >> ~/.profile
$ source ~/.profile

note: Make sure you have the right python version on instances 
```
### Kafka Cluster
- 1 Master
- 2 Workers

Step 1: Assigning the right Security Groups 
- Similar to above

Step 2: Download [kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.6.0/kafka_2.13-2.6.0.tgz)
   
```
$ tar -xzf kafka_2.13-2.6.0.tgz
$ cd kafka_2.13-2.6.0   
```

Step 3: Start zookeeper and kafka environment

```
# Start the ZooKeeper service
# Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
$ bin/zookeeper-server-start.sh config/zookeeper.properties

# Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties
```

### PostgreSQL Database
- 1 Large instance

Step 1: Assigning the right Security Groups 
- Similar to above

Step 2: Installing postgreSQL

```
$ sudo apt-get update && sudo apt-get -y upgrade
$ sudo apt-get install postgresql postgresql-contrib​
```

Step 3: Running postgreSQL

```
$ sudo -u postgres psql
$ postgres=#\password​
```

### Grafana Installation
- 1 medium sized Instance    

Step 1: Assigning the right Security Groups 
- Similar to above

Step2 : run the following code to download Grafana.

```
#!/bin/bash

$ echo ‘deb https://packages.grafana.com/oss/deb stable main’ >> /etc/apt/sources.list
$ curl https://packages.grafana.com/gpg.key | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get -y install grafana
$ systemctl daemon-reload
$ systemctl start grafana-server
$ systemctl enable grafana-server.service
```

Step3: Change the permission of file by using the command.
```
$ chmod +x grafanainstallation.sh
```

Step4:  execute the shell script to install Grafana by using command.
```
$ ./grafanainstallation.sh
```

Step5: Verify whether Grafana is running or not by using following command
```
$ service grafana-server status
```
If the Grafana Server is not running run the below command to start it.

```
$ service grafana-server start
```

Step6: Take the IP address or DNS of your server and place it on address bar of the any browser along with Grafana port 3000. 

```
https://PublicDNS:3000
```

# Engineering Challenges

### Reducing Latency 

(9s to 5s) 44% reduction in latency, by joining streams in realtime rather than building joins on database or dashboard.


Two topics:
  - Clickstream data [user data, purchase data]
  - Odds data [betting odds, game result]

Merged using left-outer **stream-stream join** in spark structured streaming

![EC1](https://github.com/JayChava/Betsight/blob/master/img/EC1.PNG)

### Handling Late Data

Watermarking is a useful method which helps a Stream Processing Engine to deal with lateness. Basically, a watermark is a threshold to specify how long the system waits for late events. If an arriving event lies within the watermark, it gets used to update a query. Otherwise, if it’s older than the watermark, it will be dropped and not further processed by the Streaming Engine. 
```
withWatermark(eventTime: String, delayThreshold: String): Dataset[T]
```

Watermark set at 15 minutes, optimal time for both my topics to be completely consumed

![EC2](https://github.com/JayChava/Betsight/blob/master/img/EC2.PNG)

**Event time aggregation**, the example below shows aggregation of upto 15 mins late data 
```
parsedData.groupBy(window("timestamp", "15mins")).max(amount)
```

# Contact

## Jayanth Chava


[![Gmail](https://img.shields.io/badge/gmail-D14836?&style=for-the-badge&logo=gmail&logoColor=white)](jaychava95@gmail.com)
[![github](https://img.shields.io/badge/github-%23100000.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/JayChava)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jay-chava/)

