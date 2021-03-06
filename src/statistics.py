# -*- coding: utf-8 -*-
'''
Created on 17/06/2010

@author: felipe
'''

import os
import xlwt
import csv
import numpy
import datetime 

class Statistics(object):
    '''
    Super class to handle project statistics
    '''
    list_directives = [
                       '#ifdef ',
                       '#ifndef ',
                       '#elifdef ',
                       '#elifndef ',
                       '#if ',
                       '#elif ',
                       '#else',
                       '#endif',
#                      '#condition ',
                       '#debug ',
                       '#mdebug ',
                       '#enddebug',
#                      '#define ',
#                      '#undefine',
#                      '#expand',
                        ]
    
    list_extra_metrics = [
                          'Coupling',
                          ]
    
    def __init__(self, project_dir, src_dir, work_dir, results_dir):
        self.project_dir = project_dir
        self.work_dir = src_dir
        self.xml_dir = work_dir
        self.project_results_dir = results_dir
        self.prefix_src = ''
        self.prefix_cpp = ''
    
    def getStatistics(self):
        pass
    
    def logErrors(self, filename, exception):
        '''
        Cria um log de erro e copia o arquivo que deu erro para _pl-stat/error
        '''
        error_dir = self.work_dir + '/error'
        log_file = error_dir + '/log.txt'
        if not os.path.exists(error_dir):
            os.mkdir(error_dir)
        if not os.path.exists(log_file):
            log_file = open(log_file, 'w')
        else:
            log_file = open(log_file, 'a')
        date_time = datetime.datetime.now()
        if not filename.__contains__('None'):
            filename = filename + '.c'
            os.system("mv %s %s" % (self.work_dir + '/' + filename, error_dir))
        log_file.write('Date and time: %s\nFilename: %s\n\n' % (date_time, filename))
        log_file.write('%s\n\n' % (str(exception)))
        log_file.write('----------------------------------------------------\n\n')
    
    def _getPackageName(self, document):
        '''
        Retorna o nome do pacote do arquivo
        '''
        pack_name = ''
        package = document.find(self.prefix_src + 'package')
        if package is not None:
            for child in package.iterchildren():
                pack_name += child.text + '.'
                
        return pack_name
    
    def _getMethodName(self, file_name, pack_name, function):
        '''
        Retorna o nome do método
        '''
        return pack_name + file_name + function.findtext(self.prefix_src + 'name')
    
    def _checkMethodName(self, dict_methods, method_name, method_repeated):
        '''
        Verifica se já existe método com esse nome na lista
        '''
        if dict_methods.__contains__(method_name):
            method_repeated += 1
            method_name += method_repeated.__str__()
            
        return [method_name, method_repeated]
    
    def _getFunctionTags(self, document):
        '''
        Retorna uma lista de elementos de tag <function>
        '''
        return [f for f in document.getiterator('*') if f.tag == self.prefix_src + 'constructor' or f.tag == self.prefix_src + 'function']
    
    def _getParamVarDeclared(self, function):
        '''
        Retorna as variáveis passadas como parâmetro do método
        '''
        aux = ''
        dict_params_decl = {}
        
        for param in function.iter(tag=self.prefix_src + 'param'):
            try:
                names = [child for child in param.iter(self.prefix_src + 'name') if child.getparent().tag == self.prefix_src + 'decl']
                for name in names:
                    if len(name.getchildren()) == 0:
                        aux = name.text
                    else:
                        subname = name.find(self.prefix_src + 'name')
                        aux = subname.text
                    dict_params_decl[aux] = 'Mandatory'
                    
            except Exception as e:
                print "Exception (_getParamVarDeclared): %s" % (e.__str__())

        return dict_params_decl
    
    def _isEndDirective(self, directive):
        '''
        Verifica se a diretiva é um #endif ou #enddebug
        '''
        # foi utilizado startswith pois a diretiva pode vir seguida de espaço em branco
        if directive.startswith('endif') or directive.startswith('enddebug'):
            return True
        return False
    
    def _isMiddleDirective(self, directive):
        '''
        Verifica se a diretiva é um #else
        '''
        # foi utilizado startswith pois a diretiva pode vir seguida de espaço em branco
        if directive.startswith('else'):
            return True
        return False
    
    def _isMiddleDeclDirective(self, directive):
        '''
        Verifica se a diretiva é um #elifdef ou #elifndef
        '''
        if directive == 'elif' or directive == 'elifdef' or directive == 'elifndef':
            return True
        return False
    
    def _getVarDeclared(self, list_vars_decl, dict_decl, stack_directive, decl_stmt):
        '''
        Coloca no dicionário as variáveis envolvidas em uma declaração
        '''
        vars = [child for child in decl_stmt.iter(self.prefix_src + 'name') if child.getparent().tag == self.prefix_src + 'decl']
        
        for var in vars:
            if len(var.getchildren()) == 0:
                aux = var.text
            else:
                subname = var.find(self.prefix_src + 'name')
                aux = subname.text
            list_vars_decl.append(aux)
            
        try:
            if len(stack_directive) > 0:
                for var in vars:
                    dict_decl[var.text] = stack_directive.pop()
                    stack_directive.append(dict_decl[var.text])
            else:
                for var in vars:
                    dict_decl[var.text] = 'Mandatory'

        except Exception as e:
            print "Exception (_getVarDeclared): %s" % (e.__str__())
        
        return [list_vars_decl, dict_decl, stack_directive]
    
    def _checkFeature(self, stack_directive):
        '''
        Retorna qual a feature atual 
        '''
        if len(stack_directive) > 0:
            assign_feature = stack_directive.pop()
            stack_directive.append(assign_feature)
        else:
            assign_feature = 'Mandatory'

        return assign_feature
    
    def _getExprVars(self, expr_names, call):
        '''
        Retorna uma lista das variáveis declaradas em uma atribuição
        '''
        list_vars = []
        aux = ''
        for name in expr_names:
            # pode-se ter: <name><name>...</name></name> sem name.text
            if name.text is not None and not self._isBooleanNullVar(name):
                if name.tail is not None and name.tail == '.':
                    # checa se NÃO é uma classe e sim um objeto
                    if name.text[0].islower():
                        list_vars.append(name.text)
                    aux += name.text + name.tail
                else:
                    aux += name.text
                    list_vars.append(aux)
                    aux = ''

        # remove os 'this'
        if list_vars.__contains__('this'):
            list_vars.remove('this')

        # remove o nome dos métodos da lista
        if call is not None:
            call_name = call.find(self.prefix_src + 'name')
            if call_name is not None:
                if call_name.text in list_vars:
                    list_vars.remove(call_name.text)
                else:
                    names = call_name.findall(self.prefix_src + 'name')
                    aux = ''
                    for name in names:
                        if name.tail == '.':
                            aux += name.text + name.tail
                        else:
                            aux += name.text
                    
                    if aux in list_vars:
                        list_vars.remove(aux)

        return list_vars
    
    def _isBooleanNullVar(self, expr_name):
        '''
        Verifica se uma tag <name> é do tipo boolean
        '''
        if expr_name.text == 'true' or expr_name.text == 'false' \
            or expr_name.text == 'True' or expr_name.text == 'False' \
            or expr_name.text == 'null' or expr_name.text == 'NULL':
            return True
        return False
    
    def _checkDeclCoupling(self, assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling):
        '''
        Checa o acoplamento do tipo declaração<->uso
        '''
        for var in list_var_assign:
        # checa se a variável já foi declarada
            if var in dict_decl or var in dict_param_decl:
                if var in dict_decl:
                    dict = dict_decl
                else:
                    dict = dict_param_decl
                    
                if dict[var] != assign_feature:
                    count += 1
                    if not var in list_var_coupling:
                        list_var_coupling.append(var)
                    list_feature_coupling.append(dict[var] + '<->' + assign_feature)
        
        return count, list_var_coupling, list_feature_coupling
    
    def _checkAssignCoupling(self, assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling):
        '''
        Checa o acoplamento do tipo atribuição<->uso
        '''
        for var in list_var_assign:
            # checa se a variável já foi declarada
            if var in dict_decl:
                if dict_decl[var] != assign_feature:
                    count += 1
                    if not var in list_var_coupling:
                        list_var_coupling.append(var)
                    list_feature_coupling.append(dict_decl[var] + '<->' + assign_feature)
            else:
                # se não foi declarada, coloca na lista de variáveis declaradas
                dict_decl[var] = assign_feature
        
        return count, dict_decl, list_var_coupling, list_feature_coupling
    
    def exportDirectivesToXLS(self, dict_methods, dict_features):
        '''
        Exporta o resultado das diretivas para o arquivo directives.csv
        '''
        os.chdir(self.project_results_dir)

        # coloca as diretivas em ordem alfabética 
        list_directives_sorted = sorted(Statistics.list_directives)
