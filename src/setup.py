# -*- coding: utf-8 -*-
'''
Created on 19/06/2010

@author: felipe
'''

import os
from project import ProjectC, ProjectJava

class Setup():
    '''
    Class to setting script actuation directories
    '''
    
    def __init__(self, language, project):
        self.language = language.lower()
        self.project_dir = os.path.abspath(project)
        
        # REMEMBER TO SET THE RELATIVE PATH OF SRC2SCRML SCRIPT BEFORE PUBLISH !!!
        self.script_dir = os.path.abspath('/home/felipe/workspace-msc/PL-Stats/scripts/src2srcml.ubuntu')
#        self.script_dir = os.path.abspath('/home/felipe/workspace-msc/pl_stats/scripts/src2srcml')

    
    def getProject(self):
        '''
        Return the project which will be analyzed according it type
        '''
        if self.language == 'c':
            return ProjectC(self.script_dir, self.project_dir)
        elif self.language == 'java':
            return ProjectJava(self.script_dir, self.project_dir)
