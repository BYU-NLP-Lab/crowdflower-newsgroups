#!/usr/bin/python3.3
import os
from os import path
from subprocess import Popen
import subprocess 
from glob import glob
from multiprocessing import Pool

latex_template = '''
\\documentclass[12pt]{article}
\\usepackage[papersize={16in,24in}]{geometry}
\\pagenumbering{gobble}

\\begin{document}

\Large{

\\begin{verbatim}
%s
\\end{verbatim}

}

\\end{document}
'''

def sanitize(text):
    badchars = [
        chr(0x1b),
        chr(0x03),
        chr(0x7f),
        chr(0x10),
        chr(0x06),
        #chr(0x),
    ]
    for bad in badchars:
        text = text.replace(bad,'')
    return text

def call(args):
    p = Popen(args, stdout=subprocess.PIPE)
    p.communicate()

def write_image(args):
    #print "calling write_image with args ", args
    text,outpath = args

    # sanitize text (remove illegal characters)
    text = sanitize(text)

    outdir = path.dirname(outpath)
    outname = path.splitext(path.basename(outpath))[0]
    basepath = path.join(outdir,outname)
    latexpath = "%s.tex"%basepath
    pdfpath = "%s.pdf" % basepath
    pngpath = "%s.png" % basepath


    if len(glob("%s*.png"%pngpath[:-8]))>0:
        return
    else:
        print "converting text len %d to image %s" % (len(text),pngpath)

    # ensure output directory exists
    if not path.exists(outdir):
        os.makedirs(outdir)

    # produce tex
    latex = open(latexpath,'w')
    latex.write(latex_template % text)
    latex.close()

    # produce pdf
    print "producing pdf %s" % latexpath
    call(['xelatex',
        '--papersize','16in,24in',
        '--output-directory',outdir,
        latexpath])

    # crop pdf
    print "cropping pdf %s" % pdfpath
    call(['pdfcrop',pdfpath,pdfpath])

    # convert to png
    print "converting pdf to png %s" % pngpath
    call(['convert',pdfpath,pngpath])

    # delete intermediate files
    print "deleting intermediate files"
    delete_cmd = ['rm']
    delete_cmd.append(path.join(outdir,"%s.tex" % outname))
    delete_cmd.append(path.join(outdir,"%s.aux" % outname))
    delete_cmd.append(path.join(outdir,"%s.log" % outname))
    delete_cmd.append(path.join(outdir,"%s.pdf" % outname))
    call(delete_cmd)

def write_images_in_parallel(text_path_generator,num_processes=20):
    pool = Pool(processes=num_processes,maxtasksperchild=1)
    pool.map(write_image, text_path_generator)
    pool.close()

