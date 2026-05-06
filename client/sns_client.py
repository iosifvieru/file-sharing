from os import getenv
import boto3
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

SNS_AWS_REGION = getenv("SNS_AWS_REGION", "eu-central-1")
SNS_TOPIC_ARN = getenv("SNS_TOPIC_ARN", "arn:aws:sns:eu-central-1:000000000000:email-topic")

sns = boto3.client("sns",
    region_name=SNS_AWS_REGION
)

def publish_message(message: dict):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=str(message),
        MessageGroupId="file-sharing"
    )

    logger.info(f"Published message: {message}")
