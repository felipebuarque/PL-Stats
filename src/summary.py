# -*- coding: utf-8 -*-
'''
Created on 19/05/2011

@author: felipe
'''
import os
import csv

class Summary(object):
    '''
    Generate summary results
    '''
    def __init__(self, language, workspace):
        self.language = language
        self.workspace = os.path.abspath(workspace)
        self.project_results_dir = '/_pl-stats/results'
        self.raffle_summary_file = 'raffle_summary_%s.csv'
        self.directives_summary_file = 'directive_summary.csv'


    
    def summary_raffle(self, dependencies, montecarlo):
        '''
        Handle raffle summary
        '''
        if dependencies:
            raffle_file = 'raffle_with_dependencies_%s.csv' % (montecarlo - 1)
        else:
            raffle_file = 'raffle_without_dependencies_%s.csv' % (montecarlo - 1)
            
        file_writer = csv.writer(open(self.workspace + '/%s' % (self.raffle_summary_file % (montecarlo - 1)), 'wb'), delimiter=';', quotechar='|')
        
        # Header
        write = []
        write.append("Project")
        write.append("Method_FQDN")
        write.append(">2 #ifdefs?")
        write.append("#ifdefs")
        write.append("Vars")
        write.append("Drawn_var")
        write.append("VS_fragments")
        write.append("VS_features")
        write.append("VS_loc")
        write.append("EI_fragments")
        write.append("EI_features")
        write.append("EI_loc")
        file_writer.writerow(write)
        ##########
        
        for project in os.listdir(self.workspace):
            if os.path.isdir(self.workspace + '/' +project):
                print project
                header = [False, False]
                dict_more_than_balance = {}
                dict_less_equal_than_balance = {}
                
                file_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + '/' + raffle_file, 'rb'), delimiter=';', quotechar='|')
                
                for row_reader in file_reader:
                    if header[0]:
                        if not header[1] and (not row_reader.__contains__('---') and not row_reader.__contains__('Total of methods')):
                            vars = []
                            vars.append(row_reader[1])
                            vars.append(row_reader[2])
                            dict_more_than_balance[row_reader[0]] = vars
                        elif header[1]:
                            vars = []
                            vars.append(row_reader[1])
                            vars.append(row_reader[2])
                            dict_less_equal_than_balance[row_reader[0]] = vars
                        elif row_reader.__contains__('Total of methods'):
                            header[1] = True
                           
                    elif row_reader.__contains__('Total of methods'):
                        header[0] = True
                
                for method in dict_more_than_balance:
                    write = []
                    write.append(project)
                    write.append(method)
                    write.append("Y")
                    write.append("")
                    write.append(dict_more_than_balance[method][0])
                    write.append(dict_more_than_balance[method][1])
                    file_writer.writerow(write)
                    
                for method in dict_less_equal_than_balance:
                    write = []
                    write.append(project)
                    write.append(method)
                    write.append("N")
                    write.append("")
                    write.append(dict_less_equal_than_balance[method][0])
                    write.append(dict_less_equal_than_balance[method][1])
                    file_writer.writerow(write)


    
    def summary_directives(self):
        '''
        Handle directives summary
        '''
        directives_results_file = 'directives_result.csv'
        dependencies_file = 'dependencies.csv'
        cloc_file = 'cloc.csv'
        
        file_writer = csv.writer(open(self.workspace + '/%s' % (self.directives_summary_file), 'wb'), delimiter=';', quotechar='|')
        
        # Header
        write = []
        write.append("Project")
        write.append("BLoC")
        write.append("CLoC")
        write.append("SLoC")
        write.append("ToM")
        write.append("MwDi")
        write.append("MwoDi")
        write.append("NoDiAVGAll")
        write.append("NoDiAVG")
        write.append("SDAll")
        write.append("SD")
        write.append("M1")
        write.append("Mm1")
        write.append("Mm2")
        write.append("Mm3")
        write.append("Mm4")
        write.append("Mm5")
        write.append("Mm10")
        write.append("Mm20")
        write.append("MwDe")
        write.append("MwDDe")
        write.append("MwADe")
        file_writer.writerow(write)
        ##########
        
        for project in os.listdir(self.workspace):
            if os.path.isdir(self.workspace + '/' +project):
                print project
                
                # Get CLoC project information
                header = True
                cloc_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + '/' + cloc_file, 'rb'), delimiter=',', quotechar='|')
                for row_reader in cloc_reader:
                    if header:
                        header = False
                    elif row_reader[1].lower() == self.language:
                        cloc = []
                        cloc.append(row_reader[2])
                        cloc.append(row_reader[3])
                        cloc.append(row_reader[4])
                        break
                
                # Get dependencies project information
                header = True
                mwdde_count = 0
                mwade_count = 0
                dep_count = 0
                dependencies_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + '/' + dependencies_file, 'rb'), delimiter=';', quotechar='|')
                for row_reader in dependencies_reader:
                    if header:
                        header = False
                    else:
                        if int(row_reader[2]) > 0:
                            mwdde_count += 1
                        if int(row_reader[5]) > 0:
                            mwade_count += 1
                        dep_count += int(row_reader[8])
                
                # Get directives project information
                header = True
                directives_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + '/' + directives_results_file, 'rb'), delimiter=';', quotechar='|')
                
                for row_reader in directives_reader:
                    if header:
                        header = False
                    else:
                        write = []
                        write.append(project)
                        write.append(cloc[0])
                        write.append(cloc[1])
                        write.append(cloc[2])
                        write.append(row_reader[0])
                        write.append(row_reader[1])
                        write.append(row_reader[2])
                        write.append(row_reader[3])
                        write.append(row_reader[4])
                        write.append(row_reader[5])
                        write.append(row_reader[6])
                        write.append(row_reader[7])
                        write.append(row_reader[8])
                        write.append(row_reader[9])
                        write.append(row_reader[10])
                        write.append(row_reader[11])
                        write.append(row_reader[12])
                        write.append(row_reader[13])
                        write.append(row_reader[14])
                        write.append(dep_count)
                        write.append(mwdde_count)
                        write.append(mwade_count)
                        file_writer.writerow(write)

dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/projects_c/'
summary = Summary('c', dir)
#summary.summary_raffle(False, 1)
summary.summary_directives()    