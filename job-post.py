import random
import requests

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()
titles = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-title").content.splitlines()
countries = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-country").content.splitlines()
states = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-state").content.splitlines()
cities = requests.get("https://raw.githubusercontent.com/a1u/job-generator/master/data-city").content.splitlines()

#url = "https://www.careersitecloud.com/api/v1/import/55e986c70cf2bf965dabbdec/autest"
url = "https://www.dev.careersitecloud.com/api/v1/import/55e986c70cf2bf965dabbdec/autest"
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

def lambda_handler(event, context):
    job = { "address" : rws(3, words),
            "applyEmail" : "no-reply@aspentechlabs.com",
            "applyRedirect" : "https://www.aspentechlabs.com",
            "category" : rws(2, words),
            "city" : rws(1, cities),
            "country" : rws(1, countries),
            "description" : rws(200, words),
            "education" : rws(10, words),
            "experience" : rws(10, words),
            "ref" : rws(1, words),
            "salary" : rws(2, words),
            "source" : rws(1, words),
            "state" : rws(2, states),
            "title" : rws(1, titles),
            "jobtype" : rws(1, words),
            "postalcode" : rws(1, words)
 }
    payload = { "source": { "job": job } }
    payload = json2xml(payload)
    response = requests.post(url, headers=headers, auth=('59b2bf0f6bc6bf600654dae3', 'ada408e0-2fe7-4c4c-b34c-76b1702abb03'), data=payload, verify=False)
    try:
        output = response.json()
    except ValueError:
        output = response.text
    return output

print lambda_handler(None, None)
