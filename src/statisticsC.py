# -*- coding: utf-8 -*-
'''
Created on 20/11/2010

@author: felipe
'''
from statistics import Statistics

import os
from lxml import etree

class StatisticsC(Statistics):
    '''
    Handle statistics for C projects
    '''
    def __init__(self, project_dir):
        super(StatisticsC, self).__init__(project_dir)
        self.prefix_src = '{http://www.sdml.info/srcML/src}'
        self.prefix_cpp = '{http://www.sdml.info/srcML/cpp}'
    
    
    def getStatistics(self):
        '''
        Return a statistical dictionary with the follow structure:
            {file: {method: {'NoDi': ..., 'NoFE': ..., 'NoDe': ...}, method...}, file...}
        '''
        parser = etree.XMLParser(remove_blank_text=True, huge_tree=True)
        
        dict_file = {}
        dict_metric = {}
        dict_method = {}
        
        method_name = ''
        
        for file in os.listdir(self.xml_dir):
            try:
                document = etree.parse(os.path.join(self.xml_dir, file), parser)
            except Exception as e:
                exception = 'Exception (getStatistics): %s' % (e.__str__())
                print exception
                self.logErrors('None', 'None', exception)
            
            # Get filename whitout ".c"
            filename = file.split('.')
            file_name = filename[0] + '.'
            print file_name + 'c'
            
            # Get <function> tags
            functions = self._getFunctionTags(document)
            
            method_repeated = 0
            for function in functions:
                try:
                    # Get method name
                    method_name = self._getMethodName(function)
                    
                    # Check if method was overheaded and renames it
                    method_name, method_repeated = self._checkMethodName(method_name, dict_method, method_repeated)
#                    print file_name + method_name
                    
                    # Get the number of #ifdefs in method <method_name>
                    dict_metric['NoDi'] = self._getNumberOfDirectives(function)
                    
                    # Get number of features in function 
                    dict_metric['NoFE'] = self._getNumberOfFeatures(function)

                    # Get dependencies of type decl<->use
                    dict_metric['NoDe'] = self._getDeclDependencies(function)
                    
                    # Get method loc (MLoC)
                    dict_metric['MLoC'] = self._getMethodLOC(file_name + method_name)
                    
                    # Get method lof (MLoF)
                    dict_metric['MLoF'] = self._getMethodLOF(file_name + method_name)

                    dict_method[method_name] = dict_metric
                    dict_metric = {}
                    
                except Exception as e:
                    print method_name
                    exception = "Exception (getStatistics): %s" % (e.__str__())
                    print exception
                    self.logErrors(self._getFileName(function), method_name, exception)
            
            dict_file[filename[0]] = dict_method
            dict_method = {}
        
        return dict_file

    
    

        
    def __stackDirective(self, element, stack_directive, stack_feature_expression):
        '''
        Put or pop directives and feature expressions in/from respective stacks
        '''
        d_child = element.find(self.prefix_src + 'name')
        aux = ''
        if d_child is not None:
            aux = d_child.text
        else:
            expr = element.find(self.prefix_src + 'expr')
            if expr is not None:
                if expr.text is not None:
                    aux = expr.text

                names = expr.findall(self.prefix_src + 'name')
                if len(names) > 0:
                    for name in names:
                        aux += name.text
                        if name.tail is not None:
                            aux += name.tail
                else:
                    calls = expr.findall(self.prefix_src + 'call')
                    for call in calls:
                        name = call.find(self.prefix_src + 'name')
                        aux += name.text + '('
                        arguments = call.getiterator(self.prefix_src + 'argument')
                        for argument in arguments:
                            names = argument.getiterator(self.prefix_src + 'name')
                            for name in names:
                                aux += name.text
                                if name.tail is not None:
                                    aux += name.tail
                        aux += ')'
                        if call.tail is not None:
                            aux += call.tail

        directive = element.findtext(self.prefix_cpp + 'directive')
        # pode possuir uma 'endDirective' que foi aberta fora do método
        if self._isEndDirective(directive) and len(stack_feature_expression) > 0:
            stack_directive.pop()
            stack_feature_expression.pop()
        elif not self._isEndDirective(directive) and not self._isMiddleDirective(directive) and not self._isMiddleDeclDirective(directive):
            stack_directive.append(directive)
            stack_feature_expression.append(aux)
        elif self._isMiddleDeclDirective(directive):
            stack_directive.pop()
            stack_directive.append(directive)
            stack_feature_expression.pop()
            stack_feature_expression.append(aux)
        elif self._isMiddleDirective(directive):
            stack_directive.pop()
            stack_directive.append(directive)
            stack_feature_expression.pop()
            stack_feature_expression.append('! ' + aux)

        return stack_directive, stack_feature_expression