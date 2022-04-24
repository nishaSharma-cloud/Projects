import findspark
import pyspark.sql.functions as f
from pyspark.ml.feature import RFormula
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression

findspark.init()

conf = SparkConf().setAppName("ApplicationTwo")
sc = SparkContext(conf=conf)

spark = SparkSession.builder.appName("how to read csv file").getOrCreate()
df = spark.read.csv('zoo.csv', inferSchema=True, header=True)
df.show()

df_new = df.withColumn("IsMammal", f.when(f.col("Type") == 1, f.lit(1)).otherwise(f.lit(0)))
df_new.show()
print(df_new.columns)


rmodel = RFormula(formula="IsMammal ~ .", featuresCol="features", labelCol="label")

rdf = rmodel.fit(df_new)
print(rdf.getLabelCol())
transform_data = rdf.transform(df_new)
transform_data.show()

train_data, test_data = transform_data.randomSplit([0.7, 0.3])

lr = LogisticRegression(labelCol="label", featuresCol="features")
fittedDataLR = lr.fit(train_data)
transformedDataLR = fittedDataLR.transform(test_data)
transformedDataLR.show()

test_df = spark.read.csv('test_data.csv', inferSchema=True, header=True)
test_df.show()

test_df_new = test_df.withColumn("IsMammal", f.when(f.col("Type") == 1, f.lit(1)).otherwise(f.lit(0)))
df_new.show()
print(df_new.columns)


rmodel_test = RFormula(formula="IsMammal ~ .", featuresCol="features", labelCol="label")

rdf2 = rmodel_test.fit(test_df_new)
print(rdf.getLabelCol())
transform_data2 = rdf2.transform(test_df_new)
transform_data2.show()
fittedDataLR2 = lr.fit(transform_data2)
test_result = fittedDataLR2.transform(transform_data2)
test_result.show()
test_result.select("AnimalName","label","Prediction").show()