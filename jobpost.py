import random
import requests
from lxml import html

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()
titles = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-title").content.splitlines()
countries = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-country").content.splitlines()
states = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-state").content.splitlines()
cities = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-city").content.splitlines()

#url = "https://www.careersitecloud.com/api/v1/import/55e986c70cf2bf965dabbdec/autest"
urlpost = "https://www.careersitecloud.com/api/v1/import/55e986c70cf2bf965dabbdec/autest"
urldelete = "https://www.careersitecloud.com/api/v1/import/job/{id}"
urllist = "https://www.careersitecloud.com/api/v1/import/job"

headers = {
   'content-type': "application/xml",
    }

def rws(l = 1, lst = []):
    s = list()
    for x in range(0, l):
        s.append(lst[random.randint(0, len(lst) - 1)])
    return " ".join(s)

def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    if json_obj_type is str:
        return "%s<![CDATA[%s]]>" % (line_padding, json_obj)

    return "%s%s" % (line_padding, json_obj)

def delete(id):
    response = requests.delete(urldelete.replace("{id}", id), headers=headers, auth=('59b2bf0f6bc6bf600654dae3', 'ada408e0-2fe7-4c4c-b34c-76b1702abb03'), verify=False)
    try:
        return response.text
    except ValueError:
        return "Failed"

def lst():
    response = requests.get(urllist, headers=headers, auth=('59b2bf0f6bc6bf600654dae3', 'ada408e0-2fe7-4c4c-b34c-76b1702abb03'), verify=False)
    try:
        output = response.text
        tree = html.fromstring(output)
        return tree.xpath('//item/@id')
    except ValueError:
        return []

def post():
    job = {"address": rws(3, words),
           "applyEmail": "no-reply@aspentechlabs.com",
           "applyRedirect": "https://www.aspentechlabs.com",
           "category": rws(2, words),
           "city": rws(1, cities),
           "country": rws(1, countries),
           "description": rws(200, words),
           "education": rws(10, words),
           "experience": rws(10, words),
           "ref": rws(1, words),
           "salary": rws(2, words),
           "source": rws(1, words),
           "state": rws(2, states),
           "title": rws(1, titles),
           "jobtype": rws(1, words),
           "postalcode": rws(1, words)
           }
    payload = {"source": {"job": job}}
    payload = json2xml(payload)
    response = requests.post(urlpost, headers=headers,
                             auth=('59b2bf0f6bc6bf600654dae3', 'ada408e0-2fe7-4c4c-b34c-76b1702abb03'), data=payload,
                             verify=False)
    try:
        return response.text
    except ValueError:
        return "Error"

def lambda_handler(event, context):
    all = lst()
    target = random.randint(20, 40)
    if (len(all) > target):
        for i in range(0, len(all) - target):
            print delete(all[i])
    elif (len(all) < target):
        for i in range(0, target - len(all)):
            print post()

print lambda_handler(None, None)
