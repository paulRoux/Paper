import logging
from urllib import request
from http import cookiejar
from urllib.error import HTTPError
from spider.configs import base_setting


def check_redirect(url, ref):
    try:
        # print(url, ref)
        base_setting.REDIRECT_DATA['Referer'] = ref
        cookie = cookiejar.CookieJar()
        opener = request.build_opener(request.HTTPCookieProcessor(cookie))
        request.install_opener(opener)
        req = request.Request(url=url, headers=base_setting.REDIRECT_DATA)
        resp = request.urlopen(req)
        if resp.status is 302 and 'Location' in resp.headers:
            redirect_url = str(resp.headers['Location'], encoding='utf-8')
            return redirect_url
        else:
            return url
    except HTTPError as e:
        logging.log(msg="redirect error! "+e.msg, level=logging.ERROR)
        return None
