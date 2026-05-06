#!/bin/bash

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=eu-central-1
export AWS_ENDPOINT_URL=http://localhost:4566

aws --endpoint-url=http://localhost:4566 sns create-topic --name email-topic

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name email-queue

TOPIC_ARN=$(aws --endpoint-url=http://localhost:4566 sns list-topics \
  --query "Topics[0].TopicArn" --output text)

QUEUE_URL=$(aws --endpoint-url=http://localhost:4566 sqs get-queue-url \
  --queue-name email-queue --query "QueueUrl" --output text)

QUEUE_ARN=$(aws --endpoint-url=http://localhost:4566 sqs get-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attribute-names QueueArn \
  --query "Attributes.QueueArn" --output text)

aws --endpoint-url=http://localhost:4566 sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol sqs \
  --notification-endpoint "$QUEUE_ARN"
