# coding=utf-8
import datetime,string,random
import time
import oss2
now = datetime.datetime.now()
random_name = now.strftime("%Y%m%d%H%M%S") + ''.join([random.choice(string.digits) for _ in range(1,4)]) # 自定义随机名称
 
auth = oss2.Auth('your-Accesskey', 'your-AccessKeySecret')
bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'your-username', connect_timeout=30)
 
# 1) 直接上传文件put_object_from_file
result = bucket.put_object_from_file(filename, 'file')
if result.status == 200:
    url = '%s' % (filename)
    print(url)
 
# 2）指定方式上传put_object，支持上传
#       1）字符串，2）bytes：直接上传，3）unicode：会自动转换为UTF-8编码的bytes进行上传，
#       4）上传本地文件以文件对象方式：必须以二进制的方式打开文件，因为内部实现需要知道文件包含的字节数
bucket.put_object('remote.txt', 'content of object')
bucket.put_object('remote.txt', b'content of object')
bucket.put_object('remote.txt', u'content of object')
with open('local_file', 'rb') as fileobj:
    result = bucket.put_object(filename, fileobj)
    if result.status == 200:
        print('http url: {0}'.format(filename))  # 上传文件生成的url，可以用它进行下载或查看
        print('http status: {0}'.format(result.status)) # HTTP返回码，成功返回200
        print('request_id: {0}'.format(result.request_id))  # 请求ID，强烈建议把它作为程序日志的一部分
        print('ETag: {0}'.format(result.etag))  #  etag则是put_object返回值特有的属性
        print('date: {0}'.format(result.headers['date']))  # HTTP响应头部
 
# 1) get_object下载,然后通过shutil将文件内容拷贝到另一个文件， 它的返回值是一个类文件对象（file-like object），同时也是一个可迭代对象（iterable）
remote_stream = bucket.get_object(filenam)
with open('jianji01.jpg', 'wb') as local_fileobj:
    import shutil
    shutil.copyfileobj(remote_stream, local_fileobj)
 
# 2）Bucket.get_object_to_file 直接下载到本地文件
result = bucket.get_object_to_file(filenam, 'local_file')
if result.status == 200:
    print('success')
 
# 列出两个文件
from itertools import islice
for b in islice(oss2.ObjectIterator(bucket), 2):
    print(b.key)
