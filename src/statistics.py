# -*- coding: utf-8 -*-
'''
Created on 17/06/2010

@author: felipe
'''

import os
import csv
import datetime 

#RESULTS_HEADER = 

class Statistics(object):
    '''
    Super class to handle project statistics
    '''
    list_directives = [
                       'ifdef',
                       'ifndef',
                       'elifdef',
                       'elifndef',
                       'if',
                       'elif',
                       'else',
                       'endif',
#                      'condition',
                       'debug',
                       'mdebug',
                       'enddebug',
#                      '#define ',
#                      '#undefine',
#                      '#expand',
                        ]
    
    
    header = ['NoM',
              'MwDi',
              'MwoDi',
              'NoDi',
              'NoFE',
              'NoDiAVGAll',
              'NoDiAVG',
              'NoDiSDAll',
              'NoDiSD',
              'M1',
              'M>1',
              'M>2',
              'M>3',
              'M>4',
              'M>5',
              'M>10',
              'M>20',
              'MwDe',
              'MwoDe',
              'NoDe',
              'NoDeAVGAll',
              'NoDeAVG',
              'NoDeSDAll',
              'NoDeSD',
              ]
    for value in sorted(list_directives):
        if not value.__contains__('#endif') and not value.__contains__('#enddebug'):
            header.append(value.split(' ')[0])
    
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.work_dir = self.project_dir + '/_pl-stats'
        self.xml_dir = self.work_dir + '/xmls'
        self.project_results_dir = self.work_dir + '/results'
        self.prefix_src = ''
        self.prefix_cpp = ''
    
    def logErrors(self, filename, method_name, exception):
        '''
        Creates a log error structure
        '''
        error_dir = self.work_dir + '/error'
        log_file = error_dir + '/log.txt'
        if not os.path.exists(error_dir):
