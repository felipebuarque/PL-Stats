# -*- coding: utf-8 -*-
'''
Created on 26/04/2011

@author: felipe
'''
import os
import xlrd

class Util(object):
    '''
    Class to help on statistics data
    '''
    def __init__(self, workspace_dir):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.project_results_dir = '/_pl-stats/results/'
        self.error_dir = '/_pl-stats/error/'
        self.xml_dir = '/_pl-stats/xmls/'
        self.directives_sheet = '%s%s' % (self.project_results_dir, 'directives.xls')
    
    def getProjectsAnalyzed(self):
        '''
        Count the total of projects analyzed
        '''
        os.chdir(self.workspace_dir)
        return [dir for dir in os.listdir(self.workspace_dir) if os.path.exists(os.path.abspath('%s%s' % (dir, self.directives_sheet)))]
    
    def countMethods(self):
        '''
        Count the total of methods analyzed
        '''
        count = 0
        os.chdir(self.workspace_dir)
        for dir in self.getProjectsAnalyzed():
            wb = xlrd.open_workbook(os.path.abspath('%s%s' % (dir, self.directives_sheet)))
            for sheet in wb.sheets():
                count += sheet.nrows - 20
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
        

dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace'
util = Util(dir)
print 'Number of projects analyzed: %d' % (len(util.getProjectsAnalyzed()))
print 'Number of methods analyzed: %d' % (util.countMethods())
print 'Number of converted files: %d' % (util.countConvertedFiles())
print 'Number of files that fail: %d' % (util.countErrorFiles())