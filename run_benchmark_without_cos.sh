source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort.sh 0513201644 4M
sleep 150
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_grep.sh 0513201645 4M
sleep 150
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_wordcount.sh 0513201646 4M
sleep 150

swift delete result
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort.sh 05132016164 16M
sleep 150
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_grep.sh 05132016165 16M
sleep 150
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_wordcount.sh 05132016166 16M