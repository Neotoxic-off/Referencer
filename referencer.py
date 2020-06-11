#!/usr/bin/env python3

import requests
import sys
import os
from lib import status
from lib import colors

class settings:
    URL = None
    OUT = "list.txt"

def progress(message):
    sys.stdout.write('\b' * len(message))
    sys.stdout.flush()
    sys.stdout.write(message)

def clean(line):
    ref = ""
    count = 0
    i = 0

    while i < len(line) and count != 2:
        if line[i] == '"' or line[i] == '\n':
            count += 1
        if count == 1 and line[i] != '"':
            ref += line[i]
        i += 1
    return (ref)

def resume(array):
    i = 0
    print("%s Removing '%s'" % (status.working(), settings.OUT))
    if os.path.exists(settings.OUT):
        os.remove(settings.OUT)
    print("%s Updating '%s'" % (status.working(), settings.OUT))
    f = open(settings.OUT, 'w+')

    while i < len(array):
        progress("%s %s%d%s References written" % (status.info(), colors.cyan(), i, colors.reset()))
        f.write("%s\n" % (array[i]))
        i += 1
    sys.stdout.write("\n")
    f.close()

def parse(r):
    current = None
    count = 0
    i = 1
    data = r.text.split('href=')
    href = []

    while i < len(data):
        if len(data[i]) >= 1:
            href.append(clean(data[i]))
            count += 1
            progress("%s %s%d%s References founds" % (status.info(), colors.cyan(), count, colors.reset()))
        i += 1
    sys.stdout.write("\n")
    resume(href)

def connect():
    print("%s Connecting" % status.working())
    try:
        r = requests.get(settings.URL)
        if r.status_code == 200:
            print("%s Connection accepted" % status.ok())
            print("%s Referencing" % status.working())
            parse(r)
        else:
            print("%s Connection rejected" % status.ko())
    except:
        print("%s Something wrong happenned" % status.error())
        exit(-1)

def init():
    settings.URL = input("%s URL: " % status.input())
    connect()

init()