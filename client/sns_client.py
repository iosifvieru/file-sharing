from os import getenv
import boto3
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

SNS_TOPIC_ARN = getenv("SNS_TOPIC_ARN", "arn:aws:sns:eu-central-1:000000000000:email-topic")

sns = boto3.client("sns")

def publish_message(message: dict):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=str(message),
    )

    logger.info(f"Published message: {message}")
