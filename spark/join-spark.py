#!/usr/bin/env python

print("# join-spark.py", flush=True)

import os
import gc
import timeit
import pyspark
from pyspark.sql import SparkSession

exec(open("./helpers.py").read())

ver = pyspark.__version__
git = "" # won't fix: https://issues.apache.org/jira/browse/SPARK-16864
task = "join"
solution = "spark"
fun = ".sql"
cache = "TRUE"

data_name = os.environ['SRC_JN_LOCAL']
src_jn_x = os.path.join("data", data_name+".csv")
y_data_name = join_to_tbls(data_name)
src_jn_y = [os.path.join("data", y_data_name[0]+".csv"), os.path.join("data", y_data_name[1]+".csv"), os.path.join("data", y_data_name[2]+".csv")]
if len(src_jn_y) != 3:
    raise Exception("Something went wrong in preparing files used for join")

print("loading datasets " + data_name + ", " + y_data_name[0] + ", " + y_data_name[2] + ", " + y_data_name[2], flush=True)

from pyspark.conf import SparkConf
spark = SparkSession.builder \
     .master("local[*]") \
     .appName("groupby-spark") \
     .config("spark.executor.memory", "100g") \
     .config("spark.driver.memory", "100g") \
     .config("spark.python.worker.memory", "100g") \
     .config("spark.driver.maxResultSize", "100g") \
     .config("spark.network.timeout", "2400") \
     .config("spark.executor.heartbeatInterval", "1200") \
     .config("spark.ui.showConsoleProgress", "false") \
     .getOrCreate()
#print(spark.sparkContext._conf.getAll(), flush=True)

x = spark.read.csv(src_jn_x, header=True, inferSchema='true').persist(pyspark.StorageLevel.MEMORY_ONLY)
big = spark.read.csv(src_jn_y[0], header=True, inferSchema='true').persist(pyspark.StorageLevel.MEMORY_ONLY)
medium = spark.read.csv(src_jn_y[1], header=True, inferSchema='true').persist(pyspark.StorageLevel.MEMORY_ONLY)
small = spark.read.csv(src_jn_y[2], header=True, inferSchema='true').persist(pyspark.StorageLevel.MEMORY_ONLY)

print(x.count(), flush=True)
print(big.count(), flush=True)
print(medium.count(), flush=True)
print(small.count(), flush=True)

x.createOrReplaceTempView("x")
big.createOrReplaceTempView("big")
medium.createOrReplaceTempView("medium")
small.createOrReplaceTempView("small")

print("joining...", flush=True)

question = "small inner on int" # q1
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join small on x.id4 = small.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #[spark.sql("select sum(v1) as v1 from ans").collect()[0].asDict()['v1']]
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=1, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join small on x.id4 = small.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #[spark.sql("select sum(v1) as v1 from ans").collect()[0].asDict()['v1']]
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=2, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
print(ans.head(3), flush=True)
# print(ans.tail(3), flush=True) # as of 2.4.0 still not implemented https://issues.apache.org/jira/browse/SPARK-26433
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans

question = "medium inner on int" # q2
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join medium on x.id4 = medium.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #[spark.sql("select sum(v1) as v1 from ans").collect()[0].asDict()['v1']]
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=1, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join medium on x.id4 = medium.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #[spark.sql("select sum(v1) as v1 from ans").collect()[0].asDict()['v1']]
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=2, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
print(ans.head(3), flush=True)
# print(ans.tail(3), flush=True)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans

question = "medium outer on int" # q3
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x left join medium on x.id4 = medium.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=1, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x left join medium on x.id4 = medium.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=2, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
print(ans.head(3), flush=True)
# print(ans.tail(3), flush=True)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans

question = "medium inner on factor" # q4
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join medium on x.id1 = medium.id1').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v2) as v2, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=1, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join medium on x.id1 = medium.id1').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v2) as v2, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=2, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
print(ans.head(3), flush=True)
# print(ans.tail(3), flush=True)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans

question = "big inner on int" # q5
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join big on x.id4 = big.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v2) as v2, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=1, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans
gc.collect()
t_start = timeit.default_timer()
ans = spark.sql('select * from x join big on x.id4 = big.id4').persist(pyspark.StorageLevel.MEMORY_ONLY)
print((ans.count(), len(ans.columns)), flush=True) # shape
t = timeit.default_timer() - t_start
m = memory_usage()
ans.createOrReplaceTempView("ans")
t_start = timeit.default_timer()
chk = [0] #list(spark.sql("select sum(v1) as v1, sum(v2) as v2, sum(v3) as v3 from ans").collect()[0].asDict().values())
chkt = timeit.default_timer() - t_start
write_log(task=task, data=data_name, in_rows=x.count(), question=question, out_rows=ans.count(), out_cols=len(ans.columns), solution=solution, version=ver, git=git, fun=fun, run=2, time_sec=t, mem_gb=m, cache=cache, chk=make_chk(chk), chk_time_sec=chkt)
print(ans.head(3), flush=True)
# print(ans.tail(3), flush=True)
ans.unpersist()
spark.catalog.uncacheTable("ans")
del ans

spark.stop()

exit(0)