#            os.system('rm -rf %s' % (error_dir))
            os.mkdir(error_dir)
        if not os.path.exists(log_file):
            log_file = open(log_file, 'w')
        else:
            log_file = open(log_file, 'a')

        date_time = datetime.datetime.now()
        if not filename.__contains__('None'):
            os.system("cp %s %s" % (self.work_dir + '/' + filename, error_dir))
        log_file.write('Date and time: %s\nFilename: %s\nMethod name: %s\n\n' % (date_time, filename, method_name))
        log_file.write('%s\n\n' % (str(exception)))
        log_file.write('----------------------------------------------------\n\n')
        log_file.close()


    def getStats(self, function):
        pass


    def _getFunctionTags(self, document):
        '''
        Get <function> or <constructor> tag elements
        '''
        return [f for f in document.getiterator('*') if f.tag == self.prefix_src + 'constructor' or f.tag == self.prefix_src + 'function']

    
    def _getMethodName(self, function):
        '''
        Get method name!
        '''
        return function.findtext(self.prefix_src + 'name')
    
    
    def _getMethodSignature(self, function):
        '''
        Get method signature!
        '''
        signature = ""
        type = function.find(self.prefix_src + 'type')
        for name in type.iter(self.prefix_src + 'name'):
            signature += name.text + ' '
        func_name = function.find(self.prefix_src + 'name')
        signature += func_name.text

        return signature
    
    
    def _getFileName(self, function):
        '''
        Get package name!
        '''
        parent = function.getparent()
        while parent.tag != self.prefix_src + 'unit':
            parent = parent.getparent()

        return parent.attrib['filename']
    
    
    def _checkMethodName(self, method_name, dict_method, method_repeated):
        '''
        Verify if this method has already in method list
        '''
        if method_name in dict_method:
            method_repeated += 1
            method_name += method_repeated.__str__()
            
        return [method_name, method_repeated]
    
    
    def _getElementBlock(self, function):
        '''
        Get <block> element in function
        '''
        block = function.find(self.prefix_src + 'block')
        # Handle THROWS clausule in method signature
        if block is None:
            expr_stmt = function.find(self.prefix_src + 'expr_stmt')
            if expr_stmt is not None:
                expr = expr_stmt.find(self.prefix_src + 'expr')
                block = expr.find(self.prefix_src + 'block')
        return block

    
    def _getMethodParams(self, function):
        '''
        Get variables which are function params
        '''
        aux = ''
        list_params_decl = []
        
        for param in function.iter(self.prefix_src + 'param'):
            dict_param = {}
            try:
                names = [child for child in param.iter(self.prefix_src + 'name') if child.getparent().tag == self.prefix_src + 'decl']
                for name in names:
                    if len(name.getchildren()) == 0:
                        aux = name.text
                    else:
                        subname = name.find(self.prefix_src + 'name')
                        aux = subname.text
                    
                    dict_param[aux] = ('', 'Mandatory')
                    list_params_decl.append(dict_param)
                    
            except Exception as e:
                print "Exception (_getMethodParams): %s" % (e.__str__())

        return list_params_decl
    
    
    def _getVarsDeclared(self, function):
        '''
        Get vars has been declared in function
        '''
        list_vars_declared = []
        stack_feature = []
        
        list_decl_stmt_elements = [decl_stmt for decl_stmt in function.iter(self.prefix_src + 'decl_stmt')]
        block = self._getElementBlock(function)
        
        if block is not None:
            for child in block.getiterator('*'):
                try:
                    if not list_decl_stmt_elements.__contains__(child):
                        # Get current feature
                        if self._isValidDirective(child):
                            directive = child.find(self.prefix_cpp + 'directive')
                            if not self._isEndDirective(directive):
                                if self._isMiddleDirective(directive):
                                    aux = stack_feature.pop()
                                    tuple = (directive.text, '! ' + aux[1])
                                else:
                                    text = ''
                                    expr = child.find(self.prefix_src + 'expr')
                                    if expr is None:
                                        for name in child.getiterator(self.prefix_src + 'name'):
                                            if name.tail is not None:
                                                text += name.text + name.tail
                                            else:
                                                text += name.text
                                    else:
                                        # Can have a method as feature name (ex: #ifdef m())
                                        calls = expr.findall(self.prefix_src + 'call')
                                        if len(calls) > 0:
                                            for call in calls:
                                                text += call.findtext(self.prefix_src + 'name')
                                        elif expr.text is not None:
                                            text = expr.text
                                        else:
                                            text = expr.findtext(self.prefix_src + 'name')
                                    
                                    tuple = (directive.text, text)
                                stack_feature.append(tuple)
                            else:
                                if len(stack_feature) > 0:
                                    stack_feature.pop()
                    else:
                        dict_vars = {}
                        
                        if len(stack_feature) > 0:
                            current_feature = stack_feature[len(stack_feature) - 1]
                        else:
                            current_feature = ('', 'Mandatory')
                        
                        decl = child.find(self.prefix_src + 'decl')
                        name = decl.find(self.prefix_src + 'name')
                        # Can have a <block> tag as <decl> child
                        if name is not None:
                            if name.text is None:
                                name = name.find(self.prefix_src + 'name')
                            
                            dict_vars[name.text] = current_feature
                            list_vars_declared.append(dict_vars)
                        
                except Exception as e:
                    exception = "Exception (_getVarsDeclared): %s" % (e.__str__())
                    print exception
                    self.logErrors(self._getFileName(function), self._getMethodName(function), exception)
