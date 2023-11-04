""" coding_utils.py

General tools to help write cleaner code.

"""
import sys, os
import random
import time
import re, json
import inspect
import argparse
import logging
import math
import numpy as np
import hashlib
import matplotlib.pyplot as plt
import operator as op
from functools import reduce
from object import Options

# Set format for Numpy printing
np.set_printoptions(precision=4, linewidth=255, threshold=10, edgeitems=15, suppress=True)

################################################################################
# FUNCTIONS

def gen_options(x, default={}):
    """
    Turn a dict into an Options object if necessary

    Parameters
    ----------
    x : dict or Options obj

    Returns
    -------
    Options obj
    """
    opt = Options(x)
    for k,v in default.items():
        if k not in opt:
            opt[k] = v   # Add each of the missing 'default' items
    
    return opt


def stderr(text=''):
    """
    Print a message to STDERR and flush

    Parameters
    ----------
    text : str
    """
    text = str(text)
    sys.stderr.write(text + '\n')
    sys.stderr.flush()
    

def err(vars=[], opt={}):
    """
    Function to help with debugging.  Easier and cleaner than writing comparable print statements.

    Usage:

        # Print the filename/line number to STDERR
        err()

        # Print the filename/line number to STDERR along with the values of a list of variables, each on a separate line
        err([var1, var2])

    Paramters
    ---------
    vars : list or str
        a list of values to be printed

    options : dict or Options object

    Options
    -------
    verbose : int
        Only prints if above zero

    exception : Exception
        Report on this exception and raise

    ValueError :
        Create a ValueError based on this string

    level (env var)
        Lowest value allows all errors and warnings to print
    """
    opt = gen_options(opt)   # Create 'Options' object if needed

    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                              # 1 represents line at caller
    frame = callerframerecord[0]
    info  = inspect.getframeinfo(frame)
    file  = os.path.basename(info.filename)
    line  = info.lineno

    # Parse exception
    exception = opt.get('exception')
    if not exception:
        if opt.get('ValueError'):
            exception = ValueError(opt.get('ValueError'))
    if not opt.silent():
        sys.stderr.write("\nDEBUG:  Line (%d)  file [%s]\n"% (line, info.filename))

        if exception:
            sys.stderr.write('\tEXC  |%s|\n' % str(exception))
        if isinstance(vars, str):
            sys.stderr.write('\tVAR  |%s| <str>\n' % vars)
        elif isinstance(vars, int):
            sys.stderr.write('\tVAR  |%d| <int>\n' % vars)
        elif isinstance(vars, float):
            sys.stderr.write('\tVAR  |%0.5f| <float>\n' % vars)
        elif isinstance(vars, list)  or  isinstance(vars, set)  or  isinstance(vars, tuple):
            for v in vars:
                sys.stderr.write('\tVAR  |%s|  %s\n'% (str(v), str(type(v))) )

    sys.stderr.flush()

    # Conditional return
    if opt.exit():
        exit(1)
    if exception:
        raise exception


def profile(vars=[], opt={}):
    """
    Function to help with debugging.  Easier and cleaner than writing comparable print statements.

    Usage:

        # Print the filename/line number to STDERR along with some stats
        err()

        # Print the filename/line number to STDERR along with some stats and the values of a list of variables, each on a separate line
        err([var1, var2])

    Paramters
    ---------
    vars : list or str
        a list of values to be printed

    options : dict or Options object

    Options
    -------
    verbose : int
        Only prints if above zero

    exception : Exception
        Report on this exception and raise

    ValueError :
        Create a ValueError based on this string

    level (env var)
        Lowest value allows all errors and warnings to print
    """
    opt = gen_options(opt)   # Create 'Options' object if needed

    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                              # 1 represents line at caller
    frame = callerframerecord[0]
    info  = inspect.getframeinfo(frame)
    file  = os.path.basename(info.filename)
    line  = info.lineno

    if not opt.silent():
        sys.stderr.write("\nDEBUG:  Line (%d)  file [%s]\n"% (line, info.filename))
        if isinstance(vars, str):
            sys.stderr.write('\tVAR  |%s| <str>\n' % vars)
        elif isinstance(vars, int):
            sys.stderr.write('\tVAR  |%d| <int>\n' % vars)
        elif isinstance(vars, float):
            sys.stderr.write('\tVAR  |%0.5f| <float>\n' % vars)
        elif isinstance(vars, list)  or  isinstance(vars, set):
            for v in vars:
                sys.stderr.write('\tVAR  |%s|  %s\n'% (str(v), str(type(v))) )

    # Handle time
    now = time.time()
    if os.environ.get('profile_start'):
        start = float(os.environ.get('profile_start'))
        last  = float(os.environ.get('profile_last'))
        stderr("\tLast step:  %0.5f"% (now - last))
        stderr("\tCumulative: %0.5f"% (now - start))
    else:
        stderr("\tInitiating profile ...")
        os.environ['profile_start'] = str(now)
    os.environ['profile_last'] = str(now)
                
    sys.stderr.flush()


