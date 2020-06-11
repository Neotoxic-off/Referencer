#!/usr/bin/env python3

import requests
import sys
import os
from lib import status
from lib import colors

class settings:
    URL  = None
    HREF = "href.txt"
    SRC  = "src.txt"

def progress(message):
    sys.stdout.write('\b' * len(message))
    sys.stdout.flush()
    sys.stdout.write(message)

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

def resume_href(array):
    i = 0
    print("%s Removing '%s'" % (status.working(), settings.HREF))
    if os.path.exists(settings.HREF):
        os.remove(settings.HREF)
    print("%s Updating '%s'" % (status.working(), settings.HREF))
    f = open(settings.HREF, 'w+')

    while i < len(array):
        f.write("%s\n" % (array[i]))
        i += 1
        progress("%s %s%d%s References written" % (status.info(), colors.cyan(), i, colors.reset()))
    sys.stdout.write("\n")
    f.close()

def resume_src(array):
    i = 0
    print("%s Removing '%s'" % (status.working(), settings.SRC))
    if os.path.exists(settings.SRC):
        os.remove(settings.SRC)
    print("%s Updating '%s'" % (status.working(), settings.SRC))
    f = open(settings.SRC, 'w+')

    while i < len(array):
        f.write("%s\n" % (array[i]))
        i += 1
        progress("%s %s%d%s Sources written" % (status.info(), colors.cyan(), i, colors.reset()))
    sys.stdout.write("\n")
    f.close()

def parse_href(r):
    current = None
    count = 0
    i = 1
    data = r.text.split('href="')
    href = []

    while i < len(data):
        if len(data[i]) >= 1:
            href.append(clean(data[i]))
            count += 1
            progress("%s %s%d%s References founds" % (status.info(), colors.cyan(), count, colors.reset()))
        i += 1
    sys.stdout.write("\n")
    resume_href(href)

def parse_src(r):
    current = None
    count = 0
    i = 1
    data = r.text.split('src="')
    src = []

    while i < len(data):
        if len(data[i]) >= 1:
            src.append(clean(data[i]))
            count += 1
            progress("%s %s%d%s Sources founds" % (status.info(), colors.cyan(), count, colors.reset()))
        i += 1
    sys.stdout.write("\n")
    resume_src(src)

def connect():
    print("%s Connecting" % status.working())
    try:
        r = requests.get(settings.URL)
        if r.status_code == 200:
            print("%s Connection accepted" % status.ok())
            print("%s Referencing" % status.working())
            parse_href(r)
            parse_src(r)
        else:
            print("%s Connection rejected" % status.ko())
    except:
        print("%s Something wrong happenned" % status.error())
        exit(-1)

def init():
    settings.URL = input("%s URL: " % status.input())
    connect()

init()