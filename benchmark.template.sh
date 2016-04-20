#!/bin/bash

#output_file_format=benchmarkname_node_appid_st_et
#$1=> experiment_id or job_id

#hadoop_param
job_id=$1
hadoop_file_size="4M"
hadoop_benchmark="wordcount"
hadoop_executable="/home/cloudsys/hadoop/bin/hadoop"
hadoop_log_dir="/home/cloudsys/hadoop_log"
hadoop_log_name="${hadoop_benchmark}_${hadoop_file_size}_${job_id}"
hadoop_app_id=""
hadoop_example_jar="/home/cloudsys/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar"
hadoop_input_dir="swift://${hadoop_benchmark}${hadoop_file_size}.SparkTest/"
hadoop_output_dir="swift://result.SparkTest/${hadoop_benchmark}${hadoop_file_size}${job_id}"
hadoop_yarn_file_name="/home/cloudsys/hadoop/logs/yarn-cloudsys-resourcemanager-proxy.log"
output_dir="/home/cloudsys/result"

#iostat_param
iostat_duration=24
iostat_interval=5
iostat_log_dir="/home/cloudsys/iostat_log"





echo "----[running benchmark]----"
echo "benchmark: $hadoop_benchmark"
echo "input_dir: $hadoop_input_dir"
echo "output_dir: $hadoop_output_dir"
echo "log: $hadoop_log_name"
#echo "${hadoop_executable} jar ${hadoop_example_jar} ${hadoop_benchmark} ${hadoop_input_dir} ${hadoop_output_dir} > ${hadoop_log_dir}/${hadoop_log_name}" 2>&1 &
torun="${hadoop_executable} jar ${hadoop_example_jar} ${hadoop_benchmark} ${hadoop_input_dir} ${hadoop_output_dir}"
out="${hadoop_log_dir}/${hadoop_log_name}"
#/home/cloudsys/hadoop/bin/hadoop jar $hadoop_example_jar $hadoop_benchmark $hadoop_input_dir $hadoop_output_dir > $hadoop_log_dir/$hadoop_log_name 2>&1 &
#echo "${torun} >${out} 2>&1 &"
${torun} >${out} 2>&1 &
sleep 5

#iostat

echo "----[running iostat]----"
for j in {1..8}; do
	iostat_log_name="${hadoop_benchmark}_object${j}_${hadoop_file_size}_${job_id}"
	echo "[iostat log]: ${iostat_log_name}"
	ssh object$j 'iostat -c -d -x -t -m /dev/sda 5 24'  > /home/cloudsys/iostat_log/${iostat_log_name} &
done

echo "----[sleeping for 120 sec]----"
sleep 120


#consolidate_hadoop_logs
#get app_id from the file
app_id=`cat ${hadoop_log_dir}/${hadoop_log_name} | grep "Submitting tokens for job" | cut -f 5 -d":"  | cut -f 2 -d "_"`
echo $app_id
python hadoop_perser.py ${hadoop_yarn_file_name} ${hadoop_log_dir}/${hadoop_log_name}  ${app_id}

mv ${hadoop_log_dir}/${hadoop_log_name}  ${output_dir}
#consolidate_iostaat_logs
echo "----[python iostat]----"

for j in {1..8}; do
	iostat_log_name="${hadoop_benchmark}_object${j}_${hadoop_file_size}_${job_id}"
	echo "[python iostat]: parsing ${iostat_log_name}"
	python iostat_perser.py /home/cloudsys/iostat_log/${iostat_log_name} ${output_dir}/${iostat_log_name}.csv
done
