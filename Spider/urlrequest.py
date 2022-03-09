from urllib.request import urlopen

resp = urlopen("http://www.baidu.com")
with open("./output.html", "w", encoding="utf-8") as f:
    f.write(resp.read().decode("utf8"))
print("over")
