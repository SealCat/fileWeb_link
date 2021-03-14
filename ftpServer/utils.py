import os
import time
from flask import Markup
from werkzeug.routing import BaseConverter
import struct
from pprint import pprint

def pare_lnk(p):
    with open(p, 'rb') as stream:
        content = stream.read()
        # skip first 20 bytes (HeaderSize and LinkCLSID)
        # read the LinkFlags structure (4 bytes)
        lflags = struct.unpack('I', content[0x14:0x18])[0]
        position = 0x18
        # if the HasLinkTargetIDList bit is set then skip the stored IDList
        # structure and header
        if (lflags & 0x01) == 1:
            position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
        last_pos = position
        position += 0x04
        # get how long the file information is (LinkInfoSize)
        length = struct.unpack('I', content[last_pos:position])[0]
        # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
        position += 0x0C
        # go to the LocalBasePath position
        lbpos = struct.unpack('I', content[position:position + 0x04])[0]
        position = last_pos + lbpos
        # read the string at the given position of the determined length
        size = (length + last_pos) - position - 0x02
        temp = struct.unpack('c' * size, content[position:position + size])
        target = b''.join(temp).decode('gbk')
        return target.replace('\\', '/')


# '':'icon icon-directory',
# 'mp4':'icon icon-mp4 icon-video',
# 'css':'icon icon-css icon-text-css',
# 'js':'icon icon-js icon-application-javascript'
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


content = {}
path = {'url': '/', 'name': '..', 'type': 'icon icon-directory', 'size': '', 'data': ''}
i = {'url': '/', 'name': '~'}
ty = {
    '': 'icon icon-directory',
    'lnk': 'icon icon-directory',
    'mp4': 'icon icon-mp4 icon-video',
    'm4a': 'icon icon-mp4 icon-video',
    'css': 'icon icon-css icon-text-css',
    'js': 'icon icon-js icon-application-javascript',
    'jpg': 'icon icon-jpg icon-image',
    'jpeg': 'icon icon-jpg icon-image',
    'png': 'icon icon-jpg icon-image',
    'gif': 'icon icon-jpg icon-image',
    'ico': 'icon icon-jpg icon-image',
    'zip': 'icon icon-zip',
    'html': 'icon icon-html',
    'pdf': 'icon icon-pdf',
    'xlsx': 'icon icon-xlsx',
    'csv': 'icon icon-xlsx',
    'doc': 'icon icon-doc',
    'txt': 'icon icon-txt',
    'mp3': 'icon icon-mp3',
    'other': 'icon icon-other',
}


def form(top, non):
    global content
    for _dir in non:
        pat = path.copy()
        pat['url'] = top + _dir if top == 'static/' else top.split('/')[-2] + '/' + _dir
        pat['name'] = _dir
        typ = ty.get(_dir.rsplit('.', 1)[-1] if '.' in _dir else '' if os.path.isdir(top + _dir) else 'other',
                     'icon icon-other')
        pat['type'] = typ
        pat['size'] = '%.2f KB' % (os.stat(top + _dir).st_size / 1024)
        pat['data'] = time.ctime(os.stat(top + _dir).st_mtime)
        content['paths'].append(pat)


def df():
    global content
    li = content['title'][:-1].split('/')
    s = '<a href="%s">%s</a> /'
    t = ''
    for k, o in enumerate(li):
        t += s % ('/'.join(li[:k + 1]).replace('~/', '/').replace('~', '/'), o)
    content['li'] = Markup(t)


def get(t):
    global content
    content = {
        "title": '',
        "paths": [],
        "li": []
    }
    top, dirs, non_dirs = os.walk(t).__next__()
    form(top, dirs)  # 解析文件夹
    form(top, non_dirs)  # 解析文件
    content['title'] = '~/' + top
    df()
    return content


def get2(f_path, ral_path):
    global content
    l = lambda k: k if k.endswith('/') else k + '/'
    f_path = l(f_path)
    ral_path = l(ral_path)
    get(ral_path)

    if f_path.endswith('.lnk/'):
        for i in content['paths']:
            i['url'] = f_path.strip('/').rsplit('/',1)[-1]+'/'+i['url'].split('/')[-1]
    content['title'] = '~/' + f_path
    df()
    # pprint(content)
    return content
