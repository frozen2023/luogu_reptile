import requests
import json

difficulty = {"无": 0, "入门": 1, "普及-": 2, "普及/提高-": 3, "普及+/提高": 4, "提高+/省选-": 5, "省选/NOI-": 6, "NOI/NOI+/CTSC": 7}
tag = {}
reqUrl = "https://www.luogu.com.cn/problem/list"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 " \
            "Safari/537.36 Edg/116.0.1938.76 "
cookie = "__client_id=d670d45cce0e21ad3e7f30f352487ddb8028277b; _uid=1086745"
headers = {
    "user-agent": userAgent,
    "cookie": cookie
}
tagUrl = "https://www.luogu.com.cn/_lfe/tags?_version=1694484943"
_contentOnly = 1


def getPids(difficultyStr, tagStr, keyword):
    if difficultyStr == '':
        difficultyInt = 0
    else:
        difficultyInt = difficulty[difficultyStr]
    if initTag() == "error":
        return "error"
    if tagStr == '':
        tagInt = None
    else:
        tagInt = tag[tagStr]
    params = {"difficulty": difficultyInt, "tag": tagInt, "keyword": keyword, "_contentOnly": _contentOnly}
    resp = requests.get(reqUrl, headers=headers, params=params)
    jsonTxt = resp.text
    map1 = json.loads(jsonTxt)
    map2 = map1["currentData"]["problems"]
    totalCount = map2["count"]
    problems = map2["result"]
    return totalCount, problems


def initTag():
    if len(tag) != 0:
        return
    res = requests.get(tagUrl, headers=headers)
    if str(res.text).find("Exception") != -1:
        print("爬取Tag列表失败...")
        return "error"
    jsonTxt = eval("u" + "\'" + res.text + "\'")
    map = json.loads(jsonTxt)
    tagList = map["tags"]
    for item in tagList:
        tagName = item['name']
        tagId = item['id']
        tag[tagName] = tagId


if __name__ == "__main__":
    totalCount, problems = getPids("入门", "字符串", "")
    print("共发现{}道题目".format(totalCount))
    print(problems)

