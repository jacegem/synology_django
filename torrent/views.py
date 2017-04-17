import logging
import re
import socket
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Magnet

# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


def rss(request):
    latest_magnet_list = Magnet.objects.order_by('-id')[:1000]

    trackers = '&tr=udp://tracker.openbittorrent.com:80&tr=http://megapeer.org:6969/announce&tr=http://mgtracker.org:2710/announce&tr=http://tracker.files.fm:6969/announce&tr=http://tracker.flashtorrents.org:6969/announce&tr=http://tracker.mg64.net:6881/announce&tr=http://tracker.nwps.ws:6969/announce&tr=http://tracker.ohys.net/announce&tr=http://tracker.tfile.me/announce&tr=udp://9.rarbg.com:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=udp://coppersurfer.tk:6969/announce&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://exodus.desync.com:6969/announce&tr=udp://open.coppersurfer.com:1337/announce'

    rss_content = '<?xml version="1.0" encoding="UTF-8"?>' +\
        '<rss xmlns:showrss="http://showrss.info" version="2.0">' +\
        '<channel>' +\
        '<title>RSS</title>' +\
        '<link>http://attr.cf</link>' + \
        '<ttl>30</ttl>' + \
        '<description>RSS</description>'

    for magnet in latest_magnet_list:
        magnet.title = re.sub(r'"', r"", magnet.title)
        rss_content += '<item>'
        rss_content += '<title>' + magnet.title + '</title>'
        rss_content += '<link>' + magnet.magnet + '</link>'
        m = re.search('(?<=btih:).*', magnet.magnet)
        info_hash = m.group(0)
        rss_content += '<guid ispermalink="false">' + info_hash + '</guid>'
        rss_content += '<showrss:info_hash>' + info_hash + '</showrss:info_hash>'
        rss_content += '<showrss:showname>' + magnet.title + '</showrss:showname>'
        enclosure_url = magnet.magnet + '&dn=' + magnet.title + trackers
        rss_content += '<enclosure url = "' + enclosure_url + '" length = "0" type = "application/x-bittorrent"></enclosure>'
        rss_content += '</item>'

    rss_content += '</channel></rss>'
    rss_content = rss_content.replace('&', '&amp;')

    return HttpResponse(rss_content)


def index(request):
    return render(request, 'torrent/index.html')


def collect_tfreeca():
    url_home = 'http://www.tfreeca2.com/'
    url_ref_map = {
        'movie': 'board.php?mode=list&b_id=tmovie',
        'tv': 'board.php?mode=list&b_id=tdrama',
        'tv': 'board.php?mode=list&b_id=tent',
        'tv': 'board.php?mode=list&b_id=tv',
        'ani': 'board.php?mode=list&b_id=tani',
        'music': 'board.php?mode=list&b_id=tmusic',
        'util': 'board.php?mode=list&b_id=util',
    }

    result = list()

    for category, url_ref in url_ref_map.items():
        bs = get_bs(url_home, url_ref)
        bs_trs = bs.find('table', {'class': 'b_list'}).findAll('tr')

        for bs_tr in bs_trs:
            if 'class' in bs_tr.attrs:
                tr_class = bs_tr.attrs['class'][0]
                if tr_class == 'nbgcolor':
                    continue
            href = bs_tr.find("a", {"class": re.compile(r'title')})['href']
            bs_content = get_bs(url_home, href)
            title = bs_content.find('td', {'class': 'view_t2'})['title']
            torrent_src = bs_content.find('iframe', {'id': 'external-frame'})['src']
            bs_torrent = get_bs(url_home, torrent_src)
            magnet = bs_torrent.find('div', {'class': 'torrent_magnet'}).find('a')['href']

            obj = save_data(title, magnet, href, category)

            result.append(obj)

            # if created:
            #     logging.debug(title, " added")
            # else:
            #     logging.debug(title, " exist")

    return result


@csrf_exempt
def collect(request):
    result = collect_torrentwiz()
    # result = collect_tfreeca()

    return render(request, 'torrent/collect.html', {'result': result})


def get_bs(url_home, url_ref=""):
    url = url_home + url_ref
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read()
        bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    except socket.timeout:
        print(url)
    return bs


def collect_torrentwiz():
    url_home = 'https://torrentwiz4.com/'
    url_ref_list = [
        ['tv', 'torrent_ent'],
        ['tv', 'torrent_sisa'],
        ['tv', 'torrent_drama'],
        ['movie', 'torrent_movieko'],
        ['movie', 'torrent_movielatest'],
        ['music', 'torrent_kpop'],
        ['music', 'torrent_pop'],
        ['ani', 'torrent_ani'],
        ['ani', 'torrent_aniend'],
        ['comic', 'torrent_cartoon'],
        ['game', 'torrent_game'],
        ['util', 'torrent_util'],
    ]

    result = list()

    for url_ref in url_ref_list:
        category = url_ref[0]
        url = url_ref[1]
        bs = get_bs(url_home, url)
        bs_trs = bs.find('table', {'class': 'list-pc'}).find('tbody').findAll('tr')

        for bs_tr in bs_trs:
            td_num = bs_tr.find('td', {'class': 'td_num'}).text
            if td_num == 'AD':
                continue
            href = bs_tr.find('td', {'class': 'list-subject'}).find('a')['href']
            # 상세 페이지 이동
            bs_content = get_bs(href)
            title = bs_content.find('div', {'class': 'view-wrap'}).find('h1').text
            a_tags = bs_content.findAll('a', {'class': 'view_file_download'})
            for a_tag in a_tags:
                m = re.search('(magnet:\?xt=urn:btih:.+?)&', a_tag['href'])
                if m is not None:
                    magnet = m.group(1)
                    break

            # print(title)
            obj = save_data(title, magnet, href, category)
            result.append(obj)

    return result


def save_data(title, magnet, url, category):
    try:
        obj = Magnet.objects.get(magnet=magnet)
    except Magnet.DoesNotExist:
        obj = Magnet(title=title, magnet=magnet, url=url, category=category)
        obj.save()

    return obj
