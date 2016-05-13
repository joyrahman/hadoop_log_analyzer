source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort_cos.sh 0513201641 4M
sleep 300
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_grep_cos.sh 0513201642 4M
sleep 300
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_wordcount_cos.sh 0513201643 4M
sleep 300
swift delete result
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_sort_cos.sh 05132016161 16M
sleep 300
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_grep_cos.sh 05132016162 16M
sleep 300
ssh palden@hyper 'source clear_cache/clean.sh'
source benchmark_wordcount_cos.sh 05132016163 16M
sleep 300






