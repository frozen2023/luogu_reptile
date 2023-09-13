import json
import re
import urllib.parse

import bs4
import requests
import os

problemUrl = "https://www.luogu.com.cn/problem/"
solutionUrl = "https://www.luogu.com.cn/problem/solution/"
userAgent02 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103"
userAgent01 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0" \
                  "Safari/537.36 Edg/116.0.1938.76"
headers = {
    "user-agent": userAgent02,
    "cookie": "__client_id=d670d45cce0e21ad3e7f30f352487ddb8028277b; _uid=1086745"
}
savePath = "D:\\luogu\\problems\\"

defaultDifficulty = ""

exclude = ["\\", '/', ':', '*', '?', '"', '>', '<', '|']


# 通过pid获取题目和题解
def getProblem(pid, title, d, tags, k):

    # 拼接目录名
    fatherDir = d
    for i in tags:
        fatherDir += '-'
        fatherDir += i
    if k != '':
        fatherDir += "-"
        fatherDir += k

    # 获取题目内容
    result = getProblemDetail(pid, title, fatherDir)
    if result == "error":
        return "error"

    # 获取题解内容
    getSolutionDetail(pid, title, fatherDir)
    print("{}爬取完毕！".format(pid))


def getProblemDetail(pid, title, fatherDir):
    print("正在爬取{}的题目...".format(pid), end="")
    problemHtml = getHTML(problemUrl + str(pid))
    if problemHtml == "error":
        print("爬取失败，可能是不存在该题或无权查看")
        return "error"
    else:
        problemMD = getMD(problemHtml, "problem")
        print("爬取成功！正在保存...", end="")
        dirName = pid + '-' + title
        fileName = dirName + ".md"
        saveData(problemMD, dirName, fileName, fatherDir)
        print("保存成功!")


def getSolutionDetail(pid, title, fatherDir):
    print("正在爬取{}的题解...".format(pid), end="")
    solutionHtml = getHTML(solutionUrl + str(pid))
    if solutionHtml == "error":
        print("爬取失败")
    else:
        solutionMD = getMD(solutionHtml, "solution")
        print("爬取成功！正在保存...", end="")
        dirName = pid + '-' + title
        fileName = dirName + "-题解.md"
        saveData(solutionMD, dirName, fileName, fatherDir)
        print("保存成功!")


def getHTML(url):
    res = requests.get(url, headers=headers)
    html = res.text
    if str(html).find("Exception") == -1:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"


# 解析html获取markdown文本
def getMD(html, type):
    bs = bs4.BeautifulSoup(html, "html.parser")
    if type == "problem":
        core = bs.select("article")[0]
        md = str(core)
        md = re.sub("<h1>", "# ", md)
        md = re.sub("<h2>", "## ", md)
        md = re.sub("<h3>", "#### ", md)
        md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        return md
    if type == "solution":
        core = bs.select("script")[0]
        script = str(core)
        index1 = script.index('"')
        index2 = script.index('"', index1 + 1)
        script = script[index1 + 1: index2]
        decodedStr = urllib.parse.unquote(script)
        map1 = json.loads(decodedStr)
        solutions = map1["currentData"]["solutions"]["result"]
        if len(solutions) > 0:
            bestSolution = solutions[0]
            md = bestSolution["content"]
            return md
        return "Sorry, there is no solution"


def saveData(data, dirName, fileName, fatherDir):
    # 规范目录或文件名
    dirName = cleanFileOrDirName(dirName)
    fileName = cleanFileOrDirName(fileName)
    fatherDir = cleanFileOrDirName(fatherDir)

    dirPath = savePath + fatherDir + "\\" + dirName
    filePath = dirPath + "\\" + fileName

    # 判断是否存在文件夹
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # 创建文件并写入
    file = open(filePath, "w", encoding="utf-8")
    for d in data:
        file.writelines(d)
    file.close()


def cleanFileOrDirName(name):
    result = str(name)
    for i in exclude:
        result = result.replace(i, "")
    return result


if __name__ == "__main__":
    getProblem("P1001", "数独", "入门", ["字符串"], "hello")
