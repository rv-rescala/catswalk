import boto3

def create_queue(qname, region_name):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.create_queue(
        QueueName=qname,
        Attributes={
            "DelaySeconds": "0",
            "VisibilityTimeout": "60",  # 60 seconds
        }
    )
    print(response)