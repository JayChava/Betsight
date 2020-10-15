# BetSight
 _**Real-time web analytics**_


[![python](https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-370/)
[![postgresql](https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/12/index.html)
[![github](https://img.shields.io/badge/github-%23100000.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/JayChava)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jay-chava/)

Online sport betting websites see a heavy flow of web traffic on game days, analyzing user engagement data in real-time, provides betting companies useful analysis of user behavior and profit margins.


![dashboard](https://github.com/JayChava/Betsight/blob/master/img/dashboard1.PNG)

## Table of Contents

* [About the Project](#about-the-project)
* [Architecture](#architecture)
* [Workflow](#workflow)
* [Data](#Data)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project 


_"Global Sports Betting Market Will Reach USD 155.49 Billion By 2024"_       **-Morgan Stanley**

The current market sits at roughly USD 52 Billion, the growth of the legal sports betting market has exceeded the expectations of many stakeholders and dramatically altered the relationship between sports leagues and the gambling industry. Football(soccer) at 54% owns the highest share of all sports in the betting market, it is extremely popular in the continent of Europe.

Online betting companies rely solely on the performance of their website for profits, data and metrics calculating user engagement, odds purchased and session level metrics are extremely important for making key business decisions. The idea behind the project is to build a real-time dashboard which gives them constant updates and supervision of their websites performance. This dashboard could potentially help people all the way from ground-level business analysts to stakeholders to monitor and make key decision for their company.


## Architecture

![stack](https://github.com/JayChava/Betsight/blob/master/img/tech_stack.PNG)

The tech Stack has two pipelines:

 - Streaming pipeline
    - The streaming pipeline provides us real-time updates on the stream on a gameweek basis.
    - The database structure for the streaming pipeline is leaner and is easier to perform real-time anlaysis on.
    
 - Batching piepline
    - The batching pipeline is part of the future scope of the pipeline, it can allow the ingestion of different datasources which augment the clickstream data for the website.
    - The database created using the batching pipeline is more normalized and provides an easier framework to build an API on.
    
## Workflow

1. Extracting the odds data and preprocessing the convoluted time format.
2. Simulating clickstream data on top of odds data using a schema from an ecommerce website.
3. Storing above mentioned data in S3, the data is then further preprocessed and sent to kafka(streaming) and spark(batching).
4. In the batch processing pipeline the data is fit to the postgresql database table schemas and sent through.
5. In the streaming pipeline a topic is created and data is sent through a producer to the topic.
6. Further on the streaming pipeline a consumer is created on spark and data is read in using the structured streaming API.
7. Using the dataframesAPI real-time aggreagtions and groupby's are performed on the streaming data.

