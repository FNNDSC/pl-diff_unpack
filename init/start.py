str_about = '''
    Simply module to provide some startup initializations.
'''

import  sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


from    pathlib                 import Path
from    argparse                import Namespace

import  pfmisc
from    pfmisc._colors          import Colors

from    chris_plugin            import chris_plugin, PathMapper

import  pudb

def init(options: Namespace, inputdir: Path, outputdir: Path) -> dict:
    """Perform some initializations, most notably verify/check on the
    FreeSurfer lookup table file.

    Args:
        options (Namespace): CLI namespace
        inputdir (Path): the plugin inputdir
        outputdir (Path): the plugin outputdir

    Returns:
        dictionary: initialization status and lookup table file location.
    """

    global PFMlogger, LOG

    d_ret               = {
        'isOK':             True,
    }
    PFMlogger           = pfmisc.debug(
                                            verbosity   = int(options.verbosity),
                                            within      = 'main',
                                            syslog      = True
                                        )
    LOG                 = PFMlogger.qprint
    LOG("initializing...")
    for k,v in options.__dict__.items():
         LOG("%25s:  [%s]" % (k, v))
    LOG("")
    return d_ret
