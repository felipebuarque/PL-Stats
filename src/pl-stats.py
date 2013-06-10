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

def main():
    
    try:
        opts, extra_params = getopt.getopt(sys.argv[1:], "hgl:e:w:p:", ["help", "generate", "language=", "export=", "workspace=", "project="])
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
            if opt in ['-e', '--export']:
                export = arg
            if opt in ['-w', '--workspace', '-p', '--project']:
                dir = arg
            
    if language is None:
        usage()
        sys.exit()

#    if len(extra_params) > 1:
#        usage()
#        sys.exit()
#    else:
#        project_name = extra_params[0]
    
    if dir != None:
        if opt == '-p':
            project_name = os.path.abspath(dir)
            print ''
            print project_name
    
            # Set the variables
            print ''
            print 'Setting up...'
            setup = Setup(language, project_name)
        
            # Set the project type (C or Java)
            project = setup.getProject()
            print 'Done.'
            print ''
            print '==================================='
        
            # Create the work directory (pl_stats directory)
            print ''
            print 'Creating directories...'
            project.createDirectories()
            print 'Done.'
            print ''
            print '==================================='
            
            # Copy files from project to work directory
            print ''
            print 'Copying source files to work directory...'
            project.copyFiles()
            print 'Done.'
            print ''
            print '==================================='
            
            # Create XML files from project source code
            print ''
            print 'Converting source files...'
            project.createXMLFiles()
            
            # Remove source files from work directory
            project.moveXMLFiles()
            print 'Done.'
            print ''
            print '==================================='
            
            # Create the object to manipulate project statistics
            print ''
            print 'Generating statistics...'
            stats = project.getStats()
            
            # Get project statistics
            dict_methods, dict_features, dict_cbr, dict_vsoc, dict_decl_coupling, dict_assign_coupling = stats.getStatistics()
            print 'Done.'
            print ''
            print '==================================='
            
            # Export directives results do XLS file
        #    print ''
        #    print 'Creating directives sheet...'
        #    stats.exportDirectivesToXLS(dict_methods, dict_features)
        #    print 'Done.'
        #    print ''
        #    print '==================================='
        #
        #    # Export dependencies results do XLS file
        #    print ''
        #    print 'Creating dependencies sheet...'
        #    stats.exportDependenciesToXLS(dict_decl_coupling, dict_assign_coupling)
        #    print 'Done.'
        #    print ''
        #    print '==================================='
        
            # Export directives data to CSV file
            print ''
            print 'Creating directives_data csv file...'
            stats.exportDirectivesDataToCSV(dict_methods, dict_features)
            print 'Done.'
            print ''
            print '==================================='
            
            # Export directives results do CSV file
            print ''
            print 'Creating directives_results csv file...'
            stats.exportDirectivesResultsToCSV(dict_methods, dict_features)
            print 'Done.'
            print ''
            print '==================================='
            
            # Export dependencies results do CSV file
            print ''
            print 'Creating dependencies csv file...'
            stats.exportDependenciesToCSV(dict_decl_coupling, dict_assign_coupling)
            print 'Done.'
            print ''
            print '==================================='
        else:
            for project_dir in os.listdir(os.path.abspath(dir)):
                project_name = os.path.abspath(dir+project_dir)
                print ''
                print project_name
        
                # Set the variables
                print ''
                print 'Setting up...'
                setup = Setup(language, project_name)
            
                # Set the project type (C or Java)
                project = setup.getProject()
                print 'Done.'
                print ''
                print '==================================='
            
                # Create the work directory (pl_stats directory)
                print ''
                print 'Creating directories...'
                project.createDirectories()
                print 'Done.'
                print ''
                print '==================================='
                
                # Copy files from project to work directory
                print ''
                print 'Copying source files to work directory...'
                project.copyFiles()
                print 'Done.'
                print ''
                print '==================================='
                
                # Create XML files from project source code
                print ''
                print 'Converting source files...'
                project.createXMLFiles()
                
                # Remove source files from work directory
                project.moveXMLFiles()
                print 'Done.'
                print ''
                print '==================================='
                
                # Create the object to manipulate project statistics
                print ''
                print 'Generating statistics...'
                stats = project.getStats()
                
                # Get project statistics
                dict_methods, dict_features, dict_cbr, dict_vsoc, dict_decl_coupling, dict_assign_coupling = stats.getStatistics()
                print 'Done.'
                print ''
                print '==================================='
                
                # Export directives results do XLS file
            #    print ''
            #    print 'Creating directives sheet...'
            #    stats.exportDirectivesToXLS(dict_methods, dict_features)
            #    print 'Done.'
            #    print ''
            #    print '==================================='
            #
            #    # Export dependencies results do XLS file
            #    print ''
            #    print 'Creating dependencies sheet...'
            #    stats.exportDependenciesToXLS(dict_decl_coupling, dict_assign_coupling)
            #    print 'Done.'
            #    print ''
            #    print '==================================='
            
                # Export directives data to CSV file
                print ''
                print 'Creating directives_data csv file...'
                stats.exportDirectivesDataToCSV(dict_methods, dict_features)
                print 'Done.'
                print ''
                print '==================================='
                
                # Export directives results do CSV file
                print ''
                print 'Creating directives_results csv file...'
                stats.exportDirectivesResultsToCSV(dict_methods, dict_features)
                print 'Done.'
                print ''
                print '==================================='
                
                # Export dependencies results do CSV file
                print ''
                print 'Creating dependencies csv file...'
                stats.exportDependenciesToCSV(dict_decl_coupling, dict_assign_coupling)
                print 'Done.'
                print ''
                print '==================================='

    print '==================================='
    print '######### PL-Stats - v. 0.5 #########'
    print '-----------------------------------'
    print '# Project: ' + project_name.__str__()
    print '-----------------------------------'
    print '# Total of project methods: ' + len(dict_methods).__str__()
    print '==================================='

if __name__ == '__main__': main()