#            list_cbr_keys_sorted = sorted(['Continue', 'Break', 'Return'])
        
        wb = xlwt.Workbook(encoding="utf-8")
        
        row_limit = 65535
        list_methods = dict_methods.keys()
        total_methods = len(list_methods)
        number_of_sheets = (total_methods/row_limit) + 1
        
        for x in range(number_of_sheets):
            sheet = wb.add_sheet("directives%d" % (x+1))
            
            # cabeçalho
            row_count = 0
            col_count = 0
            row = sheet.row(row_count)
            row.write(col_count, 'Method FQDN')
            for value in list_directives_sorted:
                # não nos interessa para os valores da planilha
                if not value.__contains__('#endif') and not value.__contains__('#enddebug'):
                    col_count += 1
                    row.write(col_count, value)
            row.write(col_count+1, 'NoDi')
            row.write(col_count+2, 'NoFE')
            ######
            
            limit_min = x*(row_limit - 20)
            if x == (number_of_sheets - 1):
                limit_max = total_methods
            else:
                limit_max = (x+1)*(row_limit - 20)
                    
            for method_name in list_methods[limit_min:limit_max]:
                try:
                    dict = dict_methods[method_name]
                    list_directive_values = []
                    total_directives = 0
    
                    for directive in list_directives_sorted:
                        # não nos interessa para os valores da planilha
                        if not directive.__contains__('#endif') and not directive.__contains__('#enddebug'):
                            total_directives += dict[directive]
                            list_directive_values.append(dict[directive])
    
    #                writer.writerow([method_name] + list_directive_values + [total_directives] + [dict_features[method_name]] + list_cbr_values)
                    
                    col_count = 0
                    row_count += 1
                    row = sheet.row(row_count)
                    row.write(col_count, method_name)
                    for value in list_directive_values:
                        col_count += 1
                        row.write(col_count, value)
                    row.write(col_count+1, total_directives)
                    row.write(col_count+2, dict_features[method_name])
                    
                except Exception as e:
                    exception = 'Exception (exportDirectivesToXLS): %s' % (e.__str__())
                    print exception
                    self.logErrors('None', exception)
                
            # escrita dos dados estatísticos finais
            sheet_methods = limit_max - limit_min
            
            row = sheet.row(row_count+2)
            row.write(0, 'Total of methods')
            row.write(1, '%d' % (total_methods))
            
            row = sheet.row(row_count+3)
            row.write(0, 'Methods with directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">0")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+4, sheet_methods)))
            
            row = sheet.row(row_count+4)
            row.write(0, 'Methods without directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;"0")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+5, sheet_methods)))
            
            row = sheet.row(row_count+6)
            row.write(0, 'Average of NoDi per method (all methods)')
            row.write(1, xlwt.Formula('AVERAGE(K2:K%d)' % (sheet_methods+1)))
            
            row = sheet.row(row_count+7)
            row.write(0, 'Average of NoDi per method (only methods with directives)')
            row.write(1, xlwt.Formula('SUMIF(K2:K%d, ">0")/COUNTIF(K2:K%d, ">0")' % (sheet_methods+1, sheet_methods+1)))

            row = sheet.row(row_count+9)
            row.write(0, 'Standard Deviation (all methods)')
            row.write(1, xlwt.Formula('STDEV(K2:K%d)' % (sheet_methods+1)))
            
            row = sheet.row(row_count+10)
            row.write(0, 'Standard Deviation (only methods with directives)')
#            row.write(1, xlwt.Formula('(  /(SUM(M2:M%s)-1))' % (total_methods+1, total_methods+1)))

            row = sheet.row(row_count+12)
            row.write(0, 'Methods with one directive')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;"1")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+13, sheet_methods)))
            
            row = sheet.row(row_count+13)
            row.write(0, 'Methods with more than one directive')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">1")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+14, sheet_methods)))
            
            row = sheet.row(row_count+14)
            row.write(0, 'Methods with more than two directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">2")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+15, sheet_methods)))
            
            row = sheet.row(row_count+15)
            row.write(0, 'Methods with more than three directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">3")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+16, sheet_methods)))
            
            row = sheet.row(row_count+16)
            row.write(0, 'Methods with more than four directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">4")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+17, sheet_methods)))
            
            row = sheet.row(row_count+17)
            row.write(0, 'Methods with more than five directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">5")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+18, sheet_methods)))
            
            row = sheet.row(row_count+18)
            row.write(0, 'Methods with more than ten directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">10")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+19, sheet_methods)))
            
            row = sheet.row(row_count+19)
            row.write(0, 'Methods with more than twelve directives')
            row.write(1, xlwt.Formula('COUNTIF(K2:K%d;">20")' % (sheet_methods+1)))
            row.write(2, xlwt.Formula('(B%d/%d)*100' % (sheet_methods+20, sheet_methods)))
                        
        wb.save('directives.xls')
        
        
    def exportDependenciesToXLS(self, dict_decl_coupling, dict_assign_coupling):
        '''
        Exporta o resultado dos acoplamentos para o arquivo dependencies.csv
        '''
        os.chdir(self.project_results_dir)
        
        wb = xlwt.Workbook(encoding="utf-8")
        
        row_limit = 65535
        list_methods = dict_decl_coupling.keys()
        total_methods = len(list_methods)
        number_of_sheets = (total_methods/row_limit) + 1
        
        for x in range(number_of_sheets):
            sheet = wb.add_sheet('dependencies%d' % (x+1))
            
            # cabeçalho
            row_count = 0
            col_count = 0
            row = sheet.row(row_count)
            row.write(col_count, 'Method FQDN')
            row.write(col_count+1, 'NoDDe')
            row.write(col_count+2, 'Vars')
            row.write(col_count+3, 'Features')
            row.write(col_count+4, 'NoADe')
            row.write(col_count+5, 'Vars')
            row.write(col_count+6, 'Features')
            row.write(col_count+7, 'Has dependency?')
            ######
            
            limit_min = x*(row_limit - 20)
            if x == (number_of_sheets - 1):
                limit_max = total_methods
            else:
                limit_max = (x+1)*(row_limit - 20)
            
            for method_name in list_methods[limit_min:limit_max]:
                try:
                    dict_decl = dict_decl_coupling[method_name]
                    list_decl_values = []
                    dict_assign = dict_assign_coupling[method_name]
                    list_assign_values = []
                    
                    for value in dict_decl:
                        list_decl_values.append(dict_decl[value])
                    
                    for value in dict_assign:
                        list_assign_values.append(dict_assign[value])
                        
    #                writer.writerow([method] + list_decl_values)

                    col_count = 0
                    row_count += 1
                    row = sheet.row(row_count)
                    row.write(col_count, method_name)
                    for value_list in list_decl_values:
                        col_count += 1
                        if type(value_list).__name__ != 'list':
                            row.write(col_count, value_list)
                        else:
                            value = ", ".join(value_list)
                            # handle strings with more than 65535 characters (features column in the sheet)
                            if len(value) >= 65535:
                                value = value[0:65535]
                            row.write(col_count, value)
                            
                    for value_list in list_assign_values:
                        col_count +=1
                        if type(value_list).__name__ != 'list':
                            row.write(col_count, value_list)
                        else:
                            value = ", ".join(value_list)
                            # handle strings with more than 65535 characters (features column in the sheet)
                            if len(value) >= 65535:
                                value = value[0:65535]
                            row.write(col_count, value)
                    
                    # marca os métodos que tem algum tipo de dependência
                    row.write(col_count+1, xlwt.Formula('IF(OR(B%d>0;E%d>0);1;0)' % (row_count+1, row_count+1)))
                    
                except Exception as e:
                    exception =  'Exception (exportDependenciesToXLS): %s' % (e.__str__())
                    print exception
                    self.logErrors('None', exception)
                
            # escrita dos dados estatísticos finais
            sheet_methods = limit_max - limit_min
            
            row = sheet.row(row_count+2)
            row.write(0, 'Número de métodos com dependência')
            row.write(1, xlwt.Formula('COUNTIF(H2:H%d, ">0"))' % (sheet_methods+1)))

            wb.save('dependencies.xls')


    def exportDirectivesDataToCSV(self, dict_methods, dict_features):
        '''
        Export directives data to csv file
        '''
        os.chdir(self.project_results_dir)

        # coloca as diretivas em ordem alfabética 
        list_directives_sorted = sorted(Statistics.list_directives)
        
        file_writer = csv.writer(open('directives_data.csv', 'wb'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # cabeçalho
        row = []
        row.append("Method_FQDN")
        for value in list_directives_sorted:
            # não nos interessa para os valores da planilha
            if not value.__contains__('#endif') and not value.__contains__('#enddebug'):
                row.append(value.split(' ')[0])
        row.append("NoDi")
        row.append("NoFE")
        file_writer.writerow(row)
        ######
        
        for method_name in dict_methods.keys():
            try:
                row = []
                row.append(method_name)
                dict = dict_methods[method_name]
                total_directives = 0

                for directive in list_directives_sorted:
                    # não nos interessa para os valores da planilha
                    if not directive.__contains__('#endif') and not directive.__contains__('#enddebug'):
                        total_directives += dict[directive]
                        row.append(dict[directive])
                
                row.append(total_directives)
                row.append(dict_features[method_name])
                file_writer.writerow(row)
                
            except Exception as e:
                exception = 'Exception (exportDirectivesToXLS): %s' % (e.__str__())
                print exception
                self.logErrors('None', exception)
    
    
    def exportDirectivesResultsToCSV(self, dict_methods, dict_features):
        '''
        Export directives results to directives_result.csv file 
        '''
        os.chdir(self.project_results_dir)
        
        file_writer = csv.writer(open('directives_result.csv', 'wb'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # cabeçalho
        row = []
        row.append("ToM")
        row.append("MwD")
        row.append("MwoD")
        row.append("NoDiAVGAll")
        row.append("NoDiAVG")
        row.append("SDAll")
        row.append("SD")
        row.append("M1")
        row.append("Mm1")
        row.append("Mm2")
        row.append("Mm3")
        row.append("Mm4")
        row.append("Mm5")
        row.append("Mm10")
        row.append("Mm20")
        
        file_writer.writerow(row)
        ######
        
        mwd = 0
        mwod = 0
        nodi = []
        nodiall = []
        m1 = 0
        mm1 = 0
        mm2 = 0
        mm3 = 0
        mm4 = 0
        mm5 = 0
        mm10 = 0
        mm20 = 0
        row = []
        header = True
        
        file_reader = csv.reader(open('directives_data.csv', 'rb'), delimiter=';', quotechar='|')
        
        for reader in file_reader:
            if header:
                header = False
            else:
                if int(reader[10]) > 0:
                    mwd += 1
                    nodi.append(int(reader[10]))
                else:
                    mwod += 1
                
                nodiall.append(int(reader[10]))
                
                if int(reader[10]) == 1:
                    m1 += 1
                if int(reader[10]) > 1:
                    mm1 += 1
                if int(reader[10]) > 2:
                    mm2 += 1
                if int(reader[10]) >3:
                    mm3 += 1
                if int(reader[10]) > 4:
                    mm4 += 1
                if int(reader[10]) > 5:
                    mm5 += 1
                if int(reader[10]) > 10:
                    mm10 += 1
                if int(reader[10]) > 20:
                    mm20 += 1
                
        tom = file_reader.line_num - 1
        nodiavgall = numpy.average(nodiall)
        nodiavg = numpy.average(nodi)
        sdall = numpy.std(nodiall)
        sd = numpy.std(nodi)
        
        row.append(tom)
        row.append(mwd)
        row.append(mwod)
        row.append(nodiavgall)
        row.append(nodiavg)
        row.append(sdall)
        row.append(sd)
        row.append(m1)
        row.append(mm1)
        row.append(mm2)
        row.append(mm3)
        row.append(mm4)
        row.append(mm5)
        row.append(mm10)
        row.append(mm20)
        
        file_writer.writerow(row)


    def exportDependenciesToCSV(self, dict_decl_coupling, dict_assign_coupling):
        '''
        Export dependencies results to .csv file
        '''
        os.chdir(self.project_results_dir)
        
        file_writer = csv.writer(open('dependencies.csv', 'wb'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # cabeçalho
        row = []
        row.append("Method_FQDN")
        row.append("Declared_vars")
        row.append("NoDDe")
        row.append("DDe_vars")
        row.append("DDe_features")
        row.append("NoADe")
        row.append("ADe_vars")
        row.append("ADe_features")
        row.append("Has_dependencies")
        
        file_writer.writerow(row)
        ######
        
        list_methods = dict_decl_coupling.keys()
        
        for method_name in list_methods:
            try:
                row = []
                has_dependencies = False
                dict_decl = dict_decl_coupling[method_name]
                dict_assign = dict_assign_coupling[method_name]
                
                row.append(method_name)
                row.append(", ".join(dict_decl['declared']))
                row.append(dict_decl['coupling'])
                row.append(", ".join(dict_decl['vars']))
                row.append(", ".join(dict_decl['features']))
                row.append(dict_assign['coupling'])
                row.append(", ".join(dict_assign['vars']))
                row.append(", ".join(dict_assign['features']))
                if dict_decl['coupling'] > 0 or dict_assign['coupling'] > 0:
                    has_dependencies = True
                                
                # marca os métodos que tem algum tipo de dependência
#                row.write(col_count+1, xlwt.Formula('IF(OR(B%d>0;E%d>0);1;0)' % (row_count+1, row_count+1)))
                if has_dependencies:
                    row.append(1)
                else:
                    row.append(0)
                
                file_writer.writerow(row)
                
            except Exception as e:
                exception =  'Exception (exportDependenciesToXLS): %s' % (e.__str__())
                print exception
                self.logErrors('None', exception)