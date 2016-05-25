source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
prefix=`date +%m%d%Y%M%H`
id='grep'
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_grep_cos.sh ${prefix}${id} 4M