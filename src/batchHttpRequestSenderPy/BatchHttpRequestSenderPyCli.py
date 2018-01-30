'''
batchHttpRequestSenderPy.appCli -- shortdesc

batchHttpRequestSenderPy.appCli is a description

It defines classes_and_methods

@author:     Maicon Fonseca Zanco

@copyright:  Copyleft 2018 Maicon Fonseca Zanco. No rights reserved.

@license:    UNLICENSE

@contact:    maiconfz@gmail.com
@deffield    updated: Updated
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from configparser import ConfigParser
import os
import sys

from batchHttpRequestSenderPy.AppConfig import AppConfig
from batchHttpRequestSenderPy.BatchHttpRequestSenderPy import BatchHttpRequestSenderPy
from pathlib import Path

__all__ = []
__version__ = 0.1
__date__ = '2018-01-28'
__updated__ = '2018-01-28'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = 'E: %s' % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v%s' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    program_license = '''%s

    Created by Maicon Fonseca Zanco on %s.
    Copyleft 2018 Maicon Fonseca Zanco. No rights reserved.

    This is free and unencumbered software released into the public domain.
    
    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.
    
    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.
    
    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
    
    For more information, please refer to <http://unlicense.org/>

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-v', '--verbose', dest='verbose', action='count', help='set verbosity level [default: %(default)s]')
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-configFilePath', dest='configFilePath', help='App configuration ini filePath. It must be a .ini pattern file', nargs='?', default='./app.ini')
        parser.add_argument('-defaultServiceUrl', dest='defaultServiceUrl', help='Default service url to send requests', nargs='?')
        parser.add_argument('-requestsCsvFilePath', dest='requestsCsvFilePath', help='Requests csv file path that contains the data, etc to be sent', nargs='?')
        parser.add_argument('-threadsNumber', dest='threadsNumber', help='How many threads the process will use', nargs='?')
        
        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 0:
            print('Verbose mode on')
        
        defaultServiceUrl = None
        requestsCsvFilePath = None
        threadsNumber = None
        
        if Path(args.configFilePath).is_file():
            config = ConfigParser()
            config.read(args.configFilePath)
            defaultServiceUrl = config.get('DEFAULT', 'defaultServiceUrl')
            requestsCsvFilePath = config.get('DEFAULT', 'requestsCsvFilePath')
            threadsNumber = config.getint('DEFAULT', 'threadsNumber')
        
        appConfig = AppConfig(defaultServiceUrl, requestsCsvFilePath, threadsNumber)
        app = BatchHttpRequestSenderPy(appConfig)
        app.run()
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help')
        return 2


if __name__ == '__main__':
    if DEBUG:
        #sys.argv.append('-h')
        sys.argv.append('-v')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'batchHttpRequestSenderPy.appCli_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'w+')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    exitCode = main()
    sys.exit(exitCode)
