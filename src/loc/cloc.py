# -*- coding: utf-8 -*-
'''
Created on 11/05/2011

@author: felipe
'''
import os
import sys
import getopt

SCRIPTS_DIR = '/home/felipe/workspace-msc/pl_stats/scripts'
CLOC_DIR = SCRIPTS_DIR + '/cloc-1.53.pl'

class CLoC(object):
    '''
    Class for handle CLoC program use
    '''
    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        
    def generateProjectData(self):
        '''
        Generate CLoC project data
        '''
        os.system('%s %s --exclude-dir=_pl-stats --csv --out=%s/_pl-stats/results/cloc.csv' % (os.path.abspath(CLOC_DIR), self.dir, self.dir))

    def generateWorkspaceData(self):
        '''
        Generate CLoC workspace of projects data
        '''
        for project in os.listdir(self.dir):
            abs_dir = os.path.abspath(os.path.join(self.dir, project))
            print '======================================================'
            print 'Project: %s' % (abs_dir)
            os.system('%s %s --exclude-dir=_pl-stats --csv --out=%s/_pl-stats/results/cloc.csv' % (os.path.abspath(CLOC_DIR), abs_dir, abs_dir))



def usage():
    '''
    Help!
    '''
    print ''
    print 'Usage: python cloc.py [OPTIONS] [PROJECT|WORKSPACE]'
    print 'Generates CLoC statistics about the PROJECT|WORKSPACE.'
    print ''
    print 'Options:'
    print '    -h, --help                   print this help'
    print '    -p, --project=PROJECT        generate CLoC statistics about the PROJECT.'
    print '    -w, --workspace=WORKSPACE    generate CLoC statistics about the projects in WORKSPACE.'
    print ''

def main():
    try:
        opts, extra_params = getopt.getopt(sys.argv[1:], "hp:w:", ["help", "project=", "workspace="])
    except getopt.GetoptError:          
        usage()
        sys.exit(2)
    
    dir = None
    flag = None
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()
        elif opt in ['-p', '--project']:
            flag = 'p'
            dir = arg
        elif opt in ['-w', '--workspace']:
            flag = 'w'
            dir = arg
        else:
            usage()
            sys.exit()

    cloc = CLoC(dir)
    if flag == 'p':
        cloc.generateProjectData()
    else:
        cloc.generateWorkspaceData()

if __name__ == '__main__': main()
