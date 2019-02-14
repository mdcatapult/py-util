# -*- coding: utf-8 -*-
import json
from klein_config import config
import boto3


def notify(msg, **kwargs):
    if config.has("notifications.topic") and config.has("aws"):
        msg_string = json.dumps(msg)
        client = boto3.client('sns', region_name=config.get("aws.region"))
        client.publish(
            TopicArn=config.get("notifications.topic"),
            Message=msg_string,
            Subject=kwargs["subject"] if "subject" in kwargs else "Consumer Notification",
        )
