#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 missingdays <missingdays@missingdays>
#
# Distributed under terms of the MIT license.

"""
Main file for evol-server
"""

from twisted.internet import reactor, protocol

class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self, data):
        print "Number of active connections: ", self.factory.numConnections
        print "Got %s, sending %s" % (data, self.getQuote())
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote

class QuoteFactory(protocol.ClientFactory):
    numConnections = 0

    def buildProtocol(self, addr):
        return QuoteProtocol(self)

    def __init__(self, quote=None):
        self.quote = quote or "Zero"


reactor.listenTCP(8000, QuoteFactory())
reactor.run()

