# -*- coding: utf-8 -*-
'''
Created on 12/01/2011

@author: felipe
'''
import os, getopt, sys
import xlrd, xlwt, csv
import random

class Raffle(object):
    '''
    Read the dependencies sheet and performs a raffle
    '''
    def __init__(self, project_dir, balance):
        self.project_dir = os.path.abspath(project_dir)
        self.project_results_dir = self.project_dir + '/_pl-stats/results/'
        self.directive_sheet = self.project_results_dir + 'directives_data.csv'
        self.coupling_sheet = self.project_results_dir + 'dependencies.csv'
        self.raffle_sheet = self.project_results_dir + 'raffle_without_dependencies_0.csv'
        self.balance = balance
        self.file_reader = csv.reader(open(self.coupling_sheet, 'rb'), delimiter=';', quotechar='|')


    def getTotalMethods(self):
        '''
        Return the number of methods in the spreadsheet
        '''
        for row in self.file_reader:
            pass
        
        return self.file_reader.line_num - 1
        

    def getMethodsWithoutDependencies(self):
        '''
        Return a dict with variables of methods without dependencies
        '''
        dict = {}
        header = True
        
        for row in self.file_reader:
            if header:
                header = False
            elif int(row[8]) == 0:
                aux = row[1].split(', ')
                dict[row[0]] = list(set(aux))
        
        return dict
        
    
    def getMethodsWithDependencies(self):
        '''
        Return a dict with variables of methods with dependencies
        '''
        dict = {}
        header = True
        
        for row in self.file_reader:
            if header:
                header = False
            elif int(row[8]) == 1:
                aux = row[3] + row[6]
                aux = aux.split(', ')
                dict[row[0]] = list(set(aux))

        return dict

    
    def getMethodsWithDirective(self):
        '''
        Read the directive sheet and return the group methods
        '''
        list_method_more_than_balance = []
        list_method_less_equal_than_balance = []
        
        header = True
        file_reader = csv.reader(open(self.directive_sheet, 'rb'), delimiter=';', quotechar='|')
        
        for row in file_reader:
            if header:
                header = False
            else:
                # get method name
                method_name = row[0]
                # get number of directives
                nod = int(row[10])
                
                if nod > 0:
                    if nod > self.balance:
                        list_method_more_than_balance.append(method_name)
                    else:
                        list_method_less_equal_than_balance.append(method_name)

        return list_method_more_than_balance, list_method_less_equal_than_balance

    
    def getProportion(self, list_more_than_balance, list_less_equal_than_balance, dict_dependencies):
        '''
        Return the proportion between groups of methods
        '''
        dict_methods_with_dependencies_more_than_balance = {}
        dict_methods_with_dependencies_less_equal_than_balance = {}
        
#        total_methods_with_dependencies = len(dict_dependencies)
        dict_proportion = {}
        
        for method in list_more_than_balance:
            if dict_dependencies.__contains__(method):
                dict_methods_with_dependencies_more_than_balance[method] = dict_dependencies[method]
        
        for method in list_less_equal_than_balance:
            if dict_dependencies.__contains__(method):
                dict_methods_with_dependencies_less_equal_than_balance[method] = dict_dependencies[method]
        
        count_more_than_balance = len(dict_methods_with_dependencies_more_than_balance)
        print count_more_than_balance
        count_less_equal_than_balance = len(dict_methods_with_dependencies_less_equal_than_balance)
        print count_less_equal_than_balance
        
        print self.project_dir
#        print "Methods with dependencies and > 2 directives: %s" % (count_more_than_balance)
#        print "Methods with dependencies and <= 2 directives: %s" % (count_less_equal_than_balance)
        
        if count_more_than_balance > count_less_equal_than_balance:
            name = 'more'
            proportion = int(round(float(count_more_than_balance)/float(count_less_equal_than_balance)))
        else:
            name = 'less'
            proportion = int(round(float(count_less_equal_than_balance)/float(count_more_than_balance)))
        
        dict_proportion[name] = proportion
        return dict_methods_with_dependencies_more_than_balance, dict_methods_with_dependencies_less_equal_than_balance, dict_proportion


    def raffle(self, dict):
        '''
        Return the list of methods between ...
        '''
        dict_dependencies_vars = dict
        list_more_than_balance, list_less_equal_than_balance = self.getMethodsWithDirective()
        dict_mtb, dict_letb, dict_proportion = self.getProportion(list_more_than_balance, list_less_equal_than_balance, dict_dependencies_vars)
        
        dict_random_more_methods = {}
        dict_random_less_equal_methods = {}
        
        if dict_proportion.__contains__('less'):
            i = 0
            method_name = dict_mtb.keys()[random.randint(0, len(dict_mtb)-1)]
            dict_random_more_methods[method_name] = dict_mtb[method_name]
#            for i in range(dict_proportion.values()[0]):
            while i < dict_proportion.values()[0]:
                method_name = dict_letb.keys()[random.randint(0, len(dict_letb)-1)]
                if not dict_random_less_equal_methods.__contains__(method_name):
                    dict_random_less_equal_methods[method_name] = dict_letb[method_name]
                    i += 1
        else:
            i = 0
            method_name = dict_letb.keys()[random.randint(0, len(dict_letb)-1)]
            dict_random_less_equal_methods[method_name] = dict_letb[method_name]
