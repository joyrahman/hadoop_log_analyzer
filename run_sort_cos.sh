#!/bin/bash
source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
prefix=`date +%m%d%Y%M%H`
id='sort_cos'
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort_cos.sh ${prefix}${id} 16M