def argparser(opt=None):
    """
    Set some standard options for CLI that should apply to various tools.  Should be called in the __main__ of a script.

    'args' is a Python Namespace object.  Its attributes must exist in order to be used by conditionals.
    """
    desc   = opt.get('desc')   # Description of the flag
    parser = argparse.ArgumentParser(description=desc)

    # Boolean flags
    parser.add_argument('--verbose',          help='Verbose Mode', required=False, action='store_true')
    parser.add_argument('--silent',           help='Silent Mode : Less or no output to STDERR / STDOUT', required=False, action='store_true')
    parser.add_argument('--no_pool',          help="Don't utilize Multiprocessing", required=False, action='store_true')
    parser.add_argument('--use_pool',         help="Utilize Multiprocessing", required=False, action='store_true')

    # Argument-taking flags (single-use)
    parser.add_argument('--bucket',           help='AWS S3 bucket', required=False, type=str)
    parser.add_argument('--host',             help='Hostname', required=False, type=str)
    parser.add_argument('--skip',             help='During iteration, skips past this percentage of the inputs', required=False, type=float)
    parser.add_argument('--verbose_level',    help='Verbose mode set to a specific level', required=False, type=int)

    # Argument-taking flags (multi-use)
    parser.add_argument('--dir',              help='A folder having files to be read', required=False, nargs='?', action='append')
    parser.add_argument('--file',             help='A file to be read', required=False, nargs='?', action='append')

    return parser


def argparser_ml(opt=None):
    """
    Like argparser (above), but specific to ML
    """
    parser = argparser(opt)

    # Boolean flags
    parser.add_argument('--by_accuracy',      help='Sort and select models by accuracy', required=False, action='store_true')
    parser.add_argument('--by_timestamp',     help='For clearing chaff only, keep latest models', required=False, action='store_true')
    parser.add_argument('--diversity_loss',   help='Include diversity loss', required=False, action='store_true')
    parser.add_argument('--gravity_loss',     help='Include gravity loss', required=False, action='store_true')
    parser.add_argument('--gaussian_noise',   help='Add Gaussian noise during training', required=False, action='store_true')
    parser.add_argument('--from_scratch',     help='In training a model, refresh model state to intial (every time)', required=False, action='store_true')
    parser.add_argument('--latest_model',     help="Load the 2nd latest model", required=False, action='store_true')
    parser.add_argument('--no_cuda',          help="Don't use CUDA", required=False, action='store_true')
    parser.add_argument('--partial_initialize', help='In training a model, refresh model state to intial, except for frozen layers', required=False, action='store_true')
    parser.add_argument('--poisson_beam_search', help='Beam search models choosing the best by a Poisson process', required=False, action='store_true')
    parser.add_argument('--refresh',          help='In training a model, refresh model state to intial (random)', required=False, action='store_true')
    parser.add_argument('--shuffle',          help='Shuffle the data before each epoch', required=False, action='store_true')
    parser.add_argument('--stacked',          help='Stacked version of the model (for RNNs)', required=False, action='store_true')
    parser.add_argument('--train',            help='Train a model on the data in the input file', required=False, action='store_true')
    parser.add_argument('--test',             help='Train a model on the data in the input file', required=False, action='store_true')

    # Argument-taking flags (single-use)
    parser.add_argument('--batch_size',       help='Size of data for each epoch', required=False, type=int)
    parser.add_argument('--criterion',        help='Specify the loss criterion to use, from [mse, cross_entropy]', required=False, type=str)
    parser.add_argument('--data_dir',         help='Directory where data is stored', required=False, type=str)
    parser.add_argument('--data_file',        help='File where data is stored', required=False, type=str)
    parser.add_argument('--dim',              help='Dimensionality of the vectors', required=False, type=int)
    parser.add_argument('--epoch',            help='Epochs to begin at for training', required=False, type=int)
    parser.add_argument('--epochs',           help='Number of total epochs for training', required=False, type=int)
    parser.add_argument('--initialization',   help='Specify an initialization (e.g. normal, eye, kaiming, uniform)', required=False, type=int)
    parser.add_argument('--learning_rate',    help='Learning rate for SGD', type=float, required=False)
    parser.add_argument('--model_dir',        help='Directory to save the model in', required=False, type=str)
    parser.add_argument('--model_file',       help='Load a specific model file', required=False, type=str)
    parser.add_argument('--optimizer',        help='Specify the optimizer to use, from [adam, rmsprop]', required=False, type=str)
    parser.add_argument('--steps',            help='Steps per training batch', required=False, type=int)
    parser.add_argument('--test_dir',         help='Directory where testing data is stored', required=False, type=str)
    parser.add_argument('--test_file',        help='Testing file path', required=False, type=str)
    parser.add_argument('--train_dir',        help='Directory where training data is stored', required=False, type=str)
    parser.add_argument('--train_file',       help='Training file path', required=False, type=str)
    parser.add_argument('--validation_dir',   help='Directory where validation data is stored', required=False, type=str)
    parser.add_argument('--validation_file',  help='Validation file path', required=False, type=str)

    # Argument-taking flags (multi-use)
    parser.add_argument('--show_parameter', help='Show these parameters in the model.', nargs='?', required=False, type=str, action='append')
    parser.add_argument('--show_tensor', help='Show tensors at these points as they propagate through the model.', nargs='?', required=False, type=str, action='append')
    
    return parser


