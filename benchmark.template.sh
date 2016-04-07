#!/bin/bash

#$1=> outputfile_suffix
#$2=> input container
benchmark_name=""
file_name=""
app_id=""

cd ~/hadoop



echo "running hadoop..."
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar sort swift://$2.SparkTest/ swift://result.SparkTest/$2_$1 &

sleep 5

#iostat
echo "running iostat..."
for j in {1..8}; do
	ssh object$j 'iostat -c -d -x -t -m /dev/sda 5 24' > /home/cloudsys/iostat_log/terasort_obj${j}_$2_$1 &
done


#consolidate_hadoop_logs
#consolidate_iostat_logs