#        print dict_vars
        return list_vars_declared
    
    
    def _getVarsUsed(self, function):
        '''
        Get vars has been used in function (in <expr> tag)
        '''
        list_vars_used = []
        stack_feature = []
        
        # Normalizes the list of <expr> elements
        list_expr_elements = [expr for expr in function.iter(self.prefix_src + 'expr')]
        for expr_element in list_expr_elements:
            list_aux = [child for child in expr_element.iter(self.prefix_src + 'expr')]
            if len(list_aux) > 1:
                for element in list_aux[1:]:
                    list_expr_elements.remove(element)
                
        block = self._getElementBlock(function)
        
        if block is not None:
            for child in block.getiterator('*'):
                try:
                    if not list_expr_elements.__contains__(child):
                        # Get current feature
                        if self._isValidDirective(child):
                            directive = child.find(self.prefix_cpp + 'directive')
                            if not self._isEndDirective(directive):
                                if self._isMiddleDirective(directive):
                                    aux = stack_feature.pop()
                                    tuple = (directive.text, '! ' + aux[1])
                                else:
                                    text = ''
                                    expr = child.find(self.prefix_src + 'expr')
                                    if expr is None:
                                        for name in child.getiterator(self.prefix_src + 'name'):
                                            if name.tail is not None:
                                                text += name.text + name.tail
                                            else:
                                                text += name.text
                                    else:
                                        # Can have a method as feature name (ex: #ifdef m())
                                        calls = expr.findall(self.prefix_src + 'call')
                                        if len(calls) > 0:
                                            for call in calls:
                                                text += call.findtext(self.prefix_src + 'name')
                                        elif expr.text is not None:
                                            text = expr.text
                                        else:
                                            text = expr.findtext(self.prefix_src + 'name')
                                    
                                    tuple = (directive.text, text)
                                stack_feature.append(tuple)
                            else:
                                if len(stack_feature) > 0:
                                    stack_feature.pop()
                    else:
                        if len(stack_feature) > 0:
                            current_feature = stack_feature[len(stack_feature) - 1]
                        else:
                            current_feature = ('', 'Mandatory')
                        
                        expr_name_elements = [name for name in child.iter(self.prefix_src + 'name')]
                        # The <expr> tag can have something like: <expr>"a string here"</expr>, whitout <name>
                        if len(expr_name_elements) > 0:
                            var_names = [name.text for name in expr_name_elements]
                            for var in var_names:
                                dict_var = {}
                                dict_var[var] = current_feature
                                list_vars_used.append(dict_var)
                            
                except Exception as e:
                    exception = "Exception (_getVarsUsed): %s" % (e.__str__())
                    print exception
                    self.logErrors(self._getFileName(function), self._getMethodName(function), exception)

        return list_vars_used
    
    
    def _isEndDirective(self, element):
        '''
        Check if element is an #endif or #enddebug
        '''
        dir_name = element.text.split(' ')
        dir_name = dir_name[0].split('\t')
        if dir_name[0] == 'endif' or dir_name[0] == 'enddebug':
            return True
        return False
    
    def _isMiddleDirective(self, element):
        '''
        Check if element is an #else
        '''
        dir_name = element.text.split(' ')
        dir_name = dir_name[0].split('\t')
        if dir_name[0] == 'else':
            return True
        return False
    
    def _isMiddleDeclDirective(self, element):
        '''
        Check if element is an #elif, #elifdef or #elifndef
        '''
        dir_name = element.text.split(' ')
        dir_name = dir_name[0].split('\t')
        if dir_name[0] == 'elif' or dir_name[0] == 'elifdef' or dir_name[0] == 'elifndef':
            return True
        return False

    
    def _isValidDirective(self, element):
        '''
        Check if element tag is a valid directive
        '''
        if element.tag.startswith(self.prefix_cpp) and element.tag != self.prefix_cpp + 'directive' \
            and element.tag != self.prefix_cpp + 'define' and element.tag != self.prefix_cpp + 'undef' \
            and element.tag != self.prefix_cpp + 'file' and element.tag != self.prefix_cpp + 'pragma' \
            and element.tag != self.prefix_cpp + 'error' and element.tag != self.prefix_cpp + 'line' \
            and element.tag != self.prefix_cpp + 'include':
            return True
        return False
    
    
    def _getNumberOfDirectives(self, function):
        '''
        Get the occurrence of <directive> in a <function>
        '''
        dict_directives = {}
        for directive in self.list_directives:
            dict_directives[directive] = 0
            
        for child in function.iter(self.prefix_cpp + 'directive'):
            try:
                dir_name = child.text.split(' ')
                dir_name = dir_name[0].split('\t')
                if dir_name[0] in dict_directives:
                    dict_directives[dir_name[0]] += 1
            except Exception as e:
                exception = "Exception (_getNumberOfDirectives): %s" % (e.__str__())
                print exception
                self.logErrors(self._getMethodName(function), exception)

        return dict_directives
    
    
    def _getNumberOfFeatures(self, function):
        '''
        Get the number of features in function
        '''
        list_features = []
        block = self._getElementBlock(function)
        
        if block is not None:
            for child in block.iter(self.prefix_cpp + 'directive'):
                try:
                    parent = child.getparent()
                    if self._isValidDirective(parent) and not self._isEndDirective(child):
                        aux = ''
                        name = parent.findtext(self.prefix_src + 'name')
                        if name is None:
                            # Check if is an #else directive
                            if self._isMiddleDirective(child):
                                aux = list_features[len(list_features) - 1]
                                aux = '! ' + aux
                            else:
                                expr = parent.find(self.prefix_src + 'expr')
                                if expr is None:
                                    for name in parent.getiterator(self.prefix_src + 'name'):
                                        if name.tail is not None:
                                            aux += name.text + name.tail
                                        else:
                                            aux += name.text
                                else:
                                    # Can have a method as feature name (ex: #ifdef m())
                                    calls = expr.findall(self.prefix_src + 'call')
                                    if len(calls) > 0:
                                        for call in calls:
                                            aux += call.findtext(self.prefix_src + 'name')
                                    elif expr.text is not None:
                                            text = expr.text
                                    else:
                                        aux = expr.findtext(self.prefix_src + 'name')
                        else:
                            aux = name

                        list_features.append(aux)
                except Exception as e:
                    exception = "Exception (_getNumberOfFeatures): %s" % (e.__str__())
                    print exception
                    self.logErrors(self._getFileName(function), self._getMethodName(function), exception)
                
        return len(list(set(list_features)))


    def _getDeclDependencies(self, function):
        '''
        Computes 'declaration <-> use' dependencies' type in a method
        '''
        list_dependencies = []
        # Get function params
        list_params = self._getMethodParams(function)
        # Get vars declared in function
        list_vars_declared = self._getVarsDeclared(function)
        # Get vars used
        list_vars_used = self._getVarsUsed(function)

        for dict_var_param in list_params:
            var_param = dict_var_param.keys()[0]
            value_param = dict_var_param[var_param]
            for dict_var_used in list_vars_used:
                var_used = dict_var_used.keys()[0]
                value_used = dict_var_used[var_used]
                if var_used == var_param:
                    if value_used[1] != value_param[1]:
                        dict_dependency = {}
                        dict_dependency[var_param] = [dict_var_param[var_param], dict_var_used[var_used]]
                        list_dependencies.append(dict_dependency)
    
        for dict_var_declared in list_vars_declared:
            var_declared = dict_var_declared.keys()[0]
            value_declared = dict_var_declared[var_declared]
            for dict_var_used in list_vars_used:
                var_used = dict_var_used.keys()[0]
                value_used = dict_var_used[var_used]
                if var_used == var_declared:
                    if value_used[1] != value_declared[1]:
                        dict_dependency = {}
                        dict_dependency[var_declared] = [dict_var_declared[var_declared], dict_var_used[var_used]]
                        list_dependencies.append(dict_dependency)