def parse_args(parser, default={}):
    """
    Much like 'argparser.parse_args()', but also creates an Options object

    Parameters
    ----------
    parser : Arg parser object (can return a Namespace)
    default : dict (default value for variables not set by the parser)

    Returns
    -------
    args : Namespace
    opt : Options obj (only this will have values from 'default')
    """
    args = parser.parse_args()
    opt  = gen_options(args, default=default)
    return args, opt


def smaller_bytes(x):
    return x * 1024.


def bigger_bytes(x):
    return x / 1024.


def bytes_to_megabytes(x):
    x = bigger_bytes(x)
    x = bigger_bytes(x)
    return x


def bytes_to_gigabytes(x):
    x = bigger_bytes(x)
    x = bigger_bytes(x)
    x = bigger_bytes(x)
    return x


def gigabytes_to_bytes(x):
    x = smaller_bytes(x)
    x = smaller_bytes(x)
    x = smaller_bytes(x)
    return x


def batch_by_n(things, N):
    """
    Split 'things' into batches of size N

    Parameters
    ----------
    things : list
    N : int

    Yields
    ------
    list of N things
    """
    output = []
    for thing in things:
        output.append(thing)
        if len(output) >= N:
            yield output
            output = []
    if len(output):
        yield output


def is_null(x):
    """
    Determine if is 0 or None or NAN or ''
    """
    if x is None:
        return True

    elif isinstance(x, float):
        if np.isnan(x):
            return True
        elif x == 0.:
            return True

    elif isinstance(x, int):
        if x == 0.:
            return True

    elif isinstance(x, str):
        if x == '':
            return True

    return False


def is_number(x):
    """
    Determine if is one of [float, int]
    """
    if x is None:
        return False

    elif isinstance(x, float):
        if np.isnan(x):
            return False
        else:
            return True

    elif isinstance(x, int):
        return True
    
    return False


def is_method(thing):
    """
    Boolean : is 'thing' a method
    """
    if str(type(thing)) == "<class 'method'>":
        return True
    return False


def this_dir(fileobj):
    """
    Get the resolved full path to the folder containing the script that called this function
    """
    # return os.path.abspath( os.path.dirname(fileobj) )
    return os.path.dirname(os.path.realpath(fileobj))


