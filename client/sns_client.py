from os import getenv
import boto3
from loguru import logger

SNS_ACCESS_KEY = getenv("SNS_ACCESS_KEY", "test")
SNS_SECRET_KEY = getenv("SNS_SECRET_KEY", "test")

SNS_AWS_REGION = getenv("SNS_AWS_REGION", "eu-central-1")
SNS_AWS_ENDPOINT_URL = getenv("SNS_AWS_ENDPOINT_URL", "http://localhost:4566")
SNS_TOPIC_ARN = getenv("SNS_TOPIC_ARN", "arn:aws:sns:eu-central-1:000000000000:email-topic")

sns = boto3.client(
    "sns",
    region_name=SNS_AWS_REGION,
    endpoint_url=SNS_AWS_ENDPOINT_URL,
    aws_access_key_id=SNS_ACCESS_KEY,
    aws_secret_access_key=SNS_SECRET_KEY,
)

def publish_message(message: dict):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=str(message),
    )

    logger.info(f"Published message: {message}")
