import random
import requests

#url = "https://www.careersitecloud.com/api/v1/import/55e986c70cf2bf965dabbdec/autest"
url = "https://www.dev.careersitecloud.com/api/v1/import/job/59b68fa659018907688b5547"
headers = {
   'content-type': "application/xml",
    }

def lambda_handler(event, context):
    response = requests.delete(url, headers=headers, auth=('59b2bf0f6bc6bf600654dae3', 'ada408e0-2fe7-4c4c-b34c-76b1702abb03'), verify=False)
    try:
        output = response.json()
    except ValueError:
        output = response.text
    return output

print lambda_handler(None, None)
