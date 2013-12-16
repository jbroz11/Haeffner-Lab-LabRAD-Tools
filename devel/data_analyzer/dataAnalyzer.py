'''
Dylan Gorman

Server for on-the-fly data analysis

The general flow should work like this:

1. Store a dataset into the databault with the parameter fit_type. fit_type can be either a
built in type such as RabiFlop, FrequencyScan, etc, or a custom type, e.g.
cct.scripts.custom_datasets.my_custom_dataset

2. load_data will import this module, so fit_type needs to refer to a module that
python can import. The module will contain a class named Fittable, which will contain the fitting routines
for this data type, some kind of automated initial value guessing, etc.

3. load_data returns a key (really an md5 hash of the datavault dir) by which the dataset can
be referred to outside the dataset.

4. populate parameters with add_parameter(). do add_parameter(key, 'param', 'auto') to autofit
Otherwise, do add_parameter(key, 'param', 'initial_guess'). the initial guess must be a string
here.

5. Once load_data() is called and the parameters are populated we can then call a fitting function

6. The fit function should optionally display the data together with the fit and allow
the user to accept or reject the fit. Reject -> either fit with custom params or do no fit at all.

'''

from labrad.server import setting, LabradServer, Signal
from labrad.units import WithUnit
from twisted.internet.defer import returnValue, inlineCallbacks
import importlib
import md5

class dataAnalyzer(LabradServer):

    """ Handles on-the-fly data analysis """

    name = 'Data Analyzer'

    @inlineCallbacks
    def initserver(self):

        self.dv = yield self.client.data_vault

        self.loaded_datasets = {}

    @setting(1, 'Load Data', data='*s', returns = '*s')
    def load_data(self, c, data):
        ''' takes a dataset from datavault, and returns a key identifying the dataset '''
        dir, dataset = data

        yield self.dv.cd(dir, context = context)
        yield self.dv.open(data, context = context)

        # first see if there's a fit type specified in the datavault
        
        raw = yield self.dv.get(context=context)
        fit_type = yield self.dv.get_parameter('fit_type', context=context)

        data_type = importlib.import_module(fit_type)

        workspace = data_type.Fittable(raw)

        key = md5.new()
        key.update(dir+dataset)

        self.loaded_datasets[key.digest()] = workspace
        
        return key.digest()

    @setting(2, 'Set Parmeter', key = '*s', param = '*s', initial_guess = '*s', to_fit = 'b', returns = '')
    def set_parameter(self, c, key, param, initial_guess, to_fit):
        ''' set a parameter with an initial guess.
        pass the initial_guess as a string so that you can also pass 'auto' to autofit.
        '''
        workspace = self.loaded_datasets[key]

        if initial_guess == 'auto':
            workspace.parameterDict[param] = ('auto', to_fit)
        else:
            workspace.parameterDict[param] = (float(intial_guess), to_fit)

    @setting(3, 'Fit', key='*s', returns = '')
    def fit(self, c, key):
        ''' fit a loaded dataset '''

        workspace = self.loaded_datasets[key]
        workspace.fit()

    @setting(4, 'Get Parameter', key = '*s', param = '*s', returns = 'v')
    def get_parameter(self, c, key, param):

        ''' get a parameter that's already fitted.
        At some point add a check that the fit has
        actually occurred
        '''
        workspace = self.loaded_datasets[key]
        result = workspace.result
        
        return result.params[param].value
    
    @setting(5, 'Get ChiSq', key = '*s', returns = 'v')
    def get_chisq(self, c, key):
        '''
        Get the chi-squared value for the fit returned by lmfit
        '''

        workspace = self.loaded_datasets[key]
        result = workspace.result
        
        return result.chisq

    @setting(6, 'Get Error', key = '*s', param = '*s', returns = 'v')
    def get_error(self, c, key, param):
        '''
        Get the error on a fit parameter
        '''

        workspace = self.loaded_datasets[key]
        result = workspace.result
        
        return result.params[param].stderr

    @setting(7, 'Accept Fit', key = '*s', returns = '')
    def accept_fit(self, c, key):
        '''
        Accept the results of a fit. Add to datavault
        and send a fit accepted signal
        '''
        workspace = self.loaded_datasets[key]
        workspace.fitAccepted = True
