# -*- coding: utf-8 -*-
'''
Created on 18/06/2010

@author: felipe
'''
from setup import Setup
import sys
import getopt
import os

def usage():
    '''
    Help!
    '''
    print ''
    print 'Usage: python pl-stats.py [OPTIONS] [PROJECT]'
    print 'Generates Antenna directives statistics about the PROJECT.'
    print ''
    print 'Options:'
    print '    -h, --help             print this help'
    print '    -g, --generate         generate statistics. Whithout this flag, is there statistics data in project directory, they will be kept.'
    print '    -l, --language=LANG    set the project language as LANG. Actually supports C and Java languages.'
    print '    -e, --export           export statistics to different formats. Actually supports CSV and XML formats.'
    print ''



def generate_statistical_data(language, dir):
    '''
    '''
    print ''
    print dir
    print ''
    print 'Setting up...'
    setup = Setup(language, dir)
    project = setup.getProject()
    print 'Done.'
    print ''
    print '==================================='
    print ''
    print 'Creating directories...'
    project.createDirectories()
    print 'Done.'
    print ''
    print '==================================='
    print ''
    print 'Copying source files to work directory...'
    project.copyFiles()
    print 'Done.'
    print ''
    print '==================================='
    print ''
    print 'Converting source files...'
    project.createXMLFiles()
    project.moveXMLFiles()
    print 'Done.'
    print ''
    print '==================================='
    print ''
    print 'Generating statistics...'
    stats = project.getStats()
    dict_file = stats.getStatistics()
    print 'Done.'
    print ''
    print '==================================='
    print ''
    print 'Exporting data to csv file...'
    stats.exportDataToCSV(dict_file)
    print 'Done.'
    print ''
    print '==================================='

#    print ''
#    print 'Creating results csv file...'
#    stats.exportResultsToCSV()
#    print 'Done.'
#    print ''
#    print '==================================='

    

def main():
    
    try:
        opts, extra_params = getopt.getopt(sys.argv[1:], "hgl:w:p:", ["help", "generate", "language=", "workspace=", "project="])
    except getopt.GetoptError:          
        usage()
        sys.exit(2)
        
    language = None
    export = None
    generate = False
    dir = None
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()
        else:
            if opt in ['-g', '--generate']:
                generate = True
            if opt in ['-l', '--language']:
                language = arg
            if opt in ['-w', '--workspace', '-p', '--project']:
                dir = arg
            
    if language is None or dir is None:
        usage()
        sys.exit()
    else:
        print dir
        abs_dir = os.path.abspath(dir)
        if not os.path.isdir(abs_dir):
            print '%s is not a directory.' % (abs_dir)
            sys.exit()
        else:
            if opt in ['-p', '--project']:
                generate_statistical_data(language, abs_dir)
            elif opt in ['-w', '--workspace']:
                for project in os.listdir(abs_dir):
                    project_dir = os.path.join(abs_dir, project)
                    if os.path.isdir(project_dir):
                        generate_statistical_data(language, project_dir)

if __name__ == '__main__': main()