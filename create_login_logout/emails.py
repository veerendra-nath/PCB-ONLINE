import boto3
import secrets
from botocore.exceptions import ClientError

from database.models import *


def email_verify(user=None, type=None):
    verification = VerificationData()
    if type == 'verification':
        SENDER = "User Verification <noreplay@ioproto.com>"
        SUBJECT = " Email Verification"
        verification.data = secrets.token_urlsafe(128)
        verification.user = user
        verification.save()
        BODY_HTML = "Ddd"
        BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                     "This email was sent with Amazon SES using the "
                     "AWS SDK for Python (Boto)."
                     )
    elif type == 'forgot':
        SENDER = "Reset Password <noreplay@ioproto.com>"
        SUBJECT = "Reset Password"
        verification.data = secrets.token_urlsafe(128)
        verification.user = user
        verification.save()
        BODY_HTML = "Ddd"
        BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                     "This email was sent with Amazon SES using the "
                     "AWS SDK for Python (Boto)."
                     )
    elif type is None:
        return False
    RECIPIENT = user.email
    AWS_REGION = "us-west-2"
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION,
                          aws_access_key_id='AKIAJ5XBMFWN3FRWOJLA',
                          aws_secret_access_key='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')

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER

        )

    except ClientError as e:
        return False, e.response['Error']['Message']
    else:
        return True, response['MessageId']
    return True

