#!/bin/bash
source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
prefix=`date +%m%d%Y%M%H`
id='sort_only'
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort.sh ${prefix}${id} 4M
#sleep 400
#id='grep_only'
#ssh palden@hyper 'source clear_cache/clean.sh'
#source benchmark_grep.sh ${prefix}${id} 4M