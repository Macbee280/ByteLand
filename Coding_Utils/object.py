""" object.py

    Using Object as a superclass will help produce cleaner, simpler code.

"""
import sys, os, re
import json
from time import sleep
import argparse
import types
import inspect
import torch

################################################################################
# OBJECTS

class Object(object):
    """
    A superclass to assist in the handling of options within code and result in cleaner code overall
    """
    def __init__(self, opt=None, default=None):
        """
        Instantiate the object and set options
        """
        self.set_options(opt, default)


    def __contains__(self, item):
        """
        Boolean: determine if 'item' is one of the keys sets
        """
        if item in self._value_:
            return True
        return False


    def _get_dict_of_(self, key, track_dict={}):
        """
        Get the value of a _dict_ item while guarding against recursion
        For use by __repr__
        """
        if key == '_value_':
            return track_dict
        if key in track_dict:
            return track_dict
        if in_recursion_loop(7):
            return track_dict
        val = self.__dict__.get(key)

        if isinstance(val, list)  or  isinstance(val, set):    # If 'val' is a list or set of things
            if len(val) > 9:
                track_dict[key] = "%d items"% len(val)
            else:
                out_list = []
                for x in val:
                    out_list.append(str(x))
                track_dict[key] = str(out_list)
        else:
            try:
                track_dict[key] = str(val)
            except:                                           # If 'val' can't be turned into a str, just get the type
                type_str = get_type(val)
                if len(type_str):
                    track_dict[key] = type_str

        return track_dict


    def _get_dict_(self, track={}):
        """
        Get the values of __dict__ while guarding against recursion
        (For use by __repr__)

        Modifies 'track' in place
        """
        for key in self.__dict__.keys():
            track.update(self._get_dict_of_(key, track))


    def _get_value_of_(self, key):
        """
        Get the value of a _value_ item while guarding against recursion
        For use by __repr__
        """
        track_value={}
        if in_recursion_loop(7):
            return track_value
        val = self._value_.get(key)

        if isinstance(val, list)  or  isinstance(val, set):    # If 'val' is a list or set of things
            if len(val) > 9:
                track_value[key] = "%d items"% len(val)
            else:
                out_list = []
                for x in val:
                    out_list.append(str(x))
                track_value[key] = str(out_list)
        else:
            try:
                track_value[key] = str(val)
            except:                                           # If 'val' can't be turned into a str, just get the type
                type_str = get_type(val)
                if len(type_str):
                    track_value[key] = type_str

        return track_value


    def _get_value_(self, track={}):
        """
        Get the values of _value_ while guarding against recursion
        (For use by __repr__)

        Modifies 'track' in place
        """
        for key in self._value_.keys():
            track.update(self._get_value_of_(key))


    def __repr__(self):
        """
        Make a string to represent this object
        """
        if hasattr(self, 'as_dict'):
            return str(self.as_dict())

        track = {'class':self.get_type()}
        self._get_dict_(track)    # Modifies 'track' in place
        self._get_value_(track)   # Modifies 'track' in place

        return json.dumps(track)


    def __str__(self):
        """
        Make a string to represent this object
        """
        if in_recursion_loop(7):
            return ''
        try:
            output = str(self.__repr__())
        except:
            output = str(self.get_type())
            raise

        return output


    def set(self, key, val):
        """
        Set key/val pair

        Parameters
        ----------
        key : str

        val : anything
        """
        self._value_[key] = val


    def update(self, data):
        """
        Store values in the _value_ dict

        Parameters
        ----------
        data : dict
        """
        for k, v in data.items():
            self.set(k, v)


    def set_values(self, data):
        """
        Store values in attributes (as opposed to the backoffice _value_ dict)

        Note:  Only sets non-null values

        Parameters
        ----------
        data : dict { "attribute_name" : "attribute_value" }
        """
        for k, v in data.items():
            if v is not None:
                setattr(self, k, v)


    def __setitem__(self, key, val):
        self._value_[key] = val


    def __delitem__(self, key):
        try:
            del self._value_[key]
        except:
            pass


    def get(self, key):
        """
        Get key/val pair

        Parameters
        ----------
        key : str

        Returns : anything
        """
        try:
            return self._value_[key]
        except KeyError:
            return None
        except:
            self._value_ = {}
            return None


    def __getitem__(self, key):
        return self.get(key)


    def ignore(self, key, val):
        """
        When setting options, ignore some situations

        Returns : boolean
        """
        if val is None:
            return True
        if re.search(r'^_', key):
            return True
        if key == 'opt':
            return True
        if isinstance(val, types.MethodType):
            return True

        return False


    def set_options(self, opt={}, default={}):
        """
        The purpose of this and related functions is to enable getting and setting of options without having to check first if a dict key exists-- results in cleaner code.

        Parameters
        ----------
        opt : dict, argparse.Namespace, Object
            The overriding options.  Each of these will definitely be set.
            Each key in this dict will be "set", i.e. stored in the _value  dict.  It can be retrieved using ".get()"

        default : dict
            The "defaults."  They will be set only if not already set
        """
        # Confirm that self._value_ exists
        try:
            if not hasattr(self, '_value_'):
                self._value_ = {}
        except AttributeError:
            self._value_ = {}
        except:
            self._value_ = {}

        # Set each of the 'options'
        if opt is None:
            pass

        elif isinstance(opt, dict):
            for key, val in opt.items():
                if self.ignore(key, val):
                    continue
                self.set(key, val)

        elif isinstance(opt, Options)  or  isinstance(opt, Object):
            for key, val in opt._value_.items():
                if self.ignore(key, val):
                    continue
                self.set(key, val)

        elif isinstance(opt, argparse.Namespace):
            for key in dir(opt):
                val = getattr(opt, key)
                if self.ignore(key, val):
                    continue
                # Some special handling
                if key == 'verbose_level':
                    key = 'verbose'
                self.set(key, val)

        else:
            frm       = inspect.stack()[1]
            mod       = inspect.getmodule(frm[0])
            mod_name  = mod.__name__
            curframe  = inspect.currentframe()
            calframe  = inspect.getouterframes(curframe, 2)
            func_name = mod_name +'.'+ str(calframe[1][3])
            sys.stderr.write('> CALLER: %s\n'% (func_name))
            sys.stderr.write('(coding_utils/object.py)  ERROR: opt object is of type:', type(opt))
            sys.stderr.write('\n')
            sys.stderr.flush()
            exit()

        # Next set the defaults if those keys have not already been set
        if default:
            self.set_missing_attributes(default)


    def set_missing_attributes(self, attributes={}):
        """
        Set options using a dict of defaults, assuming they haven't already been set

        Params
        ------
        attributes : dict {param:val}
            param : string
            val : anything
        """
        for param, val in attributes.items():
            if not self.get(param):
                self.set(param, val)


    def get_config(self, opt={}):
        """
        Generate a dict of the option settings -- only the simple ones

        Options
        -------
        serializable : boolean
            If True, only package up serializable elements

        Returns : dict
        """
        config = {}
        for param, val in self._value_.items():
            if isinstance(val, list) \
             or isinstance(val, set) \
             or isinstance(val, dict):
             pass

            elif isinstance(val, int) \
              or isinstance(val, float) \
              or isinstance(val, str) \
              or isinstance(val, int) \
              or isinstance(val, torch.dtype):

                if opt.get('serializable'):
                    if is_jsonable(val):
                        config[param] = val
                else:
                    config[param] = val
            
            elif not opt.get('serializable'):
                config[param] = val
            
        return config


    def done(self):
        """
        Used to make sure that a given function is only called once or a limited number of times.

        Usage:

            # To make sure that SomeObject.method1() only gets called twice:
            class SomeObject():
                ...
                def method1(self):
                    if self.done() < 2:
                        <do whatever>

        Returns
        -------
        int : the number of times 'caller' has been called for this object
        """
        caller = sys._getframe(1).f_code.co_name   # name of the function in which 'done()' was called
        tracker = '_DONE_' + caller                # name of stored key to track how many times 'caller' has been called for this object
        so_far = self.get(tracker)                 # number of times 'caller' has been called so far
        try:
            self.set(tracker, so_far + 1)          # increment the number of times
        except:
            self.set(tracker, 1)                   # first time

        return so_far


    def clear_done(self):
        """
        Used to enable a given function to be called again, resetting the variable being monitored in the function above

        Returns
        -------
        int : the number of times 'caller' has been called for this object
        """
        caller = sys._getframe(1).f_code.co_name   # name of the function in which 'done()' was called
        tracker = '_DONE_' + caller                # name of stored key to track how many times 'caller' has been called for this object
        self.set(tracker, 0)


    def get_type(self):
        """
        Returns a string with just the name of the instantiated class
        """
        T = str(type(self))
        T = re.sub(r"^<class '", "", T)
        T = re.sub(r"'>$", "", T)
        T = T.split('.')[-1]

        return T


