#!/usr/bin/python3.3
import os
from os import path
from subprocess import call

latex_template = '''
\\documentclass[12pt]{article}
\\usepackage[papersize={8.5in,64in}]{geometry}
\\pagenumbering{gobble}

\\begin{document}

\\begin{verbatim}
%s
\\end{verbatim}

\\end{document}
'''

def write_image(text,outpath):
    outdir = path.dirname(outpath)
    outname = path.splitext(path.basename(outpath))[0]
    basepath = path.join(outdir,outname)

    # produce tex
    latexpath = "%s.tex"%basepath
    latex = open(latexpath,'w')
    latex.write(latex_template % text)
    latex.close()

    # produce pdf
    call(['xelatex',
        '--papersize','8.5in,64in',
        '--output-directory',outdir,
        latexpath])

    # crop pdf
    pdfpath = "%s.pdf" % basepath
    call(' '.join(['pdfcrop',pdfpath,pdfpath]),shell=True)

    # convert to png
    pngpath = "%s.png" % basepath
    call(['convert',pdfpath,pngpath])

