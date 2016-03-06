# @author: Dylan Gorman, Haeffner lab

'''
### BEGIN NODE INFO
[info]
name = Newport
version = 1.2
description =
instancename = Newport
[startup]
cmdline = %PYTHON% %FILE%
timeout = 20
[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
'''

from labrad.server import LabradServer, setting, Signal
from twisted.internet import reactor
from twisted.internet.defer import DeferredLock, inlineCallbacks, returnValue, Deferred
from twisted.internet.threads import deferToThread
from controller import Controller

class NewportServer(LabradServer):

    name = 'NewportServer'

    def construct_command(self, axis, command, nn = None):
        if nn is None:
            return str(axis) + command
        else:
            return str(axis) + command + str(nn)

    @inlineCallbacks
    def initServer(self):
        self.controller = yield Controller( idProduct=0x4000, idVendor=0x104d )
        self.position_dict = dict.fromkeys( [1, 2, 3, 4], 0)
        self.setpoint = dict.fromkeys( [1, 2, 3, 4], 0)
        self.inCommunication = DeferredLock()


    @setting(0, 'Get Position', axis = 'i', returns = 'i')
    def get_position(self, c, axis):
        """
        Query the controller for the position of the given axis
        and also update position_dict
        """
        yield self.inCommunication.acquire()
        pos = yield self.controller.get_position(axis)
        self.inCommunication.relase()

        self.position_dict[axis] = pos
        returnValue(pos)

    @setting(1, 'Absolute Move', axis = 'i', pos = 'i')
    def absolute_move(self, c, axis, pos):
        """
        Move the given axis to a given absolute position
        """
        yield self.inCommunication.acquire()
        yield self.controller.absolute_move(axis, pos)
        self.inCommunication.release()

        self.position_dict[axis] = pos
    
    @setting(2, 'Relative Move', axis = 'i', steps = 'i')
    def relative_move(self, c, axis, steps):
        """
        Move the given axis the given number of steps
        """
        yield self.inCommunication.acquire()
        yield self.controller.relative_move(axis, steps)
        self.inCommunication.relase()

        self.position_dict[axis] += steps

    @setting(3, 'Mark current setpoint')
    def mark_setpoint(self, c):
        """
        Save the current position of all the axes
        to possibly return to later
        """
        
        axes = [1, 2, 3, 4]
        yield self.inCommunication.acquire()
        for axis in axes:
            pos = yield self.controller.get_position(axis)
            self.position_dict[axis] = pos
        self.inCommunication.release()
        
        self.setpoint = position_dict.copy()

    @setting(4, 'Return to setpoint')
    def return_to_setpoint(self, c):
        """
        Return all axes to the saved setpoint
        """
        axes = [1, 2, 3, 4]
        yield self.inCommunication.acquire()
        for axis in axes:
            yield self.controller.absolute_move( axis, self.setpoint[axis] )
            pos = self.setpoint[axis]
            self.position_dict[axis] = pos

    def notifyOtherListeners(self, context, message, f):
        notified = self.listeners.copy()
        notified.remove(context.ID)
        f(message.notified)

    def initContext(self, c):
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)
    
        

if __name__ == "__main__":
    from labrad import util
    util.runServer( NewportServer() )
