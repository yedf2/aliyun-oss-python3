import base64
import hmac
from hashlib import sha1
import time
try:
    import urllib.request as urllib
except ImportError:
    import urllib2 as urllib

accessKeyId = 'xxxxx'
accessKeySecret = 'xxxxx'

# use signature in url
def _oss_file_url(method, bucket, filename, content_type):
    now = int(time.time())
    expire = now - (now % 1800) + 3600 # expire will not different every second
    tosign = "%s\n\n\n%d\n/%s/%s" % (method, expire, bucket, filename)
    if method == 'PUT' or method == 'POST':
        tosign = "%s\n\n%s\n%d\n/%s/%s" % (method, content_type, expire, bucket, filename)
    h = hmac.new(accessKeySecret.encode(), tosign.encode(), sha1)
    sign = urllib.quote(base64.encodestring(h.digest()).strip())
    return 'http://%s.oss-cn-hangzhou.aliyuncs.com/%s?OSSAccessKeyId=%s&Expires=%d&Signature=%s' % (
        bucket, filename, accessKeyId, expire, sign
    )

def get_file_url(bucket, filename):
    return _oss_file_url('GET', bucket, filename, None)


def http_put(bucket, filename, cont, content_type):
    url = _oss_file_url('PUT', bucket, filename, content_type)
    req = urllib.Request(url, cont)
    req.get_method = lambda: 'PUT'
    req.add_header('content-type', content_type)
    try:
        return urllib.urlopen(req)
    except urllib.HTTPError as e:
        print(e)

http_put('fast-loan', 'mytestkey', b'sample value', 'text/plain')
url = get_file_url('fast-loan', 'mytestkey')
print(urllib.urlopen(url).read())