#!/usr/bin/env python

from sys import (path)
path.append('Dict')

from visual import (label, frame, vector, rate)
from select import (select)
from socket import (socket, AF_INET, SOCK_STREAM)
from ConfigParser import (ConfigParser)
from Dict import (Dict)

class Card(label):
    cardno = 1

    def __init__(self, dct):
        super(Card, self).__init__(**dct.__dict__)
        (self.g, self.dt, self.text) = (dct.g, dct.dt, dct.text)
        (self.velocity, self.card) = (dct.velocity, dct.card)
        (self.msg) = (dct.text)
        Card.cardno += 1
        (self.dy, self.bounce) = (0, 0)
        self.fmt = "card%d: %%s" % (self.card)
        self.report()

    def report(self):
        self.text = self.fmt % (self.msg)

    def __call__(self, text=""):
        self.msg = text if text else self.msg
        if self.visible:
            dxyz = self.velocity * self.dt
            (self.pos, self.dy) = (self.pos + dxyz, dxyz.y)
            if self.y <= self.radius:
                if (abs(self.dy) > 1e-2):
                    self.velocity.y = abs(self.velocity.y) * self.keep
                    self.bounce += 1
                else:
                    self.velocity.y = 0.0
                    self.y = self.radius
                self.report()
            else:
                self.velocity.y = self.velocity.y - self.g * self.dt

if __name__ == "__main__":
    configname = 'card3d.cfg'
    config = ConfigParser()
    config.read(configname)
    (cards, f) = ({}, frame())
    f.axis = (0,1,0)
    dct = Dict(
            g=9.8, dt=0.01, velocity=vector(0,-1,0),
            color=(1,1,1), background=(0.25,0.25,0.25), opacity=0.2,
            keep=1.0, frame=f,
            visible=True)
    for num, (key, val) in enumerate(config._sections.iteritems()):
        if not key.startswith('card'):
            continue
        dig = key[4:]
        if not dig.isdigit():
            continue
        dig = int(dig)
        line = val['text']
        (dct.pos, dct.card, dct.text) = ((num % 4, 4, num % 4), dig, line)
        dct.radius = 1
        cards[key] = Card(dct)

    (host, port, backlog, size) = ('', 50000, 5, 1024)
    s = socket(AF_INET, SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 

    def getmessage():
        msg = ""
        rcv, snd, exc = select([s,], [], [], 0)
        if rcv != []:
            client, address = s.accept() 
            msg = data = client.recv(size) 
            abc = list(msg.partition('/?'))
            if abc[1]:
                msg = abc[2]
            abc = list(msg.partition(' '))
            if abc[1]:
                msg = abc[0]
            if msg: 
                client.send(msg)
            client.close()
        return msg

    while 1:
        f.rotate(angle=0.01)
        msg = getmessage()
        cardno = None
        abc=list(msg.partition('_'))
        if abc[1]:
            cardno, _, msg = abc
            abc = list(msg.partition("\n"))
            if abc[1]:
                msg = abc[0]
        else:
            msg = ""
        rate (100)
        for name, card in cards.iteritems():
            text = ""
            if cardno and name == cardno:
                print '%s(%d): [%s]' % (cardno, len(cards), msg)
                text = msg
                config.set(cardno, 'text', text)
                with open(configname, 'w') as target:
                    config.write(target)
            card(text)