######################
class Options(Object):
    """
    A subclass of Object to assist in the handling of options outside of object code
    """
    def __init__(self, opt, default=None):
        self.set_options(opt, default)
        

    def verbose(self):
        return self.get('verbose')


    def set_verbose(self, val=1):
        self.set('verbose', val)


    def silent(self):
        return self.get('silent')


    def set_silent(self):
        self.set('silent', True)


    def exit(self):
        return self.get('exit')


################################################################################
# FUNCTIONS

def get_type(obj):
    """
    Returns a string with just the name of the instantiated class
    """
    try:
        T = obj.get_type()
    except:
        T = str(type(obj))
        T = re.sub(r"^<class '", "", T)
        T = re.sub(r"^<'", "", T)
        T = re.sub(r"'>$", "", T)
        T = T.split('.')[-1]

    return T


def is_jsonable(x):
    """
    Determine if an object can be converted to json using the json module.

    """
    try:
        json.dumps(x)
        return True
    except:
        return False


def get_recursion_level(opt={}):
    """
    Get the current recursion level in the stack
    """
    frames = inspect.getouterframes(inspect.currentframe())
    return len(inspect.getouterframes(inspect.currentframe()))


def files_in_stack(opt={}):
    """
    Inspect the current stack and return a list of files involved
    """
    files = []
    frames = inspect.getouterframes(inspect.currentframe())
    for frame in frames:
        files.append(frame.filename)
    return files


def in_recursion_loop(depth=1, opt={}):
    """
    Boolean.  Determine if the current stack has a recursion loop
    """
    files = files_in_stack(opt=opt)
    seen = {}
    for f in files:
        if seen.get(f)  and  seen.get(f) >= depth:
            return True
        try:
            seen[f] += 1
        except:
            seen[f]  = 1

    return False


def get_loop_depth(opt={}):
    """
    Boolean.  Determine if the current stack has a recursion loop
    """
    maximum = 0
    files = files_in_stack(opt=opt)
    seen = {}
    for f in files:
        try:
            seen[f] += 1
        except:
            seen[f]  = 1
        maximum = max(maximum, seen[f])

    return maximum


################################################################################
################################################################################