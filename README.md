
# django on synology nas


## 마그넷 형태
```
magnet:?xt=urn:btih:ADE00BD4FC380206C0B56F0502D879A360337FCE&dn=Your.Pretty.Face.Is.Going.To.Hell.S03E08.720p+HDTV.x264-W4F&tr=udp://tracker.openbittorrent.com:80&tr=http://megapeer.org:6969/announce&tr=http://mgtracker.org:2710/announce&tr=http://tracker.files.fm:6969/announce&tr=http://tracker.flashtorrents.org:6969/announce&tr=http://tracker.mg64.net:6881/announce&tr=http://tracker.nwps.ws:6969/announce&tr=http://tracker.ohys.net/announce&tr=http://tracker.tfile.me/announce&tr=udp://9.rarbg.com:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=udp://coppersurfer.tk:6969/announce&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://exodus.desync.com:6969/announce&tr=udp://open.coppersurfer.com:1337/announce
```



## 시놀로지에 GCC 설치
- http://blog.nuwana.com/144

```sh
ipkg install gcc
ipkg install make
ipkg install automake  
```

ipkg install libxslt
ipkg install libxml2
ipkg install py3-lxml



## cc
- https://forum.synology.com/enu/viewtopic.php?t=35326

Re: C compiler on Synology?
by runekock » Wed Mar 30, 2011 11:42 pm
ipkg install optware-devel
should give you all the basic stuff.


## pymysql


pymysql 을 설치하고, base.py파일을 수정함


```sh
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
db = MySQLdb.connect("localhost" , "root" , "password")
```

2줄 추가함

```python
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb as Database
except ImportError as e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("Error loading MySQLdb module: %s" % e)

```


I solved it this way: download the zipped package from [here](https://pypi.python.org/pypi/mysql-connector-python) and follow this set of instructions:

unzip  /path/to/downloads/folder/mysql-connector-python-VER.zip
In case u got a .gz u can use ->

tar xzf mysql-connector-python-VER.tar.gz

cd mysql-connector-python-VER

sudo python3 setup.py install # NOTICE I USED PYTHON3 INSTEAD OF PYTHON
You can read about it here


심볼릭 링크 생성
```
ln -s /volume1/mysql-5.5.39-linux2.6-i686/bin/mysql_config /usr/bin/mysql_config
```

ipkg 로 설치된 경로 : /opt/bin/mysql_config

```
ln -s /opt/bin/mysql_config /usr/bin/mysql_config
```

## ipkg 설치

https://nas.moe/archives/1372 참조하여 ipkg 설치

패키지 소스 – 추가

- 이름: cphub
- 위치: https://www.cphub.net

perl 설치
Easy Bootstrap Installer 설치
iPKGui 설치



git ignore 에 추가한  settings.py 파일을 복사한다

http://ilizaran.blogspot.kr/2014/09/instalacion-del-modulo-mysql-python-en.html


## ssh

```sh
ssh [id]@[domain] -p [port]
```


## 설치

윈도우즈
```sh
pip install mysqlclient
```

MAC
```sh
brew install mysql
export PATH=$PATH:/usr/local/mysql/bin
pip install mysqlclient
```

synology
```sh
pip3.5 install mysqlclient
pip3.5 install python-firebase
pip3.5 install beautifulsoup4
pip3.5 install feedgen
```

## start app

start app
```sh
python manage.py startapp torrent
```