def up_1_dir(fileobj):
    """
    Get the resolved full path to the folder *above* the one containing the script that called this function
    """
    # return os.path.abspath( os.path.join( os.path.dirname(fileobj), '..' ) )
    return os.path.abspath( os.path.join( os.path.dirname(os.path.realpath((fileobj))), '..' ) )


def nan_to_num(X):
    """
    For a given numpy array, will replace NaN's, inf, and -inf with zero

    Parameters
    ----------
    X : numpy array

    Returns
    -------
    X : numpy array
    """
    try:
        if isinstance(X[0], str):
            return X
        elif isinstance(X[0][0], str):
            return X
    except:
        pass
    X[X == np.inf] = 0
    X[X == -np.inf] = 0
    X[X == None] = 0
    X = np.nan_to_num(X)

    return X


def list_to_np_num(X):
    """
    Given a list of ints and/or floats, return a numpy ndarray without any NaNs
    """
    if not isinstance(X, np.ndarray):
        X = np.array(X)
    X = nan_to_num(X)
    return X


def nan_to_num_list(X):
    """
    For a given number or array, will replace NaN's, and None with 0

    Parameters
    ----------
    X : int, float, or list thereof

    Returns
    -------
    X : float or list of float
    """
    if isinstance(X, list):
        output = []
        for x in X:
            output.append(nan_to_num_list(x))
        return output
    elif isinstance(X, int):
        return X
    elif isinstance(X, float):
        return X
    elif X is None:
        return 0
    elif math.isnan(X):
        return 0
    else:
        return 0
            

def raise_error_on_nans(X):
    """
    For a given numpy array, will replace NaN's, inf, and -inf with zero

    Parameters
    ----------
    X : numpy array

    Returns
    -------
    boolean
    """
    try:
        np.all(np.isfinite(X))
    except:
        err()
        for x in X:
            if len(x.shape) > 0:
                for e in x:
                    err([x, e])
            else:
                err([X, x])
        raise


def prep_x_points(X, x_index=0):
    """
    Use just the specified element
    """
    x_points = []
    for x in X:
        if isinstance(x, float)  or  isinstance(x, int):
            x_points.append(x)
        else:
            x_points.append(x[x_index])   # Requires setting the right opt

    return x_points


def plot_data(Y, X, Y2=None, X2=None, opt={}):
    """
    Simple plot of data

    Parameters
    ----------
    data : list of (Y, X)
        Y : float
        X : float or list of float
    """
    fig, ax = plt.subplots()
    x_points = prep_x_points(X, opt.get('x_index'))   # Convert incoming data as needed

    ax.scatter(x_points, Y, s=10, c='b', marker="s", label='first')
    if Y2 is not None:
        if X2 is not None:
            x_points = prep_x_points(X2, opt.get('x_index'))   # Convert incoming data as needed
        ax.scatter(x_points, Y2, s=10, c='r', marker="o", label='second')

    # Set options, if any
    ax.set(xlabel=opt.get('xlabel'), ylabel=opt.get('ylabel'), title=opt.get('title'))
    if opt.get('legend'):
        try:
            plt.legend(loc=opt.get('legend'))
        except:
            plt.legend(loc='upper right')
    if opt.get('grid'):
        ax.grid()
    if opt.get('save_to_file'):
        fig.savefig(opt.get('save_to_file'))

    plt.show()


def print_tensor_info(T, desc=None):
    """
    Returns some info about a tensor or variable
    """
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                              # 1 represents line at caller
    frame = callerframerecord[0]
    info  = inspect.getframeinfo(frame)
    file  = os.path.basename(info.filename)
    line  = info.lineno
    grad_fn = T.grad_fn
    requires_grad = T.requires_grad

    try:
        size = str(T.size())
        typ  = str(type(T))
        Ttyp = str(T.type())
    except:
        size = "None"
        typ  = "None"
        Ttyp = "None"

    if desc is None:
        sys.stderr.write("\nINFO from file: %s"% file + " Line: %d"% line + "\n\tsize: %s"% size + "\n\ttype: %s\n"% typ)
    else:
        sys.stderr.write("\n%s (from file: %s)"% (desc, file) + " Line: %d"% line + "\n\tsize: %s"% size + "\n\ttype: %s\n"% typ)
    sys.stderr.write("\tType: %s\n"% Ttyp)
    try:
        sys.stderr.write("\tDType: %s\n"% str(T.data.type()))
    except:
        pass
    sys.stderr.write("\tGrad Fn: %s\n"% grad_fn)
    sys.stderr.write("\tRequires grad: %s\n"% requires_grad)
    print()