#        print len(list_dependencies)
        return list_dependencies
    
    
    def _getMethodLOC(self, method_fqdn):
        '''
        Get the Method LoC of function
        '''
        count = 0
        next = ''
        
        file = method_fqdn.split('.')
        filename = file[0]
        method_name = file[1]
        with open(os.path.join(self.xml_dir, filename + '.xml'), 'rb') as file_opened:
            for line in file_opened:
                try:
                    # Check function name
                    if line.__contains__('<name>%s</name>' % (method_name)) and line.__contains__('<parameter_list>'):
                        next = line
                        while not next.__contains__('<block>{'):
                            next = file_opened.next()

                        while not next.__contains__('</block></function>'):
                            next = file_opened.next()
                            if not next.__contains__('</block></function>'):
                                next = next.strip()
                                # Handle comment lines
                                if next.startswith('<comment'):
                                    while not next.__contains__('</comment>'):
                                        next = file_opened.next()
                                # Handle blank lines
                                elif next != '':
                                    count += 1

                        break
        
                except Exception as e:
                    count = 0
                    exception = "Exception (_getMethodLOC): %s" % (e.__str__())
                    print exception
#                    self.logErrors(filename + '.c', method_name, exception)
                    
#        print count
        return count
                    
                    
    def _isMethodSignature(self, line, method_signature, method_name):
        '''
        Check if there is a method signature in line
        '''
        if line.__contains__(method_signature):
            return True
        elif not line.__contains__(';') and not line.__contains__('=') and \
                not line.__contains__('/*') and not line.__contains__('//') and not line.__contains__('*/') and \
                line.split('(')[0].strip() == method_name:
            return True
        
        return False
    
    
    def _getMethodLOF(self, method_fqdn):
        '''
        Get the Method LoF of function
        '''
        count = 0
        next = ''
        
        file = method_fqdn.split('.')
        filename = file[0]
        method_name = file[1]
        with open(os.path.join(self.xml_dir, filename + '.xml'), 'rb') as file_opened:
            for line in file_opened:
                try:
                    # Check function name
                    if line.__contains__('<name>%s</name>' % (method_name)) and line.__contains__('<parameter_list>'):
                        next = line
                        while not next.__contains__('<block>{'):
                            next = file_opened.next()

                        while not next.__contains__('</block></function>'):
                            next = file_opened.next()
                            if not next.__contains__('</block></function>'):
                                next = next.strip()
                                # Handle directive occurrence
                                if next.startswith('<cpp:') and not next.__contains__('<cpp:endif>') and \
                                        not next.__contains__('<cpp:define>') and not next.__contains__('<cpp:undef>') and \
                                        not next.__contains__('<cpp:file>') and not next.__contains__('<cpp:pragma>') and \
                                        not next.__contains__('<cpp:error>') and not next.__contains__('<cpp:line>') and \
                                        not next.__contains__('<cpp:include>'):
                                    next = file_opened.next()
                                    while not next.__contains__('<cpp:endif>'):
                                        next = next.strip()
                                        if next.__contains__('<cpp:else') or next.__contains__('<cpp:elif') or \
                                                next.__contains__('<cpp:elifdef') or next.__contains__('<cpp:elifndef'):
                                            next = file_opened.next()
                                            next = next.strip()
                                        # Handle comment lines
                                        if next.startswith('<comment'):
                                            while not next.__contains__('</comment>'):
                                                next = file_opened.next()
                                        elif next != '':
                                            count += 1
                                        next = file_opened.next()

                        break
                    
                except Exception as e:
                    count = 0
                    exception = "Exception (_getMethodLOF): %s" % (e.__str__())
                    print exception
