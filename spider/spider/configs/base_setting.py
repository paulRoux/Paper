MONGODB = {
    "uri": "mongodb://localhost:27017/",
    "db": "search_word",
    "collection": "words"
}

REDIRECT_DATA = {
    "Referer": "",  # 需要在check_redirect里面设置
    "User-Agent": "",  # 需要在check_redirect里面设置
    "Content-Type": "text/html; charset=utf-8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

# 知网PC请求数据
CNKI_URL = {
    "base_url": "http://kns.cnki.net",
    "home_url": "http://kns.cnki.net/kns/request/SearchHandler.ashx?action=&NaviCode=*&",
    "list_url": "http://kns.cnki.net/kns/brief/brief.aspx?",
    "current_referer": "http://kns.cnki.net/kns/brief/default_result.aspx"
}

CNKI_START = {
    "txt_1_sel": "SU$%=|",
    "txt_1_value1": "",  # 需要在start_requests里面设置
    "txt_1_special1": "%",
    "PageName": "ASP.brief_default_result_aspx",
    "ConfigFile": "SCDBINDEX.xml",
    "DbPrefix": "SCDB",
    "db_opt": "CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD",
    "his": 0,
    "ua": "1.11",
    "isinEn": "1",
    "parentdb": "SCDB",
    "__": ""  # 需要在start_requests里面设置
}

CNKI_PARSE = {
    "pagename": "ASP.brief_default_result_aspx",
    "isinEn": "1",
    "dbPrefix": "SCDB",
    "dbCatalog": "中国学术文献网络出版总库",
    "ConfigFile": "SCDBINDEX.xml",
    "research": "off",
    "t": "",   # 需要在parse里面设置
    "keyValue": "",  # 需要在parse里面设置
    "S": "1",
    "sorttype": "",
}

CNKI_PARSE_LIST = {
    "curpage": "",  # 需要在parse_list_first里面设置
    "RecordsPerPage": 20,
    "QueryID": 2,
    "ID": "",
    "turnpage": 1,
    "tpagemode": "L",
    "dbPrefix": "SCDB",
    "Fields": "",
    "DisplayMode": "listmode",
    "PageName": "ASP.brief_default_result_aspx",
    "isinEn": 1
}

# 万方的请求数据
WANFANG = {
    "searchType": "all",
    "showType": "detail",
    "pageSize": 20,
    "searchWord": "",  # 需要在start_requests里面设置
    "isTriggerTag": ""
}

WANFANG_NEXT = {
    "beetlansyId": "aysnsearch",
    "searchType": "all",
    "pageSize": 20,
    "page": "",  # 需要在parse_link_list设置
    "searchWord": "",  # 需要在parse_link_list设置
    "order": "correlation",
    "showType": "detail",
    "isCheck": "check",
    "isHit": "",
    "isHitUnit": "",
    "firstAuthor": "false",
    "rangeParame": "",
    "navSearchType": "all"
}

WANFANG_ITEM = {
    "_type": "",
    "id": ""
}

# 知网手机端请求数据
CNKI_WAP_START = {
    "kw": "",
    "field": 5
}

CNKI_WAP_PARSE = {
    "searchtype": "0",
    "dbtype": "",
    "pageindex": "1",
    "pagesize": "10",
    "theme_kw": "",
    "title_kw": "",
    "full_kw": "",
    "author_kw": "",
    "depart_kw": "",
    "key_kw": "",
    "abstract_kw": "",
    "source_kw": "",
    "teacher_md": "",
    "catalog_md": "",
    "depart_md": "",
    "refer_md": "",
    "name_meet": "",
    "collect_meet": "",
    "keyword": "",
    "remark": "",
    "fieldtype": "101",
    "sorttype": "0",
    "articletype": "-1",
    "screentype": "0",
    "isscreen": "",
    "subject_sc": "",
    "research_sc": "",
    "depart_sc": "",
    "sponsor_sc": "",
    "author_sc": "",
    "teacher_sc": "",
    "subjectcode_sc": "",
    "researchcode_sc": "",
    "departcode_sc": "",
    "sponsorcode_sc": "",
    "authorcode_sc": "",
    "teachercode_sc": "",
    "starttime_sc": "",
    "endtime_sc": "",
    "timestate_sc": "1"
}


# 爱学术
IXUESHU_START = {
    "q": "",
    "sort": "year desc"
}

IXUESHU_LINK = {
    "q": "",
    "sort": "year desc",
    "page": ""
}
