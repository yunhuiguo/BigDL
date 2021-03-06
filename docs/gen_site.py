#!/usr/bin/env python

import argparse
import sys
import os
from subprocess import Popen, PIPE
import subprocess


def run_cmd(cmds, err_msg, s=False):
    cmd = cmds
    if s:
        cmd = ' '.join(cmds) 
    try:
        # print cmd
        p = Popen(cmd, shell=s)
        p.communicate()
        if p.returncode != 0:
            print err_msg
            sys.exit()
    except OSError as e:
        print err_msg
        print e.strerror
        sys.exit()

parser = argparse.ArgumentParser(description='Process BigDL docs.')
parser.add_argument('-s', '--scaladocs',
    dest='scaladocsflag', action='store_true', 
    help='Add scala doc to site')
parser.add_argument('-p', '--pythondocs',
    dest='pythondocsflag', action='store_true',
    help='Add python doc to site')
parser.add_argument('-m', '--startmkdocserve',
    dest='mkdocserveflag', action='store_true',
    help=argparse.SUPPRESS)

args = parser.parse_args()

scaladocs = args.scaladocsflag

pythondocs = args.pythondocsflag

mkdoc_serve = args.mkdocserveflag


script_path = os.path.realpath(__file__)
dir_name = os.path.dirname(script_path)
os.chdir(dir_name)
run_cmd(['rm', '-rf', '{}/readthedocs'.format(dir_name)],
    'rm readthedocs error')

# check if mkdoc is installed
run_cmd(['mkdocs', '--version'], 
    'Please install mkdocs and run this script again\n\te.g., pip install mkdocs')

# git clone docs
run_cmd(['rm', '-rf', '/tmp/bigdl-doc'],
    'rm readthedocs error')

run_cmd(['git', 'clone', 'https://github.com/helenlly/bigdl-project.github.io.git', '/tmp/bigdl-doc'],
    'git clone readthedocs error')

run_cmd(['mv', '/tmp/bigdl-doc/readthedocs', dir_name],
    'mv readthedocs error')

run_cmd(['rm', '-rf', '/tmp/bigdl-doc'],
    'rm readthedocs error')

# mkdocs build
run_cmd(['mkdocs', 'build'], 
    'mkdocs build error')

if scaladocs:
    print 'build scala doc'
    bigdl_dir = os.path.dirname(dir_name)
    os.chdir(bigdl_dir)
    run_cmd(['mvn', 'scala:doc'], 'Build scala doc error')
    scaladocs_dir = bigdl_dir + '/spark/dl/target/site/scaladocs/*'
    target_dir = dir_name + '/site/APIdocs/scaladoc/'
    run_cmd(['cp', '-r', scaladocs_dir, target_dir],
        'mv scaladocs error', s=True)

if pythondocs:
    print 'build python'
    pyspark_dir = os.path.dirname(dir_name) + '/pyspark/docs/'
    target_dir = dir_name + '/site/APIdocs/python-api-doc/'
    os.chdir(pyspark_dir)
    run_cmd(['./doc-gen.sh'], 'Build python doc error')
    pythondocs_dir = pyspark_dir + '_build/html/*'
    run_cmd(['cp', '-r', pythondocs_dir, target_dir],
        'mv scaladocs error', s=True)

os.chdir(dir_name)

if mkdoc_serve:
    print 'start mkdoc server'
    run_cmd(['mkdocs', 'serve'], 
        'mkdocs start serve error')
   
