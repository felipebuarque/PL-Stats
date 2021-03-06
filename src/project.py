# -*- coding: utf-8 -*-
'''
Created on 19/06/2010

@author: felipe
'''
import os
from statisticsC import StatisticsC
from statisticsJava import StatisticsJava

class Project(object):
    '''
    Class to setting project according it language
    '''
    
    def __init__(self, script_dir, project_dir):
        self.project_dir = project_dir
        self.work_dir = self.project_dir + '/_pl-stats'
        self.xml_dir = self.work_dir + '/xmls'
        self.project_results_dir = self.work_dir + '/results'
    
    def createDirectories(self):
        '''
        Create directory of XML files
        '''
        os.chdir(self.project_dir)
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
            os.mkdir(self.xml_dir)
            os.mkdir(self.project_results_dir)
            
    def createXMLFiles(self):
        '''
        Create XML files from source code
        '''
        os.chdir(self.work_dir)
        if len(os.listdir(self.xml_dir)) == 0:
            for file in os.listdir(self.work_dir):
                if os.path.isdir(file):
                    continue
                name = file.split('.')
                os.system(self.script_command + " " + file + " " + name[0] + ".xml")
    
    def copyFiles(self, work_dir, project_dir, flst):
        pass
    
    def getStats(self):
        pass


class ProjectC(Project):
    '''
    Settings for C projects
    '''
    
    def __init__(self, script_dir, project_dir):
        super(ProjectC, self).__init__(script_dir, project_dir)
        self.script_command = script_dir + ' -l C --no-xml-declaration'
        
    def copyFiles(self):
        '''
        Walk in project directories
        '''
        if len(os.listdir(self.work_dir)) < 4:
            os.path.walk(self.project_dir, self.__walkDirectories, None)
        
    def __walkDirectories(self, arg, dir, flst):
        '''
        Copy C files to work directory
        '''
        for file in flst:
            fullFile = os.path.join(dir, file)
            if fullFile.__str__().endswith('.c') and \
                not fullFile.__str__().__contains__('_pl-stats'):
                os.system("cp " + fullFile + " " + self.work_dir)
    
    def moveXMLFiles(self):
        '''
        Move XML files from work directory to XML directory
        '''
        os.chdir(self.work_dir)
        for file in os.listdir(self.work_dir):
            if file.__contains__('.xml'):
                os.system("mv " + file + " " + self.xml_dir)
    
    def getStats(self):
        '''
        Return an instance of StatisticsC
        '''
        return StatisticsC(self.project_dir, self.work_dir, self.xml_dir, self.project_results_dir)


class ProjectJava(Project):
    '''
    Settings for Java projects
    '''
    
    def __init__(self, script_dir, project_dir):
        super(ProjectJava, self).__init__(script_dir, project_dir)
        self.script_command = script_dir + ' -l Java --no-namespace-decl --no-xml-declaration'
        
    def copyFiles(self):
        '''
        Walk in project directories
        '''
        os.path.walk(self.project_dir, self.__walkDirectories, None)
        
    def __walkDirectories(self, arg, dir, flst):
        '''
        Copy C files to work directory
        '''
        for file in flst:
            fullFile = os.path.join(dir, file)
            if fullFile.__str__().endswith('.java') and \
                not fullFile.__str__().__contains__('_pl-stats'):
                os.system("cp " + fullFile + " " + self.work_dir)

    def moveXMLFiles(self):
        '''
        Move XML files from work directory to XML directory
        '''
        os.chdir(self.work_dir)
        for file in os.listdir(self.work_dir):
            if file.__contains__('.xml'):
                os.system("mv " + file + " " + self.xml_dir)
    
    def getStats(self):
        '''
        Return an instance of StatisticsJava
        '''
        return StatisticsJava(self.project_dir, self.work_dir, self.xml_dir, self.project_results_dir)