'''
### BEGIN NODE INFO
[info]
name = Pulser_729
version = 1.0
description =
instancename = Pulser_729

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
'''
from labrad.server import LabradServer, setting
from twisted.internet.defer import Deferred, DeferredLock, inlineCallbacks
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from api import api
from labrad.types import Error

class Pulser_729(LabradServer):
    
    name = 'pulser_729'
    
    @inlineCallbacks    
    def initServer(self):
        self.api  = api()
        self.inCommunication = DeferredLock()
        yield self.initializeBoard()
        self.in_control = None
    
    @inlineCallbacks
    def initializeBoard(self):
        connected = self.api.connectOKBoard()
        while not connected:
            print 'not connected, waiting for 10 seconds to try again'
            yield self.wait(10.0)
            connected = self.api.connectOKBoard()
    
    @setting(0, 'Reset DDS', returns = '')
    def resetDDS(self , c):
        """
        Reset the ram position to 0
        """
        self.check_control(c)
        yield self.inCommunication.acquire()
        yield deferToThread(self.api.resetAllDDS)
        self.inCommunication.release()
        
    @setting(1, "Program DDS", program = '*(is)', returns = '')
    def programDDS(self, c, program):
        """
        Programs the DDS, the input is a tuple of channel numbers and buf objects for the channels
        """
        self.check_control(c)
        yield self.inCommunication.acquire()
        yield deferToThread(self._programDDSSequence, program)
        self.inCommunication.release()
    
    @setting(2, "Reinitialize DDS", returns = '')
    def reinitializeDDS(self, c):
        """
        Reprograms the DDS chip to its initial state
        """
        self.check_control(c)
        yield self.inCommunication.acquire()
        yield deferToThread(self.api.initializeDDS)
        self.inCommunication.release()
    
    @setting(3, "Control", shouldSet = 'b', returns = '(ww)')
    def getControl(self, c, shouldSet = False):
        if shouldSet:
            self.in_control = c.ID
        if self.in_control is None: return (0,0)
        return self.in_control
    
    def check_control(self, c):
        '''checks for which context controls the channel'''
        if self.in_control is None:
            self.in_control = c
        elif self.in_control != c:
            raise Error(code = 1, msg = 'Not in Control')
    
    def _programDDSSequence(self, program):
        '''takes the parsed dds sequence and programs the board with it'''
        for chan, buf in program:
            self.api.setDDSchannel(chan)
            self.api.programDDS(buf)
        self.api.resetAllDDS()
    
    def wait(self, seconds, result=None):
        """Returns a deferred that will be fired later"""
        d = Deferred()
        reactor.callLater(seconds, d.callback, result)
        return d
    
    def expireContext(self, c):
        if c.ID == self.in_control:
            self.in_control = None
        
if __name__ == "__main__":
    from labrad import util
    util.runServer( Pulser_729() )