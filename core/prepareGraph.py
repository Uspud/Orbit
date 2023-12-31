import json
import random

def prepareGraph(filename, json_dump):
    just_nodes = []
    jsoned = {'nodes': [], 'edges': []}

    data = 'var rendru = ' + json_dump
    savefile = open('%s.js' % filename, 'w+', encoding='utf-8')
    savefile.write(data)
    savefile.close()

    quark = open('quark.html', 'r', encoding='utf-8')
    lines = quark.readlines()
    lines[6] = '<script id="ourfile" src="%s"></script>\n' % (filename + '.js')
    with open('quark.html', 'w+', encoding='utf-8') as quark_save:
        for line in lines:
            quark_save.write(line)

    quark.close()