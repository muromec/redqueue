import urllib
from redqueue import task
from tornado.httpclient import AsyncHTTPClient

BASE = 'http://api.ipinfodb.com/v3/ip-city'

class GeoipTask(task.Task):
    key = 'task:geoip'

    def __init__(self, server, token):
        self.token = token
        super(GeoipTask, self).__init__(server)

    def on_data(self, data):
        url_back = data['url']

        def handle_response(response):
            if response.code != 200:
                return

            body = urllib.urlencode({"response": response.body})
            http_client.fetch(url_back, lambda x:x, body=body, method='POST')

        http_client = AsyncHTTPClient()
        params = urllib.urlencode({
            "key": self.token,
            "format": "json",
            "ip": data['ip'],
            })
        url = '%s?%s' % (BASE, params)

        http_client.fetch(url, handle_response)

