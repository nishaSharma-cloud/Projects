import findspark
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB

pulpColor = ['red', 'red', 'red', 'yellow', 'yellow', 'green', 'green', 'green']
taste = ['sour', 'sour', 'bitter', 'sweet', 'bitter', 'sour', 'sweet', 'bitter']
edible = ['yes', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no']

df_new = df.withColumn("IsEdible", f.when(f.col("Type") == 1, f.lit(1)).otherwise(f.lit(0)))
df_new.show()
print(df_new.columns)

preprocess = preprocessing.LabelEncoder()

color = preprocess.fit_transform(pulpColor)
taste_pre = preprocess.fit_transform(taste)

print( color, taste_pre)

features = zip(color, taste_pre)
print(features.__next__())

label = preprocess.fit_transform(edible)

print (label)

model = GaussianNB()

model.fit(features, label)

test = model.predict([[2,1]]) #2: yellow, 1: sour
print (test)




















#
#

#
#
# rmodel = RFormula(formula="IsMammal ~ .", featuresCol="features", labelCol="label")
#
# rdf = rmodel.fit(df_new)
# # print(rdf.getLabelCol())
# transform_data = rdf.transform(df_new)
# transform_data.show()
#
# train_data, test_data = transform_data.randomSplit([0.7, 0.3])
#
# lr = LogisticRegression(labelCol="label", featuresCol="features")
# fittedDataLR = lr.fit(train_data)
# transformedDataLR = fittedDataLR.transform(test_data)
# # transformedDataLR.show()
#
# test_df = spark.read.csv('test_data.csv', inferSchema=True, header=True)
# # test_df.show()
#
# test_df_new = test_df.withColumn("IsMammal", f.when(f.col("Type") == 1, f.lit(1)).otherwise(f.lit(0)))
# # df_new.show()
# # print(df_new.columns)
#
#
# rmodel_test = RFormula(formula="IsMammal ~ .", featuresCol="features", labelCol="label")
#
# rdf2 = rmodel_test.fit(test_df_new)
# # print(rdf.getLabelCol())
# transform_data2 = rdf2.transform(test_df_new)
# # transform_data2.show()
# fittedDataLR2 = lr.fit(transform_data2)
# test_result = fittedDataLR2.transform(transform_data2)
# # test_result.show()
# test_result.select("AnimalName","label","Prediction").show()
