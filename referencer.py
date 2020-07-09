#!/usr/bin/env python3

import requests
import sys
import os
from lib import status
from lib import colors

class settings:
    URL  = None
    FILE = "data.txt"
    DATA = []

def ALL():
    return (settings.DATA)

def clean(line):
    ref = ""
    count = 0
    i = 0

    while i < len(line) and count != 1:
        if line[i] == '"' or line[i] == '\n':
            count += 1
        if count == 0 and line[i] != '"':
            ref += line[i]
        i += 1
    return (ref)

def check(url):
    for i in range(0, len(settings.DATA)):
        if url == settings.DATA[i]:
            return (1)
    return (0)

def resume(array):
    for i in range(0, len(array)):
        if array[i].startswith("https://") and check(array[i]) == 0:
            print(array[i])
            settings.DATA.append(array[i])
            if array[i].endswith("/") == False:
                os.system("wget -q %s" % (array[i]))

def parse_href(r):
    count = 0
    data = r.text.split('href="')
    href = []

    for i in range(1, len(data)):
        if len(data[i]) >= 1:
            href.append(clean(data[i]))
            count += 1
    resume(href)

def parse_src(r):
    count = 0
    data = r.text.split('src="')
    src = []

    for i in range(1, len(data)):
        if len(data[i]) >= 1:
            src.append(clean(data[i]))
            count += 1
    resume(src)

def connect():
    i = 0

    while settings.DATA[i]:
        print("=> %s" % settings.DATA[i])
        r = requests.get(settings.DATA[i])
        if r.status_code == 200:
            parse_href(r)
            parse_src(r)
        i += 1

settings.DATA.append(input("url: "))
connect()
