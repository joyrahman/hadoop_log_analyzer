source ~/admin-openrc.sh
swift delete result
cd hadoop_log_analyzer
source benchmark_sort_cos.sh 0505201541 4M
source benchmark_grep_cos.sh 0505201542 4M
source benchmark_wordcount_cos.sh 0505201543 4M
swift delete result
source benchmark_sort_cos.sh 05052015161 16M
source benchmark_grep_cos.sh 05052015162 16M
source benchmark_wordcount_cos.sh 05052015163 16M


source ~/admin-openrc.sh
swift delete result
cd hadoop_log_analyzer
source benchmark_sort.sh 0505201544 4M
source benchmark_grep.sh 0505201545 4M
source benchmark_wordcount.sh 0505201546 4M
swift delete result
source benchmark_sort.sh 05052015164 16M
source benchmark_grep.sh 05052015165 16M
source benchmark_wordcount.sh 05052015166 16M

