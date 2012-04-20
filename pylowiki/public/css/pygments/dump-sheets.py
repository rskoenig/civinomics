from pygments.styles import get_all_styles

import subprocess

def dump( scheme ):
    return subprocess.call( 'pygmentize -S ' + scheme + ' -f html > ' + scheme + '.css', shell=True )

for scheme in get_all_styles():
     dump( scheme )
