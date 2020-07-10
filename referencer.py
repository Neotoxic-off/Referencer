#!/usr/bin/env python3

import sys
import os
import shutil
import requests
import argparse

class settings:
    DATA      = []
    EXTENSION = []
    EXCEPTION = []
    OUT       = None
    TIMEOUT   = 5
    CLEAN     = True

def color(c):
    colors = {
        "reset"  : "0",
        "red"    : "1;31",
        "green"  : "1;32",
        "yellow" : "1;33",
        "blue"   : "1;34",
        "purple" : "1;35",
        "cyan"   : "1;36"
    }
    return ("\033[%sm" % (colors.get("%s" % c)))

def status(s):
    statuses = {
        "download" : "%s ~> %s " % (color("yellow"), color("reset")),
        "ko"       : "%s KO %s" % (color("red"),    color("reset")),
        "ok"       : "%s OK %s" % (color("green"),  color("reset")),
        "info"     : "%s ?? %s" % (color("purple"), color("reset")),
        "done"     : "%sDONE%s" % (color("green"), color("reset")),
        "error"    : "%s E: %s" % (color("red"),    color("reset")),
    }
    return (statuses.get("%s" % s))

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

def exception(element):
    total = 0

    if len(settings.EXCEPTION) > 0:
        for i in range(0, len(settings.EXCEPTION)):
            if element.endswith(settings.EXCEPTION[i]) == False:
                return (1)
            total += 1
        if total == len(settings.EXCEPTION):
            return (0)
    return (1)

def extension(element):
    total = 0

    if len(settings.EXTENSION) > 0:
        for i in range(0, len(settings.EXTENSION)):
            if element.endswith(settings.EXTENSION[i]):
                return (1)
            total += 1
        if total == len(settings.EXCEPTION):
            return (0)
    return (0)

def download(element):
    if extension(element) == 1 and exception(element) == 1:
        try:
            print("%s  %s" % (status("download"), element))
            os.system("wget %s --directory-prefix=%s -O %s/%s -q" % (element, settings.OUT, settings.OUT, exists(element)))
            return (1)
        except:
            print("%s  %s" % (status("error"), element))
            return (-1)
    return (0)

def resume(array):
    for i in range(0, len(array)):
        if array[i].startswith("https://") and check(array[i]) == 0:
            print("%s  %s" % (status("ok"), array[i]))
            settings.DATA.append(array[i])

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

def count_char(str, char):
    total = 0

    for i in range(0, len(str)):
        if str[i] == char:
            total += 1
    return (total)

def extract(path, c):
    cleanned = ""
    count = 0
    total = count_char(path, c)

    if path[len(path) - 1] == c:
        total -= 1
    for i in range(0, len(path)):
        if path[i] == c:
            count += 1
        if path[i] != c and count == total:
            cleanned += path[i]
    return (cleanned)

def exists(path):
    name = extract(path, '/').split('.')[0]
    ext  = extract(path, '/').split('.')[1]
    i = 0
    content = "%s_%d.%s" % (name, i, ext)

    while os.path.exists("%s/%s" % (settings.OUT, content)):
        content = "%s_%d.%s" % (name, i, ext)
        i += 1
    return (content)

def folder():
    if os.path.isdir(settings.OUT):
        try:
            shutil.rmtree(settings.OUT)
        except:
            exit(-1)
    os.mkdir(settings.OUT)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output",    action = "store", default = "referenced", help = "Directory to store content")
    parser.add_argument('-l', '--list',      nargs  = '*',     default = [],           help = "Extension's content to download")
    parser.add_argument("-e", "--exception", nargs  = '*',     default = [],           help = "Extension's content not to download")
    parser.add_argument("-u", "--url",       nargs  = '*',     default = [],           help = "Url to extract", required = True)
    args = parser.parse_args()
    settings.EXTENSION = args.list
    settings.EXCEPTION = args.exception
    settings.OUT       = args.output
    settings.DATA      = args.url

def connect():
    i = 0

    arguments()
    folder()
    while settings.DATA[i]:
        try:
            if download(settings.DATA[i]) != 1:
                r = requests.get(settings.DATA[i], timeout = settings.TIMEOUT)
                if r.status_code == 200:
                    parse_href(r)
                    parse_src(r)
                    print("%s  %s" % (status("ok"), settings.DATA[i]))
                else:
                    print("%s  %s" % (status("ko"), settings.DATA[i]))
        except:
            print("%s  %s" % (status("error"), settings.DATA[i]))
        i += 1

connect()
