#!/usr/bin/env python

from sys import (path)
path.append('Dict')

from visual import (scene, frame, rate, label, vector, exit)
from select import (select)
from socket import (socket, AF_INET, SOCK_STREAM)
from ConfigParser import (ConfigParser)
from Dict import (Dict)

class Card(label):
    cardno = 1
    constant = Dict(g=9.8, dt=0.01)

    def __init__(self, dct):
        super(Card, self).__init__(**dct.__dict__)
        (self.force, self.text) = (vector(0.0,0.0,0.0), dct.text)
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
            dxyz = self.velocity * Card.constant.dt
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
                self.velocity.y = (
                        self.velocity.y - Card.constant.g * Card.constant.dt)

def getCards(f, configname = 'card3d.cfg'):
    config = ConfigParser()
    config.read(configname)
    cards = {}
    dct = Dict(
            velocity=vector(0,-1,0),
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
    return cards

def getmessage(cards, s):
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

        buf = '<html><body><h1>%s</h1><dl>' % (str(address))
        for name, card in cards.iteritems():
            buf += '<dt>%s</dt><dd>%s</dd>' % (name, card.text)
        buf += '</dl></body></html>'
        client.send(buf)
        client.close()
    return msg

def main(cards, f, s):
    while True:
        msg = getmessage(cards, s)
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

if __name__ == "__main__":

    # Initialize the web interface.
    (host, port, backlog, size) = ('', 50000, 5, 1024)
    s = socket(AF_INET, SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 

    # Initialize the visual python scene.
    scene.exit = True
    scene.title = 'card3d: prototype'
    f = frame()

    # Initialize the card contents from the configuration file.
    cards = getCards(f, 'card3d.cfg')

    # Define the spinning functions
    def spinLeft(f):
        f.axis = (1, 0, 0)
        f.rotate(angle=0.1)

    def spinRight(f):
        f.axis = (1, 0, 0)
        f.rotate(angle=0.1)

    def spinForward(f):
        f.axis = (0, 1, 0)
        f.rotate(angle=0.1)

    def spinBackward(f):
        f.axis = (0, 1, 0)
        f.rotate(angle=0.1)

    def spinUp(f):
        f.axis = (0, 0, 1)
        f.rotate(angle=0.1)

    def spinDown(f):
        f.axis = (0, 0, 1)
        f.rotate(angle=0.1)

    # Prepare a dictionary for keyboard function binding.
    spin = Dict(
        h=spinLeft, a=spinLeft,
        l=spinRight, f=spinRight,
        j=spinDown, s=spinDown,
        d=spinUp, k=spinUp,
        y=spinForward, t=spinForward,
        b=spinBackward, v=spinBackward
    )

    # Define keyboard event function.
    def keyInput(evt):
        k = evt.key
        if len(k) == 1:
            if k in spin.__dict__.keys():
                spin.__dict__[k](f)
            elif k == 'q' or k == 'Q':
                exit()
        elif ((k == 'backspace') or (k == 'delete')):
            pass

    # Bind keyboard events to the function.
    scene.bind('keydown', keyInput)

    # Run the card3d main loop.
    main(cards, f, s)
