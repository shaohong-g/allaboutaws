import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket (use from_source to insert source manually)
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="glue_experiment",
    push_down_predicate="dataload=20230221",
    table_name="csv",
    transformation_ctx="S3bucket_node1",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("merchant", "string", "merchant", "string"),
        ("mcc", "long", "mcc", "long"),
        ("currency", "string", "currency", "string"),
        ("amount", "double", "amount", "double"),
        ("transaction_date", "timestamp", "transaction_date", "timestamp"),
        ("card_type", "string", "card_type", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# preprocessing
def add_constant_value_column(dyf):
    dyf["new_amount"] = dyf["amount"] * 2
    return dyf

Processed_node3 = ApplyMapping_node2.map(f=add_constant_value_column)

# useless - to increase processing time
sparkDF = Processed_node3.toDF()
sparkDF.show(5)

# Drop
Processed_node3 = Processed_node3.drop_fields(["amount"])
# Processed_node3.show(10)
ApplyMapping_node_final = ApplyMapping.apply(
    frame=Processed_node3,
    mappings=[
        ("merchant", "string", "merchant", "string"),
        ("mcc", "long", "mcc", "long"),
        ("currency", "string", "currency", "string"),
        ("new_amount", "double", "amount", "double"),
        ("transaction_date", "timestamp", "transaction_date", "timestamp"),
        ("card_type", "string", "card_type", "string"),
    ],
    transformation_ctx="ApplyMapping_node_final",
)


# Script generated for node PostgreSQL table
PostgreSQLtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=ApplyMapping_node_final,
    database="postgres",
    table_name="glue_public_records",
    transformation_ctx="PostgreSQLtable_node3",
)

job.commit()