def json_loads(text):
    """
    Wrapper around json.loads.  Handles an error with the json package
    """
    try:
        output = json.loads(text)
        return output
    except:
        text = re.sub(r"([\[, ])\.(\d)", r"\1 0.\2", text)
        output = json.loads(text)
        return output


def chunk_range(size, chunk_num, N):
    """
    Split a range of 'size' things into 'N' subranges. Return offset, stopping point, and limit for the 'chunk_num'th chunk

    Makes it easy to avoid "one-off" errors.  Returns the exact values needed for 'range(start, stop)'

    Parameters
    ----------
    size : int      (size of some list of things)
    N : int         (number of desired chunks)
    chunk_num: int  (the number of the specified chunk)

    Returns
    -------
    start : int   (where to start iterating for this chunk)
    stop : int    (where to stop -- uses the python indexing convention, i.e. "5" means do up until 5)
    limit : int   (after doing this many, stop iterating)
    """
    chunk_size   = int( math.floor(size / N) )
    chunk_start = int(chunk_num * chunk_size)
    chunk_stop   = chunk_start + chunk_size
    chunk_stop   = min(chunk_stop, size)
    if chunk_num == N - 1:
        chunk_stop = size + 1    # Make sure the last chunk gets the last item
        chunk_size = chunk_stop - chunk_start
    if chunk_num > N - 1:
        err(["ERROR: no chunks after %d"% N-1])
        exit()

    return chunk_start, chunk_stop, chunk_size


def md5_hash(x):
    """
    Returns the MD5 hash of a string

    Parameters
    ----------
    x : str

    Returns
    -------
    str
    """
    x = x.encode("utf-8")
    hasher = hashlib.md5()
    hasher.update(x)
    return hasher.hexdigest()


def clean_spaces(line):
    """
    Remove extra spaces
    """
    line = re.sub('\s+', ' ', line)
    line = re.sub('^\s+', '', line)
    line = re.sub('\s+$', '', line)
    
    return line


def disable_logger(name, filepath="/dev/null"):
    """
    Disable the named logger.  After some new updates to various Python packages, this function
    became necessary
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.CRITICAL)
    logger.disabled = True
    f = open(filepath,"w")
    lh = logging.StreamHandler(f)
    logger.addHandler(lh)


def n_choose_k(n, k):
    """
    Will be deprecated after Python 3.8, with the introduction of math.comb
    See: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
    """
    n = int(n)
    k = int(k)
    k = min(k, n-k)
    numer = reduce(op.mul, range(n, n-k, -1), 1)
    denom = reduce(op.mul, range(1, k+1), 1)

    return int(numer / denom)


def input_boolean(prompt):
    """
    Print prompt, accept input, convert to boolean
    """
    response = input(prompt)
    sys.stdout.flush()
    sys.stderr.flush()
    if re.search('yes', response, flags=re.I):
        return True
    if re.search('true', response, flags=re.I):
        return True
    if response in ['y', 'Y', '1', ' ', '  ']:
        return True

    return False
    

def input_int(prompt):
    """
    Print prompt, accept input, convert to int
    """
    response = None
    while response is None:
        x = input(prompt)
        sys.stdout.flush()
        sys.stderr.flush()
        if x in ['quit', 'q', 'QUIT', 'Q']:
            response = 'QUIT'
        elif x == '':
            response = 0
        else:
            response = int(x)
        return response


def random_seed():
    """
    Set the random seed

    Future work:
    also set os.environ['PYTHONHASHSEED'] = some str
    """
    # random.seed(os.getpid() + datetime.now().second)
    random.seed(os.getpid() + time.time())
    

def get_OS():
    """
    Get the operating system
    """
    p = sys.platform
    if p in ['darwin', 'macos']:
        return 'macos'
    elif p in ['linux', 'linux2']:
        return 'linux'

    return 'unknown'
    

def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]

def clear_screen():
    """Clear the command-line interface screen."""
    if os.name == 'posix':  # Unix-based system (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':   # Windows
        os.system('cls')

################################################################################
################################################################################