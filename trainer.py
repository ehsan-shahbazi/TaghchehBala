from pyspark import SparkConf, SparkContext
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder
import findspark
import os


spark_location = '/usr/lib/spark'  # Set your own
java8_location = '/usr/lib/jvm/java-8-openjdk-amd64'  # Set your own
os.environ['JAVA_HOME'] = java8_location
findspark.init(spark_home=spark_location)
sc = SparkContext("local", "Spark Demo")
words = sc.parallelize(["scala", "java", "hadoop", "spark", "akka", "spark vs hadoop", "pyspark", "pyspark and spark"])
counts = words.count()
print("Number of elements in RDD -> %i" % counts)
