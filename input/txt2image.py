#!/usr/bin/python3.3
import os
from os import path
from subprocess import call
from glob import glob
from multiprocessing import Pool

latex_template = '''
\\documentclass[12pt]{article}
\\usepackage[papersize={11in,24in}]{geometry}
\\pagenumbering{gobble}

\\begin{document}

\Large{

\\begin{verbatim}
%s
\\end{verbatim}

}

\\end{document}
'''

def write_image(args):
    print "calling write_image with args ", args
    text,outpath = args
    print "saving text len %d to %s" % (len(text),outpath)
    outdir = path.dirname(outpath)
    outname = path.splitext(path.basename(outpath))[0]
    basepath = path.join(outdir,outname)

    # ensure output directory exists
    if not path.exists(outdir):
        os.makedirs(outdir)

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

    # delete intermediate files
    delete_cmd = ['rm']
    delete_cmd.append(path.join(outdir,"%s.tex" % outname))
    delete_cmd.append(path.join(outdir,"%s.aux" % outname))
    delete_cmd.append(path.join(outdir,"%s.log" % outname))
    delete_cmd.append(path.join(outdir,"%s.pdf" % outname))
    print "delete command ",delete_cmd
    call(delete_cmd)

def write_images_in_parallel(text_path_generator,num_processes=8):
    pool = Pool(processes=num_processes)
    pool.map(write_image, text_path_generator)

