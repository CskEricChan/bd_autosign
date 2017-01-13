#-*- coding: utf8 -*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dict_header = {
	"Cookie":"",
	"DNT":"1",
	"User-Agent":"Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352"
}
base_url = "https://tieba.baidu.com" 
session = requests.Session()
session.headers.update(dict_header)
res = session.get(base_url)
#print res.encoding
#print res.text

html = res.text
pattern = re.compile(r'\<a href\=\"([^\>]*?tab=favorite)\"\>[^\<]*?\<\/a\>')
rs = pattern.search(html)
#print "######################"
#print rs
if rs == None:
	#print "Error, please check.."
	sys.exit(1);
url_newbase = (base_url + rs.group(1)).split('/')[:-1]
tmp_url = url_newbase[0]
for s in url_newbase[1:]:
	tmp_url += '/' + s 
url_newbase = tmp_url
res = session.get(base_url + rs.group(1))
html = res.text
#print html
iter = re.finditer('\<tr[^\>]*?\>\<td\>([^\<]*?)\<a href\=\"([^\>]*?)\"\>([^\<]*?)\<\/a\>\<\/td\>\<td[^\>]*?>([^\<]*?)\<\/td\>\<td[^\>]*?>([^\<]*?)\<\/td\>\</tr\>',html)
#list_url = re.findall(pattern, html)
#print len(list_url)

list_message = []
for m in iter:
	list_message.append(m.groups())
url_tmp = url_newbase.replace(base_url,'')
pattern = re.compile(r'\<a href\=\"([^\>]*?\/sign\?[^\>]*?)\"\>[^\<]*?\</a\>')
for ls in list_message:
	#print 'visit', ls[2], ls[3],ls[4],'...'
	#print ls[1]
	page_url = url_newbase+ls[1]
	res = session.get(page_url)
	match = re.search(pattern,res.text)
	#print "match",match
	if match:
		url_sign = base_url + match.group(1)
		url_sign = url_sign.replace('&amp;','&')
		#print url_sign
		#print page_url

		#print ls[2],'正在签到..'
		res = session.get(url_sign,headers={"Refer":page_url},allow_redirects=True);
		#print "res.url:", res.url
		#print res.status_code
		#print ls[2], '已签到..'

	else:
		pass;
		#print ls[2], '已签到..'
