#!/usr/bin/env python
import redis
import json
import web

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool = pool)

urls = (
    '/instances', 'all',
    '/instance/([\w\d\.-_]+)', 'instance',
    '/instance/(\d+)/history', 'instance_history'
)

class all:
    def GET(self):
        pass

    def POST(self):
        resp = {'code': 200, 'message': 'ok'}
        try:
            data = web.data()
            obj  = json.loads(data)
            #TODO:
            
            inst = Instance(obj['domain'], obj['backend'], obj['start_ip'], obj['end_ip'])
            if inst.save():
                resp['code'] = 500
                resp['message'] = 'could not save'
        except Exception,e:
            resp['code'] = 500
            resp['message'] = e.message
        return json.dumps(resp)

    def iprange_from_str(self, ip):
        pass #TODO

class instance:
    def GET(self, iid):
        print iid
        return Instance.get(iid)

    def POST(self):
        resp = {}
        try:
            data = web.data()
        except Error,e:
            resp['code'] = 500
            resp['error'] = e
            return json.dumps(resp)
        return 'ok'

class Instance:
    def __init__(self, domain, backend = None, start_ip = None, end_ip = None):
        self.domain = domain
        self.backend = backend
        self.start_ip = start_ip
        self.end_ip = end_ip

    def __repr__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get(domain):
        ret = r.hmget(domain, "backend", "start_ip", "end_ip")
        if ret:
            return Instance(domain, ret[0], ret[1], ret[2])
        return None

    @staticmethod
    def delete(domain):
        ret = r.delete(backend)
        if ret:
            return Instance(ret[0], ret[1], ret[2])
        return None

    def save(self):
        ret = r.hmset(self.domain,self.__dict__)
        return ret
    
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
