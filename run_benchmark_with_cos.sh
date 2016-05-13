source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
source benchmark_sort_cos.sh 0513201641 4M
sleep 300
source benchmark_grep_cos.sh 0513201642 4M
sleep 300
source benchmark_wordcount_cos.sh 0513201643 4M
sleep 300
swift delete result
source benchmark_sort_cos.sh 05132016161 16M
sleep 300
source benchmark_grep_cos.sh 05132016162 16M
sleep 300
source benchmark_wordcount_cos.sh 05132016163 16M
sleep 300



source ~/admin-openrc.sh
swift delete result
cd ~/hadoop_log_analyzer
source benchmark_sort.sh 0513201644 4M
sleep 300
source benchmark_grep.sh 0513201645 4M
sleep 300
source benchmark_wordcount.sh 0513201646 4M
sleep 300
swift delete result
source benchmark_sort.sh 05132016164 16M
sleep 300
source benchmark_grep.sh 05132016165 16M
sleep 300
source benchmark_wordcount.sh 05132016166 16M


