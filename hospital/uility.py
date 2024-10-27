import requests
import logging

logger = logging.getLogger(__name__)


def user_has_group(user, group_name):
    if user.groups.filter(name=group_name).exists():
        return True
    else:
        return False


def sent_sms(api_key, senderid, phone: str, message: str):
    """
    send sms to phone number by bulksmsbd.net
    api_key & senderid given by doctor
    """
    logger.info(f"send_sms called, params phone: {phone} message: {message}")
    url = "http://bulksmsbd.net/api/smsapi"
    params = {
        'api_key': api_key,
        'senderid': senderid,
        'type': 'text',
        'number': phone,
        'message': message
    }
    request_response = requests.get(url=url, params=params)
    response_json = request_response.json()
    logger.info(f"{'*' * 10} send sms response {response_json}")
    return response_json
