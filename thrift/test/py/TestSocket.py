#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys, glob
sys.path.insert(0, './gen-py')
lib_path = glob.glob('../../lib/py/build/lib.*')
if lib_path:
  sys.path.insert(0, lib_path[0])

from ThriftTest import ThriftTest
from ThriftTest.ttypes import *
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
import unittest
import time
import socket
import random
from optparse import OptionParser

class TimeoutTest(unittest.TestCase):
    def setUp(self):
        for i in xrange(50):
            try:
                # find a port we can use
                self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.port = random.randint(10000, 30000)
                self.listen_sock.bind(('localhost', self.port))
                self.listen_sock.listen(5)
                break
            except:
                if i == 49:
                    raise

    def testConnectTimeout(self):
        starttime = time.time()

        try:
            leaky = []
            for i in xrange(100):
                socket = TSocket.TSocket('localhost', self.port)
                socket.setTimeout(10)
                socket.open()
                leaky.append(socket)
        except:
            self.assert_(time.time() - starttime < 5.0)

    def testWriteTimeout(self):
        starttime = time.time()

        try:
            socket = TSocket.TSocket('localhost', self.port)
            socket.setTimeout(10)
            socket.open()
            lsock = self.listen_sock.accept()
            while True:
                socket.write("hi" * 100)

        except:
            self.assert_(time.time() - starttime < 5.0)

def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TimeoutTest))
    return suite

if __name__ == "__main__":
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(suite())
