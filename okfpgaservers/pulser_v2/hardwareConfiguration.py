class channelConfiguration(object):
    """
    Stores complete configuration for each of the channels
    """
    def __init__(self, channelNumber, ismanual, manualstate,  manualinversion, autoinversion):
        self.channelnumber = channelNumber
        self.ismanual = ismanual
        self.manualstate = manualstate
        self.manualinv = manualinversion
        self.autoinv = autoinversion
        
class ddsConfiguration(object):
    """
    Stores complete configuration of each DDS board
    """
    def __init__(self, address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
        self.channelnumber = address
        self.allowedfreqrange = allowedfreqrange
        self.allowedamplrange = allowedamplrange
        self.frequency = frequency
        self.amplitude = amplitude
        self.state = True
        self.boardfreqrange = args.get('boardfreqrange', (0.0, 800.0))
        self.boardamplrange = args.get('boardamplrange', (-63.0, -3.0))
        self.boardphaserange = args.get('boardphaserange', (0.0, 360.0))
        self.off_parameters = args.get('off_parameters', (0.0, -63.0))
        self.remote = args.get('remote', False)        

class remoteChannel(object):
    def __init__(self, ip, server, reset, program):
        self.ip = ip
        self.server = server
        self.reset = reset
        self.program = program
        
class hardwareConfiguration(object):
    channelTotal = 32
    timeResolution = 40.0e-9 #seconds
    timeResolvedResolution = timeResolution/4.0
    maxSwitches = 1022
    devicePollingPeriod = 10
    isProgrammed = False
    sequenceType = None #none for not programmed, can be 'one' or 'infinite'
    collectionMode = 'Normal' #default PMT mode
    collectionTime = {'Normal':0.100,'Differential':0.100} #default counting rates
    collectionTimeRange = (0.010, 5.0) #range for normal pmt counting
    sequenceTimeRange = (0.0, 85.0) #range for duration of pulse sequence
    sequenceType = None #none for not programmed, can be 'one' or 'infinite'
    okDeviceID = 'Pulser729'
    okDeviceFile = 'cctphoton.bit'
    secondPMT = False
    DAC = True
    resetstepDuration = 2
    
    #name: (channelNumber, ismanual, manualstate,  manualinversion, autoinversion)
    channelDict = {
#                  'bluePI':channelConfiguration(1, False, True, False, False),
                  ''''0':channelConfiguration(0, False, False, False, True),
                  '1':channelConfiguration(1, False, False, False, True),
                  '2':channelConfiguration(2, False, False, False, False),
                  '3':channelConfiguration(3, False, False, False, False),
                  '4':channelConfiguration(4, False, False, False, False),
                  '5':channelConfiguration(5, False, False, False, False),
                  '6':channelConfiguration(6, False, False, False, False),
                  '7':channelConfiguration(7, False, False, False, False),
                  '8':channelConfiguration(8, False, False, False, False),
                  '9':channelConfiguration(9, False, False, False, False),
                  '10':channelConfiguration(10, False, False, False, False),
                  '12':channelConfiguration(12, False, False, False, False),
                  '14':channelConfiguration(14, False, False, False, False),'''
                  #------------INTERNAL CHANNELS----------------------------------------#
                  'DiffCountTrigger':channelConfiguration(16, False, False, False, False),
                  'TimeResolvedCount':channelConfiguration(17, False, False, False, False),
                  'AdvanceDDS':channelConfiguration(18, False, False, False, False),
                  'ResetDDS':channelConfiguration(19, False, False, False, False),
                  'ReadoutCount':channelConfiguration(20, False, False, False, False),
                  }
    
    ddsDict = {
               '397DP':ddsConfiguration(0, (150.0,250.0), (-63.0,-3.0), 220.0, -10.0,
                                        #boardfreqrange = (170.0,270.0),
                                        #off_parameters = (220.0, -63.0),
                                        #boardphaserange = (0.0, 360.0)
                                         ),
                '866DP':ddsConfiguration(6, (70.0,90.0), (-63.0,-3.0), 80.0, -10.0,
                                        #boardfreqrange = (170.0,270.0),
                                        #ff_parameters = (220.0, -63.0),
                                        #boardphaserange = (0.0, 360.0)
                                         ),
                '854DP':ddsConfiguration(4, (70.0,90.0), (-63.0,-3.0), 80.0, -10.0,),
                '397DP Heating':ddsConfiguration(2, (150.0,250.0), (-63.0,-3.0), 220.0, -63.0,),
                #remote channels
                '729DP':ddsConfiguration(0, (150.0,250.0),  (-63.0,-3.0), 220.0, -33.0, remote = 'pulser_729')
#'1':ddsConfiguration(1, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#'2':ddsConfiguration(2, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'3':ddsConfiguration(3, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'4':ddsConfiguration(4, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#'5':ddsConfiguration(5, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'6':ddsConfiguration(6, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'7':ddsConfiguration(7, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#               '397':ddsConfiguration(2, (170.0,270.0), (190.0,250.0), (-63.0,-3.0), (-63.0,-3.0), 220.0, -33.0),               
               #'729DP':ddsConfiguration(0, (190.0,250.0), (-63.0,-3.0), 220.0, -33.0, remote = 'pulser_729')
               }

    remoteChannels = { 'pulser_729': remoteChannel('192.168.169.49', 'pulser_729', 'reset_dds','program_dds')}
