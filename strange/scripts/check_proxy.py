import os
import sys
from os.path import dirname

_env_path = dirname(dirname(dirname(os.path.abspath(__file__))))
sys.path.append(_env_path)

import socket
import urllib.request
from datetime import timedelta, datetime

from strange.database import Proxy
from strange.database.session import Session

session = Session().session
target_url = 'http://www.baidu.com'
timeout = 2
already_check_upper = 1000

socket.setdefaulttimeout(timeout)

def check(id):
    proxy = session.query(Proxy).filter(Proxy.id == id).first()
    p = (urllib
         .request
         .ProxyHandler({'http': '{}:{}'.format(proxy.ip, proxy.port)}))
    opener = urllib.request.build_opener(p)
    urllib.request.install_opener(opener)
    now = datetime.now()
    try:
        urllib.request.urlopen(target_url)
    except Exception as e:
        proxy.status = 1
        proxy.updated_at = now
        session.commit()
        print('{}:{} is not ok!'.format(proxy.ip, proxy.port))
    else:
        if not (proxy.status == 1 and proxy.on_duration != timedelta()):
            updated_at = proxy.updated_at
            on_duration = proxy.on_duration + (now - updated_at)
            proxy.on_duration = on_duration
        proxy.status = 0
        proxy.updated_at = now
        session.commit()
        print('{}:{} is ok!'.format(proxy.ip, proxy.port))


if __name__ == "__main__":
    # 最新入库的都需要检查一遍
    need_check = (session
                .query(Proxy)
                .filter(Proxy.created_at == Proxy.updated_at))
    need_check_ids = [f.id for f in need_check]

    # 以前曾经可用的数据抽取可用时间最长的一部分检查
    once_available = (session
                      .query(Proxy)
                      .filter(Proxy.on_duration != timedelta())
                      .order_by(-Proxy.on_duration)
                      .limit(already_check_upper))
    once_available_ids = [o.id for o in once_available]
    ids = need_check_ids.extend(once_available_ids)
    for id in need_check_ids:
        check(id)

    session.close()
