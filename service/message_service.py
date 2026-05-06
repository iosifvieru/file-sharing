from client import sns_client

def publish_message_to_all_participants(emails: list[str], unique_key: str):
    for email in emails:
        message = dict()

        message["email"] = email
        message["unique_key"] = str(unique_key)

        sns_client.publish_message(message)