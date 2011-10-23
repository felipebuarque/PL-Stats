# -*- coding: utf-8 -*-
'''
Created on 19/05/2011

@author: felipe
'''
import os
import csv
import numpy
from statistics import Statistics

class Summary(object):
    '''
    Generate summary results
    '''
    def __init__(self, language, workspace):
        self.language = language
        self.workspace = os.path.abspath(workspace)
        self.project_results_dir = '/_pl-stats/results/'
        self.raffle_summary_file = 'raffle_summary_%s.csv'
        self.directives_summary_file = 'directive_summary.csv'
        self.dependencies_summary_file = 'dependencies_summary.csv'
        self.summary_file = 'summary.csv'
        
        self.data_file = 'data.csv'
        self.results_file = 'results.csv'


    
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


    def summary_projects_data(self):
        '''
        Summary data.csv project files in results.csv
        '''
        # Header
        header = []
        header.append('Project')
        header.append('NoM')
        header.append('MLoC')
        header.append('MLoCAVG')
        header.append('MLoCSD')
        header.append('MLoF')
        header.append('MLoFAVGAll')
        header.append('MLoFAVG')
        header.append('MLoFSDAll')
        header.append('MLoFSD')
        header.append('MwDi')
        header.append('MwoDi')
        header.append('NoDi')
        header.append('NoDiAVGAll')
        header.append('NoDiAVG')
        header.append('NoDiSDAll')
        header.append('NoDiSD')
        for directive in sorted(Statistics.list_directives):
            if directive != 'endif' and directive != 'enddebug':
                header.append('#' + directive)
        header.append('NoFE')
        header.append('NoFEAVGAll')
        header.append('NoFEAVG')
        header.append('NoFESDAll')
        header.append('NoFESD')
        header.append('MwDe')
        header.append('NoDe')
        header.append('NoDeAVGAll')
        header.append('NoDeAVG')
        header.append('NoDeSDAll')
        header.append('NoDeSD')
        for directive in sorted(Statistics.list_directives):
            if directive != 'endif' and directive != 'enddebug':
                header.append('#' + directive)
        
        #####
        
        for project in os.listdir(self.workspace):
            if os.path.isdir(os.path.join(self.workspace, project)):
                print project
                
                mloc = []
                mlof = []
                mlof_all = []
                nodi = []
                nodi_all = []
                list_directives = [0,0,0,0,0,0,0,0,0]
                list_dependencies = [0,0,0,0,0,0,0,0,0]
                nofe = []
                nofe_all = []
                node = []
                node_all = []
                
                read_file = csv.reader(open(os.path.join(self.workspace, project + self.project_results_dir + self.data_file), 'rb'), delimiter=';', quotechar='|')
                flag = True
                for reader in read_file:
                    if flag:
                        flag = False
                    else:
                        if int(reader[1]) > 0:
                            mloc.append(int(reader[1]))
                        
                        mlof_all.append(int(reader[2]))
                        if int(reader[2]) > 0:
                            mlof.append(int(reader[2]))
                        
                        nodi_all.append(int(reader[3]))
                        if int(reader[3]) > 0:
                            nodi.append(int(reader[3]))
                            
                        for i in range(9):
                            list_directives[i] += int(reader[i+4])
                            list_dependencies[i] += int(reader[i+15])
                
                        nofe_all.append(int(reader[13]))
                        if int(reader[13]) > 0:
                            nofe.append(int(reader[13]))
                        
                        node_all.append(int(reader[14]))
                        if int(reader[14]) > 0:
                            node.append(int(reader[14]))
                
                writer_file = csv.writer(open(os.path.join(self.workspace, project + self.project_results_dir + self.results_file), 'w'), delimiter=';', quotechar='|')
                writer_file.writerow(header)
                row = []
                row.append(project)
                row.append(read_file.line_num - 1)
                row.append(numpy.sum(mloc))
                row.append(numpy.average(mloc))
                row.append(numpy.std(mloc))
                row.append(numpy.sum(mlof))
                row.append(numpy.average(mlof_all))
                row.append(numpy.average(mlof))
                row.append(numpy.std(mlof_all))
                row.append(numpy.std(mlof))
                row.append(len(nodi))
                row.append((read_file.line_num - 1) - len(nodi))
                row.append(numpy.sum(nodi))
                row.append(numpy.average(nodi_all))
                row.append(numpy.average(nodi))
                row.append(numpy.std(nodi_all))
                row.append(numpy.std(nodi))
                row += list_directives
                row.append(numpy.sum(nofe))
                row.append(numpy.average(nofe_all))
                row.append(numpy.average(nofe))
                row.append(numpy.std(nofe_all))
                row.append(numpy.std(nofe))
                row.append(len(node))
                row.append(numpy.sum(node))
                row.append(numpy.average(node_all))
                row.append(numpy.average(node))
                row.append(numpy.std(node_all))
                row.append(numpy.std(node))
                row += list_dependencies
                
                writer_file.writerow(row)


    def summary_workspace_data(self):
        '''
        Summary workspace data
        '''
        writer = csv.writer(open(self.workspace + '/%s' % (self.summary_file), 'wb'), delimiter=';', quotechar='|')
        
        # Header
        header = []
        header.append('Project')
        header.append('NoFi')
        header.append('BLoC')
        header.append('CLoC')
        header.append('SLoC')
        header.append('NoM')
        
        header.append('MLoC')
        header.append('MLoCAVG')
        header.append('MLoCSD')
        header.append('MLoF')
        header.append('MLoFAVGAll')
        header.append('MLoFAVG')
        header.append('MLoFSDAll')
        header.append('MLoFSD')
        
        header.append('MwDi')
        header.append('MwoDi')
        header.append('NoDi')
        header.append('NoDiAVGAll')
        header.append('NoDiAVG')
        header.append('NoDiSDAll')
        header.append('NoDiSD')
        for directive in sorted(Statistics.list_directives):
            if directive != 'endif' and directive != 'enddebug':
                header.append('#' + directive)
        header.append('NoFE')
        header.append('NoFEAVGAll')
        header.append('NoFEAVG')
        header.append('NoFESDAll')
        header.append('NoFESD')
        header.append('MwDe')
        header.append('NoDe')
        header.append('NoDeAVGAll')
        header.append('NoDeAVG')
        header.append('NoDeSDAll')
        header.append('NoDeSD')
        for directive in sorted(Statistics.list_directives):
            if directive != 'endif' and directive != 'enddebug':
                header.append('#' + directive)
        
        writer.writerow(header)
        #####
        
        nofi = 0
        cloc_file = 'cloc.csv'
        
        for project in os.listdir(self.workspace):
            if os.path.isdir(self.workspace + '/' + project):
                print project
                results = []
                results.append(project)
                
                # Get NoFi of project
                list_files = []
                list_files = [file for file in os.listdir(os.path.join(self.workspace, project, '_pl-stats')) if not os.path.isdir(os.path.join(self.workspace, project, '_pl-stats', file))]
                results.append(len(list_files))
                
                # Get CLoC project information
                cloc_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + cloc_file, 'rb'), delimiter=',', quotechar='|')
                flag = True
                for row_reader in cloc_reader:
                    if flag:
                        flag = False
                    elif row_reader[1].lower() == self.language:
#                        results.append(row_reader[0])
                        results.append(row_reader[2])
                        results.append(row_reader[3])
                        results.append(row_reader[4])
                        break
                
                data_reader = csv.reader(open(self.workspace + '/' + project + self.project_results_dir + '/' + self.results_file, 'rb'), delimiter=';', quotechar='|')
                flag = True
                list_aux = []
                for row_reader in data_reader:
                    if flag:
                        flag = False
                    else:
                        for i in row_reader[1:]:
#                            print i
                            list_aux.append(i)
                
                results += list_aux
                
                writer.writerow(results)
        

dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/projects_java/'
#dir = '/home/felipe/workspace-msc/pl-stats/projects_c/'
summary = Summary('java', dir)
#summary.summary_raffle(False, 1)
summary.summary_projects_data()
summary.summary_workspace_data()
