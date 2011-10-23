# -*- coding: utf-8 -*-
'''
Created on 20/11/2010

@author: felipe
'''
from statistics import Statistics

import os
import xml.etree.ElementTree as ET
from lxml import etree

class StatisticsJava(Statistics):
    '''
    Handle statistics for Java projects
    '''
    def __init__(self, project_dir):
        super(StatisticsJava, self).__init__(project_dir)
        self.prefix_src = ''
        self.prefix_cpp = 'cpp-'

    
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
            
            # Get filename whitout ".java"
            filename = file.split('.')
            file_name = filename[0] + '.'
            print file_name + 'java'
            
            # Get <function> tags
            functions = self._getFunctionTags(document)
            
            method_repeated = 0
            for function in functions:
                try:
                    # Change directive tags
                    self.__changeCommentTags(document, file, function)
                    
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
#                    self.logErrors(filename[0], exception)
            
            dict_file[filename[0]] = dict_method
            dict_method = {}
        
        return dict_file
    
    
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
                                if next.startswith('<cpp-') and not next.__contains__('<cpp-endif>') and \
                                        not next.__contains__('<cpp-define>') and not next.__contains__('<cpp-undef>') and \
                                        not next.__contains__('<cpp-file>') and not next.__contains__('<cpp-pragma>') and \
                                        not next.__contains__('<cpp-error>') and not next.__contains__('<cpp-line>') and \
                                        not next.__contains__('<cpp-include>'):
                                    next = file_opened.next()
                                    while not next.__contains__('<cpp-endif>'):
                                        next = next.strip()
                                        if next.__contains__('<cpp-else') or next.__contains__('<cpp-elif') or \
                                                next.__contains__('<cpp-elifdef') or next.__contains__('<cpp-elifndef'):
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
    
    
    def __changeCommentTags(self, document, file, function):
        '''
        Change XML tags if comments are directives
        '''
        block = self._getElementBlock(function)
        
        if block is not None:
            try:
                for comment in block.iter(self.prefix_src + 'comment'):
                    for directive in self.list_directives:
                        if comment.text.__contains__('#') and comment.text.__contains__(directive):
                            aux = comment.text.split('//')
                            # We can have: // // // // #mdebug
                            aux = aux[len(aux)-1].strip()
                            if not aux.__contains__('{') and not aux.__contains__('}'):
                                aux = aux.split('#')
                                list_type = aux[1].split(' ')
                                
                                comment.tag = self.prefix_cpp + list_type[0]
                                comment.text = '#'
                                comment.attrib.clear()
                                
                                cpp_directive = etree.SubElement(comment, self.prefix_cpp + 'directive', attrib={})
                                cpp_directive.text = list_type[0]
                                
                                if len(list_type) > 1:
                                    name = ET.SubElement(comment, 'name', attrib={})
                                    name.text = ''
                                    for expression in list_type[1:]:
                                        name.text += expression
                                     
                out_file = open(os.path.join(self.xml_dir, file), 'w')
                document.write(out_file)
            
            except Exception as e:
                exception = "Exception (__changeCommentTags): %s" % (e.__str__())
                print exception
            
    
    
    def __stackDirective(self, child, stack_directive, stack_feature_expression):
        '''
        Put or pop directives and feature expressions in/from respective stacks
        '''
        directive = child.findtext('type')
        feature_expression = child.findtext('decl')
        # pode possuir uma 'endDirective' que foi aberta fora do método
        if self._isEndDirective(directive) and len(stack_feature_expression) > 0:
            stack_directive.pop()
            stack_feature_expression.pop()
        elif not self._isEndDirective(directive) and not self._isMiddleDirective(directive) and not self._isMiddleDeclDirective(directive):
            stack_directive.append(directive)
            stack_feature_expression.append(feature_expression)
        elif self._isMiddleDeclDirective(directive):
            stack_directive.pop()
            stack_directive.append(directive)
            stack_feature_expression.pop()
            stack_feature_expression.append(feature_expression)

        return stack_directive, stack_feature_expression