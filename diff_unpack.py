#!/usr/bin/env python

from    pathlib                 import Path
from    argparse                import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from    importlib.metadata      import Distribution
from    typing                  import Iterator, Optional

from    chris_plugin            import chris_plugin, PathMapper
import  itertools

__pkg       = Distribution.from_name(__package__)
__version__ = __pkg.version

import  os
from    importlib.resources     import files
import  sys

import  pfmisc
from    pfmisc._colors          import Colors

import  pudb

from    init                    import start
from    job                     import jobber

DISPLAY_TITLE = r"""
       _           _ _  __  __                              _    
      | |         | (_)/ _|/ _|                            | |   
 _ __ | |______ __| |_| |_| |_ _   _ _ __  _ __   __ _  ___| | __
| '_ \| |______/ _` | |  _|  _| | | | '_ \| '_ \ / _` |/ __| |/ /
| |_) | |     | (_| | | | | | | |_| | | | | |_) | (_| | (__|   < 
| .__/|_|      \__,_|_|_| |_|  \__,_|_| |_| .__/ \__,_|\___|_|\_\
| |                       ______          | |                    
|_|                      |______|         |_|                    
"""


parser = ArgumentParser(description='A ChRIS DS plugin that is a thin wrapper about diff_unpack (part of TrackVis, original author Ruopeng Wang)',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

parser.add_argument(
        '--inputFilter', '-i',
        default     = '*dcm',
        help        = '''
        Input target filter of files to process. Default '*dcm'.
        '''
)
parser.add_argument(
        '--output_type', '-ot',
        default     = 'nii',
        help        = '''
        Output file type. accepted values are:
             analyze -> analyze format 7.5
             ni1     -> nifti format saved in seperate .hdr and .img file
             nii     -> nifti format with one .nii file
             nii.gz  -> nifti format with compression
        '''
)
parser.add_argument(
        '--split',
        default     = False,
        help        = '''
        Instead of saving everything in one big multi-timepoint 4D image,
        split it into separate files, one timepoint per file
                        '''
)
parser.add_argument(
        '--paddings',
        default     = "3",
        help        = '''
        Number of 0 paddings for output filename prefix when '-split' enabled.
                        '''
)
parser.add_argument(
        '--start_number',
        default     = "1",
        help        = '''
        Start number of the output filename numbering. default is 1, meaning
        the first filename in the series is prefix001.suffix
        NOTE: '-p' and '-sn' options are only effective when '-split' is
        on, meaning output as a series of 3D image files instead of one 4D
        file
                        '''
)
parser.add_argument(
                        '-v', '--verbosity',
                        default = '0',
                        help    = 'verbosity level of app'
)

def inputDir2File_do(options : Namespace, t: tuple[Path, Path]) -> Optional[tuple[Path, Path]]:
    """This method transforms an (inputdir, outputdir) Path Tuple
    to an (inputfile, outputdir) spec. This is useful for the case where
    processing is on a per-directory level, but only one file in each
    inputdir is processed for analysis (a common pattern with especially
    DICOM data).

    Args:
        t (tuple[Path, Path]): The (inputdir, outputdir) Path Tuple

    Returns:
        Optional[tuple[Path, Path]]: An (inputfile, outputdir) Tuple
    """
    inputdir    : Path      = None
    outputdir   : Path      = None
    inputdir, outputdir     = t
    glob                    = inputdir.glob(options.inputFilter)
    inputFile   : Path      = next(glob, None)
    if inputFile is None:
        return None
    return inputFile, outputdir

def inputFileFilter_do(options : Namespace, mapper: PathMapper) -> Iterator[tuple[Path, Path]]:
    """Entry point to convert the input pathmapper to a file/dir mapper

    Args:
        options (_type_): CLI options
        mapper (PathMapper): A directory mapper

    Returns:
        _type_: a mapper with one inputfilename in lieu of the inputdir and the
                original outputdir.

    Yields:
        Iterator[tuple[Path, Path]]: the posix mapper
    """
    # globs   = ((i.glob("*dcm"), o) for i, o in mapper)
    # firsts  = ((next(g, None), o) for g, o in globs)
    # return filter(lambda t: t[0] is not None, firsts)
    return filter(
        lambda t: t is not None,
        map(inputDir2File_do, itertools.repeat(options), mapper)
    )

def diff_unpack(options: Namespace, inputfile: Path, outputdir: Path) -> dict:
    """Main entry point the diff_pack wrapper. The logic is trivial, for each
    inputfile/outputfile combination, wrap around a shell job of `diff_unpack`.

        options (Namespace): The option space, needed to determine report types.
        inputfile (Path): The input file path to process
        outputdir (Path): The corresponding outputdir path
    """
    start.LOG(f"Processing {inputfile} -> {outputdir}")
    shell           = jobber.Jobber({
                        'verbosity':    1,
                        'noJobLogging': True
                        })
    l_cliArgs       : list  = [
        '--output_type',    options.output_type,
        '--start_number',   options.start_number,
        '--paddings',       options.paddings
    ]
    if options.split: l_cliArgs.append('--split')
    # targetInput     : Path  = next(inputdir.glob(options.inputFilter))
    str_cliArgs     : str   = ' '.join(l_cliArgs)
    str_cliArgs             = '/usr/local/src/pl-diff_unpack/dtk/diff_unpack ' + str_cliArgs
    str_cliArgs            += ' ' + str(inputfile) + ' ' + str(outputdir)

    return shell.job_run(str_cliArgs)


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser              = parser,
    title               = 'diff_unpack',
    category            = '',               # ref. https://chrisstore.co/plugins
    min_memory_limit    = '8Gi',            # supported units: Mi, Gi
    min_cpu_limit       = '1000m',          # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit       = 0                 # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    global cloptions
    cloptions = options
    print(DISPLAY_TITLE, file=sys.stderr)
    ld_result   : list  = []
    if start.init(options, inputdir, outputdir)['isOK']:
        dir_mapper  = PathMapper.dir_mapper_deep(inputdir, outputdir)
        file_mapper = inputFileFilter_do(options, dir_mapper)
        for inputfile, outputdir in file_mapper:
            ld_result.append(diff_unpack(options, inputfile, outputdir))


if __name__ == '__main__':
    main()
