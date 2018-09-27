# EE412-HW1
EE412-HW1 programming assignment

Using MapReduce and Spark

1)Mapper
  Input: user, list of friends
  Output: user, (user, common friend)
2) Reducer
  Input: user, (user, common friend)
  Output: user, user, number of common friends

How to Run

input this command in the directory where spark is installed

bin/spark-submit /mnt/home/20130242/EE412-HW1/finder.py /mnt/home/20130242/EE412-HW1/soc-LiveJournal1Adj.txt /mnt/home/20130242/EE412-HW1/hw1.txt
