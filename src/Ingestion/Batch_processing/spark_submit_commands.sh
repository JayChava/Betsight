#########################
# Spark_submit commands #
#########################

# pulling and processing data from s3 on spark
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 \ 
			 --conf spark.executor.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
			 --conf spark.driver.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
			 --master spark://10.0.0.11:7077 s3_spark_processing.py
			 
# querying schema for table from postgresql
spark-submit --jars ./postgresql-42.2.16.jar \
	         --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 \
             --master spark://10.0.0.11:7077 table_schema.py
			 
# writing data to postgresql
spark-submit --jars ./postgresql-42.2.16.jar \  
			 --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7  \
			 --master spark://10.0.0.11:7077 spark_write_postgres.py