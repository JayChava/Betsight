## src structure


```
src
├── Data_simulator
│   ├── create-emr-cluster.sh
│   ├── bootstrap.sh
│   ├── data_simulation.py
│   └── README.md
│    
├── Grafana                                                  
│   ├── betting_companies_dashboard_config.json
│   ├── Graph_queries.txt                                      
│   └── setup.txt  
│                                                                
├── Ingestion                                                    
│   ├── Batch_processing                                       
│   │   ├── batch_db.sql
│   │   ├── README.md                                            
│   │   ├── s3_spark_processing.py                                        
│   │   ├── spark_postgres.py
│   │   ├── spark_submit_commands.sh
│   │   └── table_schema.py
│   │
│   └── Stream_processing
│       ├── Kafka_commands.sh
│       ├── README.md
│       ├── s3_kafka_producer.py
│       ├── spark_consumer.py
│       ├── spark-streaming-submit_commands.sh 
│       └── stream_db.sql
│
└── pre-processing
    ├── directory_breakdown.py  
    └── README.md
