import requests
import re
name = input("请输入你要下载的小说名称：")
find_url = 'https://m.biquku.com/s/so.php?type=articlename&s=' + name
response = requests.get(url=find_url).content.decode('gb18030')
one = re.findall(r'<div class="cover">([\d\D]*?</p>)[\s\n]*?</div>', response)
try:
    two = re.findall(r'<p class="line">([\d\D]*?</p>)', one[0])
    all_book = []
    all_book_a = []
    i = 1
    print("{}搜索结果如下".format(name))
    for one_book in two:
        all_book.append(re.findall(r'target="_blank">([\d\D]*?)</a>', one_book)[0])
        all_book_a.append(re.findall(r'</a>/(.*?)</p>', one_book))
        print(str(i), ":", all_book[i-1], " —— 作者：", all_book_a[i-1][0].strip("\n"))
        i += 1
except Exception as e:
    print("没有搜索到，可以试试换个名字")
else:
    try:
        i = int(input("请输入要下载的小说编号："))
        three = re.findall(r'<a href="([\d\D]*?)"', two[i-1])
        book_name = all_book[i-1]
    except Exception as e:
        print("请正确输入要下载的小说前的编号！")
    else:
        book_url = 'https://m.biquku.com' + three[-1]
        response = requests.get(url=book_url).content.decode('gb18030')
        one = re.findall(r'<ul class="chapter">([\d\D]*?)</ul>', response)
        two = re.findall(r'<li>([\d\D]*?)</li>', one[0])
        three = re.findall(r"<a href='(.*?)'", two[0])
        end_page = int(three[0].split("/")[-1].replace(".html", ""))
        all_page_url = book_url + 'index_1.html'
        response = requests.get(url=all_page_url).content.decode('gb18030')
        one = re.findall(r'<ul class="chapter">([\d\D]*?)</ul>', response)
        two = re.findall(r'<li>([\d\D]*?)</li>', one[0])
        three = re.findall(r"<a href='(.*?)'", two[0])
        start_page = int(three[0].split("/")[-1].replace(".html", ""))
        key = start_page-1
        while start_page <= end_page:
            try:
                if start_page - key > 10:
                    url = book_url + str(key) + ".html"
                    response = requests.get(url=url, timeout=3).content.decode('gb18030')
                    one = re.findall(r'<a id="pb_next" href="([\d\D]*?)">', response)
                    start_page = int(one[0].split("/")[-1].replace(".html", ""))
                url = book_url + str(start_page) + ".html"
                response = requests.get(url=url, timeout=3).content.decode('gb18030')
                text = re.findall(r'<div id="nr1">[\w\W]*?</div>', response)[0]
                lines = re.findall(r'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />', text)
                title = re.findall(r'<div class="nr_title" id="nr_title">([\w\W]*?)</div>', response)[0]
            except Exception as e:
                pass
            else:
                print('{}——已爬取'.format(title))
                key = start_page
                with open('{}.doc'.format(book_name), 'a', encoding='gb18030') as f:
                    f.write('\n\n\n')
                    f.write(title.replace('\n',""))
                    f.write('\n\n')
                    for line in lines:
                        if not line.startswith("－－－"):
                            f.write("    ")
                        f.write(line)
                        f.write('\n')
            finally:
                start_page += 1
        print('{}——爬取完毕'.format(book_name))