#                    self.logErrors(filename + '.c', method_name, exception)
#        print count
        return count
    
    
    def exportDataToCSV(self, dict_data):
        '''
        Export data to CSV
        '''
        os.chdir(self.project_results_dir)
        file_writer = csv.writer(open('data.csv', 'wb'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # Header
        row = []
        row.append("Method_FQDN")
        row.append('MLoC')
        row.append('MLoF')
        row.append("NoDi")
        for directive in sorted(Statistics.list_directives):
            if not directive.__contains__('endif') and not directive.__contains__('enddebug'):
                row.append('#' + directive)
        row.append("NoFE")
        row.append("NoDe")
        for directive in sorted(Statistics.list_directives):
            if not directive.__contains__('endif') and not directive.__contains__('enddebug'):
                row.append('#' + directive)
                
        file_writer.writerow(row)
        ######
        
        for file in sorted(dict_data):
            dict_method = dict_data[file]
            for method in sorted(dict_method):
                row = []
                list_nodi_aux = []
                list_node_aux = []
                dict_aux = {}
                for directive in sorted(Statistics.list_directives):
                    if not directive.__contains__('endif') and not directive.__contains__('enddebug'):
                        dict_aux[directive] = 0
                # Set method name
                method_fqdn = file + '.' + method
                row.append(method_fqdn)
                dict_metric = dict_method[method]
                # Set NoDi metrics
                nodi = dict_metric['NoDi']
                # Set MLoC metric
                row.append(dict_metric['MLoC'])
                # Set MLoF metric
                row.append(dict_metric['MLoF'])
                for value in sorted(nodi):
                    if not value.__contains__('endif') and not value.__contains__('enddebug'):
                        list_nodi_aux.append(nodi[value])
                row.append(sum(list_nodi_aux))
                # Set NoFE metric
                row += list_nodi_aux
                row.append(dict_metric['NoFE'])
                # Set NoDe metrics
                list_node = dict_metric['NoDe']
                row.append(len(list_node))
                for dict_node_aux in list_node:
                    for key, list_value in dict_node_aux.items():
                        for tuple in list_value:
                            if tuple[0] != '':
#                                print tuple
                                dict_aux[tuple[0]] += 1
                for key in sorted(dict_aux):
                    list_node_aux.append(dict_aux[key])
                row += list_node_aux
                
                file_writer.writerow(row)
