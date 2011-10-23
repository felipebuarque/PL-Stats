# -*- coding: utf-8 -*-
'''
Created on 26/04/2011

@author: felipe
'''
import os
import csv

class Util(object):
    '''
    Class to help on statistics data
    '''
    def __init__(self, workspace_dir):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.project_results_dir = '/_pl-stats/results/'
        self.error_dir = '/_pl-stats/error/'
        self.xml_dir = '/_pl-stats/xmls/'
        self.data = '%s%s' % (self.project_results_dir, 'data.csv')
    
    def getProjectsAnalyzed(self):
        '''
        Count the total of projects analyzed
        '''
        os.chdir(self.workspace_dir)
        return [dir for dir in os.listdir(self.workspace_dir) if os.path.exists(os.path.abspath('%s%s' % (dir, self.data)))]
    
    def countMethods(self):
        '''
        Count the total of methods analyzed
        '''
        count = 0
        os.chdir(self.workspace_dir)
        for dir in self.getProjectsAnalyzed():
            file_reader = csv.reader(open(os.path.abspath('%s%s' % (dir, self.data)), 'rb'), delimiter=';', quotechar='/')
            for reader in file_reader:
                pass
            count += file_reader.line_num - 1
        return count
    
    def countConvertedFiles(self):
        '''
        Count the number of converted files
        '''
        count = 0
        os.chdir(self.workspace_dir)
        for dir in self.getProjectsAnalyzed():
            list_xml = os.listdir(os.path.abspath('%s%s' % (dir, self.xml_dir)))
            count += len(list_xml)
        return count
    
    def countErrorFiles(self):
        '''
        Count the number of files that fail
        '''
        count = 0
        os.chdir(self.workspace_dir)
        for dir in self.getProjectsAnalyzed():
            if os.path.exists('%s%s' % (dir, self.error_dir)):
                list_error = os.listdir(os.path.abspath('%s%s' % (dir, self.error_dir)))
                count += len(list_error) - 1
        return count
    
    def removeErrorDirectory(self):
        '''
        Removes _pl-stats/error project directory
        '''
        for project in os.listdir(self.workspace_dir):
            if os.path.isdir(os.path.join(self.workspace_dir, project)):
                print project
                error_dir = os.path.join(self.workspace_dir, project, '_pl-stats/error')
                if os.path.exists(error_dir):
                    os.system('rm -rf %s' % (error_dir))
        print 'Done.'
        
    
    def removeStatsDirectory(self):
        '''
        Removes _pl-stats project directory
        '''
        for project in os.listdir(self.workspace_dir):
            if os.path.isdir(os.path.join(self.workspace_dir, project)):
                print project
                dir = os.path.join(self.workspace_dir, project, '_pl-stats')
                if os.path.exists(dir):
                    os.system('rm -rf %s' % (dir))
        print 'Done.'
        

dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/projects_java/'
util = Util(dir)
print 'Number of projects analyzed: %d' % (len(util.getProjectsAnalyzed()))
print 'Number of methods analyzed: %d' % (util.countMethods())
print 'Number of converted files: %d' % (util.countConvertedFiles())
print 'Number of files that fail: %d (%.2f%%)' % (util.countErrorFiles(), (float(util.countErrorFiles())/float(util.countConvertedFiles()))*100)
#util.removeErrorDirectory()
#util.removeStatsDirectory()