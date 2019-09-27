#coding=utf-8
import requests
import time
import random
import sys
from urllib import parse

headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
	'Origin': 'https://www.lagou.com',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-origin',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
	'X-Anit-Forge-Code': '0',
	'X-Anit-Forge-Token': None,
	'X-Requested-With': 'XMLHttpRequest',
        #'Content-Length': '23',  #这个不固定，加上后反而不能连接网站
    }

def get_json(page,lang_name,city):

    MyParams = {'labelWords':'','fromSearch':'true','suginput':''}
    headers['Referer'] = 'https://www.lagou.com/jobs/list_{}?px=default&city={}'.format(lang_name,city) 
    url_start = 'https://www.lagou.com/jobs/list_{}?px=default&city={}#filterBox'.format(lang_name,city)
    s = requests.Session()
    s.get(url_start,headers=headers,params=MyParams,timeout=3)
    time.sleep(random.uniform(5,15))
    cookie = s.cookies

    data = {'first':'true','pn':str(page),'kd':lang_name}
    MyParams = {'px':'default','city':city,'needAddtionalResult':'false'}
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(city)
    json = s.post(url, data=data, headers=headers,cookies=cookie, timeout=3).json()
    time.sleep(random.uniform(5,15))
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('positionName','no'))
        info.append(i.get('companyShortName','no'))
        info.append(i.get('education','no'))
        info.append(i.get('workYear','no'))
        info.append(i.get('salary','no'))
        info.append(i.get('city','no'))
        info.append(i.get('district','no'))
        info.append(i.get('createTime','no'))
        info.append(i.get('stationname','no'))
        info.append(i.get('jobNature','no'))
        info.append(i.get('industryField','no'))
        info.append(i.get('companySize','no'))
        info.append(i.get('companyFullName','no'))
        info.append(';'.join(i.get('companyLabelList','no')))
        info.append(i.get('positionAdvantage','no'))
        info.append(i.get('firstType','no'))
        info.append(i.get('secondType','no'))
        info.append(i.get('thirdType','no'))
        for i in range(len(info)):
            if info[i] is None:
                info[i] = 'no'
        info_list.append(info)
    return info_list

def main(lang_name,outfile):
    out_hd = open(outfile,'w')
    head_list = ['职位','公司简称','学历要求','工作经验','工资','城市','县区','位置','创建时间', '工作性质','经营范围','公司规模','公司全称','福利待遇','公司优势','类型1','类型2','类型3']
    out_hd.write('\t'.join(head_list)+'\n')
    city_name_list = ['北京','上海','深圳','广州','杭州','成都','南京','武汉','长沙']
    city_num_list = [2,3,215,213,6,25,79,184,198]
    for k in range(len(city_name_list)):
        city_name = parse.quote(city_name_list[k])
        city_num = str(city_num_list[k])
        lang_name = parse.quote(lang_name)
        page = 1
        while page<31:
            t = random.uniform(5,15)
            time.sleep(t)
            result = get_json(page,lang_name,city_name)
            for each in result:
                each_info = '\t'.join(each)
                out_hd.write(each_info+'\n')
                out_hd.flush()
            page += 1
    out_hd.close()

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])