#            for i in range(dict_proportion.values()[0]):
            while i < dict_proportion.values()[0]:
                method_name = dict_mtb.keys()[random.randint(0, len(dict_mtb)-1)]
                if not dict_random_more_methods.__contains__(method_name):
                    dict_random_more_methods[method_name] = dict_mtb[method_name]
                    i += 1
        
#        print len(dict_random_more_methods)
#        print len(dict_random_less_equal_methods)
        
        return dict_random_more_methods, dict_random_less_equal_methods, [len(dict_mtb), len(dict_letb)]


    def exportRaffleToXLS(self, dict_random_more_methods, dict_random_less_equal_methods, list_size):
        '''
        Export raffle results to xls spreadsheet
        '''
        os.chdir(self.project_results_dir)
        try:
            wb = xlwt.Workbook(encoding="utf-8")
            sheet = wb.add_sheet("raffle results")
            
            # cabeçalho para "more than" methods
            row_count = 0
            col_count = 0
            row = sheet.row(row_count)
            row.write(col_count, 'Methods with more than %s directives' % (str(self.balance)))
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'Total of methods: %s' % (str(list_size[0])))
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'Method FQDN')
            row.write(col_count+1, 'Dependencies Vars')
            row.write(col_count+2, 'Drawn var')
            ###
            for method in dict_random_more_methods:
                list_vars = dict_random_more_methods[method]
                row_count += 1
                row = sheet.row(row_count)
                row.write(col_count, method)
                row.write(col_count+1, ", ".join(list_vars))
                row.write(col_count+2, list_vars[random.randint(0, len(list_vars)-1)])
                
            
            # cabeçalho para "less or equal than" methods
            row_count = len(dict_random_more_methods) + 4
            col_count = 0
            row = sheet.row(row_count)
            row.write(col_count, 'Methods with less or equal than %s directives' % (str(self.balance)))
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'Total of methods: %s' % (str(list_size[1])))
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'Method FQDN')
            row.write(col_count+1, 'Dependencies Vars')
            row.write(col_count+2, 'Drawn var')
            ###
            for method in dict_random_less_equal_methods:
                list_vars = dict_random_less_equal_methods[method]
                row_count += 1
                row = sheet.row(row_count)
                row.write(col_count, method)
                row.write(col_count+1, ", ".join(list_vars))
                row.write(col_count+2, list_vars[random.randint(0, len(list_vars)-1)])
            
            wb.save('raffle2-4.xls')
        except Exception as e:
            print 'Exception (exportRaffleToXLS): ' + e.__str__()
        
    
    def exportRaffleToCSV(self, dict_random_more_methods, dict_random_less_equal_methods, list_size):
        '''
        '''
        row = []
        file_writer = csv.writer(open(self.raffle_sheet, 'wb'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # Header
        row.append("Method_FQDN")
        row.append("Vars")
        row.append("Drawn Vars")
        file_writer.writerow(row)
        #########
        row = []
        row.append("---")
        file_writer.writerow(row)
        
        row = []
        row.append("Total of methods")
        row.append(list_size[0])
        file_writer.writerow(row)
        for method in dict_random_more_methods:
            row = []
            row.append(method)
            list_vars = dict_random_more_methods[method]
            row.append(", ".join(list_vars))
            var_drawn = random.randint(0, len(list_vars)-1)
            row.append(list_vars[var_drawn])
            file_writer.writerow(row)
        
        row = []
        row.append("---")
        file_writer.writerow(row)
            
        row = []
        row.append("Total of methods")
        row.append(list_size[1])
        file_writer.writerow(row)
        for method in dict_random_less_equal_methods:
            row = []
            row.append(method)
            list_vars = dict_random_less_equal_methods[method]
            row.append(", ".join(list_vars))
            var_drawn = random.randint(0, len(list_vars)-1)
            row.append(list_vars[var_drawn])
            file_writer.writerow(row)
            
            
def generateProjectData(dir):
    '''
    Generate Raffle project data
    '''
    raffle = Raffle(os.path.abspath(dir), 2)
    dict_random_more_methods, dict_random_less_equal_methods, lens = raffle.raffle(raffle.getMethodsWithoutDependencies())
    raffle.exportRaffleToCSV(dict_random_more_methods, dict_random_less_equal_methods, lens)


def generateWorkspaceData(dir):
    '''
    Generate Raffle workspace of projects data
    '''
    for project in os.listdir(os.path.abspath(dir)):
        print '======================================================'
        print 'Project: %s' % (project)
        raffle = Raffle(os.path.join(os.path.abspath(dir), project), 2)
        dict_random_more_methods, dict_random_less_equal_methods, lens = raffle.raffle(raffle.getMethodsWithoutDependencies())
        raffle.exportRaffleToCSV(dict_random_more_methods, dict_random_less_equal_methods, lens)
    
            
def usage():
    print "opa!"

def main():
    try:
        opts, extra_params = getopt.getopt(sys.argv[1:], "hp:w:m:", ["help", "project=", "workspace=", "montecarlo="])
    except getopt.GetoptError:          
        usage()
        sys.exit(2)
    
    dir = None
    flag = None
    montecarlo = 1
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
        elif opt in ['-m', '--montecarlo']:
            montecarlo = arg
        else:
            usage()
            sys.exit()

    if flag == 'p':
        generateProjectData(dir)
    else:
        generateWorkspaceData(dir)

if __name__ == '__main__': main()
