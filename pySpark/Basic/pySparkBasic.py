import findspark
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
findspark.init()

# import os
# os.environ["JAVA_HOME"] = "C:/Progra~1/Java/jdk-15.0.2"

from pyspark import SparkConf, SparkContext
conf=SparkConf().setAppName("ApplicationOne")
sc=SparkContext(conf=conf)

from pyspark.sql import SparkSession

spark = SparkSession.builder .appName("how to read csv file").getOrCreate()


df = spark.read.csv('2015-summary.csv',inferSchema=True, header =True)
df.show()


# Printing df based on destination country
print(df.select('DEST_COUNTRY_NAME').rdd.flatMap(lambda line: line.split(" ")))

# Selecting df based on max count
print(df.select('count').rdd.max())

#Filtering based on threshold 
print(df.filter(df['count'] > 10).count())

#Filtering country based on US and finding the sum
import pyspark.sql.functions as f
records = df.filter(df['DEST_COUNTRY_NAME'] == 'United States')
sum = records.select(f.sum('count'))
print(sum.show())


## Customer table
data1 = [(1, "James", "Koblenzer str 236", "yahoo", 3000),
         (2, "Rose", "Moselwieser str 132", "google", 4000),
         (3, "Robert", "Casino Str 542", "amazon", 2000),
         (4, "Maria", "Gymnasiumstr 42", "aldi", 4000),
         (5, "Jen", "Elisebeth str", "rewe", 5000)]

schema = StructType([StructField("CustomerId", IntegerType(), True), StructField("Name", StringType(), True),
                     StructField("Address", StringType(), True), StructField("website", StringType(), True),
                     StructField("CreditLimit", IntegerType(), True)])

Customers = spark.createDataFrame(data=data1, schema=schema)
Customers.printSchema()
Customers.show(truncate=False)
Customers.createOrReplaceTempView("customers")

## Employee table

data2 = [(1, "James", "Smith", "jamesSmith@yahoo.com", 15732, "12.05.2021", 4, "Salesman"),
         (2, "Rose", "Antony", "roseAntony@gamil.com", 43785, "25.04.2019", 3, "Senior Salesman"),
         (3, "Marry", "watson", "maryWatson@gamil.com", 78346, "12.07.2008", 5, "Manager"),
         (4, "Maria", "jones", "mariaJones@gamil.com", 943576, "15.08.2009", 5, "Manager"),
         (5, "Jen", "Elisebeth", "jenElisebeth@gmail.com", 85432, "23.06.2000", None, "President")]

schema2 = StructType([StructField("EmployeeId", IntegerType(), True), StructField("FirstName", StringType(), True),
                      StructField("LastName", StringType(), True), StructField("email", StringType(), True),
                      StructField("Phone", IntegerType(), True), StructField("HireDate", StringType(), True),
                      StructField("ManagerId", IntegerType(), True), StructField("JobTitle", StringType(), True)])

Employees = spark.createDataFrame(data=data2, schema=schema2)
Employees.printSchema()
Employees.show(truncate=False)
Employees.createOrReplaceTempView("employees")


### Orders table

data3 = [(1, 5, "Ordered", 1, "23.02.2021"),
         (2, 2, "Pending", 2, "19.08.2021"),
         (3, 3, "Cancelled", None, "03.04.2021"),
         (4, 3, "Pending", 2, "07.02.2021"),
         (5, 4, "Delivered", None, "16.05.2021")]

schema3 = StructType([StructField("OrderId", IntegerType(), True), StructField("CustomerId", IntegerType(), True),
                      StructField("Status", StringType(), True), StructField("SalesmanId", IntegerType(), True),
                      StructField("OrderDate", StringType(), True)])

Orders = spark.createDataFrame(data=data3, schema=schema3)
Orders.printSchema()
Orders.show(truncate=False)
Orders.createOrReplaceTempView("Orders")


 ## Order_item table

data4 = [(1, 5, 3, 1, 50),
         (2, 2, 2, 2, 10),
         (3, 3, 4, 1, 30),
         (4, 3, 1, 2, 22),
         (5, 4, 5, 3, 34)]

schema4 = StructType([StructField("OrderId", IntegerType(), True), StructField("ItemId", IntegerType(), True),
                      StructField("ProductId", IntegerType(), True), StructField("Quantity", IntegerType(), True),
                      StructField("Unit_Price", IntegerType(), True)])

order_items = spark.createDataFrame(data=data4, schema=schema4)
OrderItem.printSchema()
OrderItem.show(truncate=False)
order_items.createOrReplaceTempView("order_items")

spark.sql("""SELECT year(order_date) as year, sum(quantity * unit_price) as revenue
FROM orders NATURAL JOIN order_items GROUP BY year(order_date) ORDER BY year""").show()

Orders.join(Employees, f.expr("EmployeeId = SalesmanId"), "left_semi").show()

Employees.join(Orders, f.expr("employee_id = salesman_id"),"full").groupBy("employee_id").agg(f.expr("count(*) as sales")).orderBy("sales",ascending=False)



spark.sql(sqlText="""SELECT e.employee_id, count(*) as sales FROM Employees e
FULL JOIN Orders o ON e.employee_id = o.salesman_id GROUP BY e.employee_id ORDER BY sales DESC""").show()


Orders.rdd.filter(lambda y: y["Status"] == "pending").map(lambda y: (y["CustomerId"], 1)).reduceByKey(lambda x,y: x + y).sortBy(lambda x:x[1], ascending= False)

result = Customers.withColumnRenamed("CustomerId","customer")\
    .join(Orders,f.expr(("customer = CustomerId")),"inner")\
    .selectExpr("customer as CustomerId","Name","year(to_date(\"OrderDate\",'dd.mm.yyyy')) as year","OrderId")\
    .groupBy("CustomerId","Name").pivot("year")\
    .agg(f.expr("count(OrderId)"))\
    .orderBy("Name",ascending=True)\
    .fillna(value=0)
result.show()