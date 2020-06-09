import urllib.request
from lxml.html import parse
import xml.etree.ElementTree as ET
from .config import version as conf
import gevent
import time
import gevent.monkey


def fetch():
    gevent.monkey.patch_all()
    start = time.time()
    input = ET.parse('banks.xml')
    data = ET.Element('data')
    if conf == 1:
        for bank in input.findall('bank'):
            html = urllib.request.urlopen(bank.find('url').text)
            page = parse(html).getroot()
            bank1 = ET.SubElement(data, 'bank')
            bank1.set('name', bank.get('name'))
            for currency in bank.findall('currency'):
                cur = ET.SubElement(bank1, 'currency')
                cur.set('name', currency.get('name'))
                for element in page.xpath(currency.find('sell').text):
                    sell = ET.SubElement(cur, 'sell')
                    sell.text = element.text.strip()
                for element in page.xpath(currency.find('buy').text):
                    buy = ET.SubElement(cur, 'buy')
                    buy.text = element.text.strip()

    if conf == 2:
        def task(bank):
            html = urllib.request.urlopen(bank.find('url').text)
            page = parse(html).getroot()
            bank1 = ET.SubElement(data, 'bank')
            bank1.set('name', bank.get('name'))
            for currency in bank.findall('currency'):
                cur = ET.SubElement(bank1, 'currency')
                cur.set('name', currency.get('name'))
                for element in page.xpath(currency.find('sell').text):
                    sell = ET.SubElement(cur, 'sell')
                    sell.text = element.text.strip()
                for element in page.xpath(currency.find('buy').text):
                    buy = ET.SubElement(cur, 'buy')
                    buy.text = element.text.strip()
            gevent.sleep(0)

        threads = [gevent.spawn(task, bank) for bank in input.findall('bank')]
        gevent.joinall(threads)

    datastring = ET.tostring(data)
    file = open('data.xml', 'wb')
    file.write(datastring)
    file.close()

    end = time.time()
    print(end - start)
