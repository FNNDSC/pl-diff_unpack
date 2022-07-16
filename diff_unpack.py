#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


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
parser.add_argument('-e', '--example', default='foo',
                    help='argument which does not do anything')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='diff_unpack',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)
    print(f'Option: {options.example}')

    output_file = outputdir / 'success.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()
