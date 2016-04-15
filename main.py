#! /usr/bin/env python3

import websocket
import _thread
import time
import json
import unicodedata
import subprocess
import google
import ED


comm = {"|source": "Source: https://github.com/WhiteheadV/ExistentialistBear",
"|help": "Usage: \"|ebear\" [args] (\"-s\" 4 source of last text), , \"|afk [reason(optional)]\", \"|source\"\n,\"|g [query]\", \"|ed [query]\" (Search Encyclopedia Dramatica)",
'owname': 'ExistentialistBear'}

usrstat = {}

usrmsg = {}

def run(*args):
    ws.send(json.dumps({"cmd": "chat", "text": runBear(args).decode('utf-8')}))

def runBear(sors):
    if sors:
        p = subprocess.Popen("./Ebear -s", cwd="/home/theone/Documents/Atom(SSD)/ExistentialistBear/", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output
    else:
        p = subprocess.Popen("./Ebear", cwd="/home/theone/Documents/Atom(SSD)/ExistentialistBear/", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output

def afk(msg):
    if msg['text'].lower()[:4] == '|afk':
        if len(msg['text'].strip()) > 4:
            usrstat[msg['nick']] = msg['text'][4:].strip()
            ws.send(json.dumps({"cmd": "chat", "text": "User @%s is now afk cuz %s." % (msg['nick'], usrstat[msg['nick']])}))
        else:
            usrstat[msg['nick']] = ''
            ws.send(json.dumps({"cmd": "chat", "text": "User @%s is now afk." % (msg['nick'])}))
    elif msg['nick'] != comm['owname'].split('#')[0]:
        for key, val in usrstat.items():
            if '@%s' % (key) in msg['text'] and key != msg['nick']:
                if val != '':
                    ws.send(json.dumps({"cmd": "chat", "text": "@%s user @%s is afk cuz %s." % (msg['nick'], key, val)}))
                    usrmsg[key] = [msg['nick'], msg['text'].strip('@' + key)]
                else:
                    ws.send(json.dumps({"cmd": "chat", "text": "@%s user @%s is afk." % (msg['nick'], key)}))
                    usrmsg[key] = [msg['nick'], msg['text'].strip('@' + key)]
            if msg['nick'] == key:
                if msg['text'][0] == '|' and len(msg['text']) > 1:
                    break
                ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now back.' % (key)}))
                del usrstat[key]
                for k, v in usrmsg.items():
                    if k == msg['nick']:
                        time.sleep(0.5)
                        ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s left:%s.' % (msg['nick'], v[0], v[1])}))
                        del usrmsg[k]
                        break
                break

def heartBeat():
    ws.send(json.dumps({'cmd': 'ping'}))
    while(True):
        time.sleep(50)
        ws.send(json.dumps({'cmd': 'ping'}))

def on_message(ws, message):
    message = json.loads(message)
    for i in message:
        unicodedata.normalize('NFKD', i).encode('ascii', 'ignore')
    if message['cmd'] == 'chat':
        if message['text'].lower() == '|ebear' or message['text'].lower() == '|eb':
            _thread.start_new_thread(run, ())
        if message['text'].lower() == '|ebear -s' or message['text'].lower() == '|eb -s':
            _thread.start_new_thread(run, ((1,)))
        elif message['text'].lower() == '|source':
            ws.send(json.dumps({"cmd": "chat", "text": ("%s") % comm['|source']}))
        elif message['text'].lower() == '|help' or message['text'].lower() == '|h':
            ws.send(json.dumps({"cmd": "chat", "text": ("%s") % comm['|help']}))
        elif message['text'].lower()[:3] == '|g ':
            if len(message['text']) > 3:
                ws.send(json.dumps({"cmd": "chat", "text": google.search(message['text'][3:])}))
            else:
                ws.send(json.dumps({"cmd": "chat", "text": "Usage is |g \"string\""}))
        elif message['text'].lower() == '|g':
            ws.send(json.dumps({"cmd": "chat", "text": "Usage is |g \"string\""}))
        elif message['text'].lower()[:4] == '|ed ':
            if len(message['text']) > 4:
                ws.send(json.dumps({"cmd": "chat", "text": ED.search(message['text'][4:])}))
            else:
                ws.send(json.dumps({"cmd": "chat", "text": "Usage is |ed \"string\""}))
        elif message['text'].lower() == '|ed':
            ws.send(json.dumps({"cmd": "chat", "text": "Usage is |ed \"string\""}))
        afk(message)

def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    ws.send(json.dumps({"cmd": "join", "channel": "room_name", "nick": comm['owname']}))
    _thread.start_new_thread(heartBeat, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://hack.chat/chat-ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
