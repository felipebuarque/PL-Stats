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
    Classe responsável por gerar as estatísticas do pl-stats para projetos em C
    '''
    def __init__(self, project_dir, src_dir, work_dir, results_dir):
        super(StatisticsC, self).__init__(project_dir, src_dir, work_dir, results_dir)
        self.prefix_src = '{http://www.sdml.info/srcML/src}'
        self.prefix_cpp = '{http://www.sdml.info/srcML/cpp}'
    
    def getStatistics(self):
        '''
        Retorna uma lista contendo:
            - Um dicionário com o número de #ifdefs por método
            - Um dicionário com o número de acoplamentos do tipo decl<->uso por método
            - Um dicionário com o número de acoplamentos do tipo atr<->uso por método
            - O número total de métodos do projeto
        '''
        method_name = ''
        dict_methods = {}
        dict_directive_metrics = {}
        dict_features = {}
        dict_cbr = {}
        dict_vsoc = {}
        dict_coupling_du = {}
        dict_coupling_au = {}
        parser = etree.XMLParser(remove_blank_text=True, huge_tree=True)
        
        os.chdir(self.xml_dir)
        for file in os.listdir(self.xml_dir):
            try:
                document = etree.parse(file, parser)
            except Exception as e:
                exception = 'Exception (getStatistics): %s' % (e.__str__())
                print exception
                self.logErrors('None', exception)
                       
            # pega o nome do pacote da função
            pack_name = self._getPackageName(document)
            
            # pega o nome do arquivo sem '.c'
            filename = file.split('.')
            file_name = filename[0] + '.'
            print file_name + 'c'

            # pega as tags <class>
            # cl = document.find('class')
            
            # pega as tags <function>
            functions = self._getFunctionTags(document)
            
            method_repeated = 0
            for func in functions:
                try:
                    # pega o nome do método
                    method_name = self._getMethodName(file_name, pack_name, func)
                    
                    # verifica se o método já existe na lista de métodos e modifica o nome (caso exista)
                    method_name, method_repeated = self._checkMethodName(dict_methods, method_name, method_repeated)
                    
                    # pega o número de #ifdefs por método e adiciona no dicionário dict_directive_metrics
                    for directive in Statistics.list_directives:
                        dict_directive_metrics[directive] = self.__getDirectiveOccur(func, directive)
                    dict_methods[method_name] = dict_directive_metrics
                    
                    # pega as features do método
                    dict_features[method_name] = len(self.__getFeatureOccur(func))
                    
                    # pega o número de CBRs no método
    #                dict_cbr[method_name] = self.__getCBROccur(func)
                    
                    # pega o número de features VSoC
    #                dict_vsoc[method_name] = self.__getVSoCOccur(func)
    
                    # pega a métrica de acoplamento do tipo declaração<->uso
                    count_coupling, list_vars_decl, list_vars, list_features = self.__getDeclCouplingOccur(func)
                    dict_coupling = {'coupling': count_coupling, 'declared': list_vars_decl, 'vars': list_vars, 'features': list_features}
                    dict_coupling_du[method_name] = dict_coupling
                    
                    # pega a métrica de acoplamento do tipo atribuição<->uso
                    count_coupling, list_vars, list_features = self.__getAssignCouplingOccur(func)
                    dict_coupling = {'coupling': count_coupling, 'vars': list_vars, 'features': list_features}
                    dict_coupling_au[method_name] = dict_coupling
                    
    #                print dict_coupling_du[method_name]
    #                print dict_coupling_au[method_name]
    
                    dict_directive_metrics = {}
                    dict_coupling = {}
                    
                except Exception as e:
                    print method_name
                    exception = "Exception (getStatistics): %s" % (e.__str__())
                    print exception
#                    self.logErrors(filename[0], exception)
        
        return [dict_methods, dict_features, dict_cbr, dict_vsoc, dict_coupling_du, dict_coupling_au]
    
    def __getDirectiveOccur(self, function, directive):
        '''
        Retorna o número de ocorrências da diretiva <directive> em um método <function>
        '''
        aux = directive.split(' ')
        dir = aux[0].split('#')
        dir_count = 0

        for child in function.iter(self.prefix_cpp + 'directive'):
            dir_name = child.text.split(' ')
            dir_name = dir_name[0].split('\t')
            if dir_name[0] == dir[1]:
                dir_count += 1

        return dir_count
    
    def __getFeatureOccur(self, function):
        '''
        Retorna o número de Features em um dado método
        '''
        list_features = []
        
        for child in function.iter(self.prefix_cpp + 'directive'):
            parent = child.getparent()
            type = child.text
            if not self._isEndDirective(type) and \
                not self._isMiddleDirective(type) and \
                parent.tag != self.prefix_cpp + 'error' and \
                parent.tag != self.prefix_cpp + 'pragma' and \
                type != 'define' and type != 'undef' and type != 'include' and type != 'file' and type != 'line':
                name = parent.findtext(self.prefix_src + 'name')
#                print parent.tag
                aux = ''
                if name is None:
                    expr = parent.find(self.prefix_src + 'expr')
                    if expr is None:
                        for name in expr.getiterator(self.prefix_src + 'name'):
                            if name.tail is not None:
                                aux += name.text + name.tail
                            else:
                                aux += name.text
                    else:
                        aux = expr.text

                if not list_features.__contains__(aux):
                    list_features.append(aux)
        
        return list_features
    
    def __getCBROccur(self, function):
        '''
        Retorna o número de ocorrência para as cláusulas Continue, Break e Return
        dentro de #ifdefs
        '''
        stack_directive = []
        c_count = 0
        b_count = 0
        r_count = 0
        
        block = function.find(self.prefix_src + 'block')
        # pode haver uma cláusula THROWS na assinatura do método
        if block is None:
            expr_stmt = function.find(self.prefix_src + 'expr_stmt')
            expr = expr_stmt.find(self.prefix_src + 'expr')
            block = expr.find(self.prefix_src + 'block')
        
        # varre todas as tags dentro de <block>
        for child in block.getiterator('*'):
            # se for uma diretiva, coloca ou retira da pilha
            if child.tag == self.prefix_src + 'directive':
                stack_directive = self.__stackDirective(stack_directive, child)
                continue
            
            # pega o número de tags <continue>
            if child.tag == self.prefix_src + 'continue' and len(stack_directive) > 0:
                c_count += 1
            
            # pega o número de tags <break>
            if child.tag == self.prefix_src + 'break' and len(stack_directive) > 0:
                b_count += 1
        
            # pega o número de tags <return>
            if child.tag == self.prefix_src + 'return' and len(stack_directive) > 0:
                r_count += 1
            
        return {'Continue': c_count, 'Break': b_count, 'Return': r_count}
    
    def __getDeclCouplingOccur(self, function):
        '''
        Retorna o número de acoplamentos do tipo 'declaração <-> uso' 
        em um determinado método
        '''
        count = 0
        list_feature_coupling = []
        dict_decl = {}
        stack_directive = []
        list_var_assign = []
        list_var_coupling = []
        list_vars_decl = []
        list_all_vars = []
        
        # pega as variáveis passadas como parâmetro do método
        dict_param_decl = self._getParamVarDeclared(function)
        
        block = function.find(self.prefix_src + 'block')
        # pode haver uma cláusula THROWS na assinatura do método
        if block is None:
            expr_stmt = function.find(self.prefix_src + 'expr_stmt')
            if expr_stmt is not None:
                expr = expr_stmt.find(self.prefix_src + 'expr')
                block = expr.find(self.prefix_src + 'block')
        
        if block is not None:
            # varre todas as tags dentro de <block>
            for child in block.getiterator('*'):
                # se for uma diretiva, coloca ou retira da pilha
                if child.tag.startswith(self.prefix_cpp) and child.tag != self.prefix_cpp + 'directive' \
                    and child.tag != self.prefix_cpp + 'define' and child.tag != self.prefix_cpp + 'undef' \
                    and child.tag != self.prefix_cpp + 'file' and child.tag != self.prefix_cpp + 'pragma' \
                    and child.tag != self.prefix_cpp + 'error':
                    stack_directive = self.__stackDirective(stack_directive, child)
                    continue
                
                # se for uma declaração, coloca a variável declarada no dicionário
                elif child.tag == self.prefix_src + 'decl_stmt':
                    list_vars_decl, dict_decl, stack_directive = self._getVarDeclared(list_vars_decl, dict_decl, stack_directive, child)
                    # checa se uma variável está sendo usada em uma declaração
                    # verifica em qual feature a atribuição está contida
                    assign_feature = self._checkFeature(stack_directive)
                    
                    exprs = child.getiterator(self.prefix_src + 'expr')
                    for expr in exprs:
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        
                        # checa o acoplamento para variáveis utilizadas em uma atribuição
                        count, list_var_coupling, list_feature_coupling = self._checkDeclCoupling(assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
                        
                # calcula o acoplamento em uma atribuição
                elif child.tag == self.prefix_src + 'expr_stmt':
                    expr = child.find(self.prefix_src + 'expr')
                    # erro quando ocorre <expr_stmt> aninhados
                    if expr is not None:
                        # pega os nomes das variáveis de uma atribuição
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        
                        # verifica em qual feature a atribuição está contida
                        assign_feature = self._checkFeature(stack_directive)
                        
                        # checa o acoplamento para variáveis utilizadas em uma atribuição
                        count, list_var_coupling, list_feature_coupling = self._checkDeclCoupling(assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
                        
                # calcula o acoplamento em estruturas condicionais e loop
                elif child.tag == self.prefix_src + 'if' \
                    or child.tag == self.prefix_src + 'while' \
                    or child.tag == self.prefix_src + 'for' \
                    or child.tag == self.prefix_src + 'switch':
                    condition = child.find(self.prefix_src + 'condition')
                    expr = condition.find(self.prefix_src + 'expr')
                    if expr is not None:
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        # verifica em qual feature a atribuição está contida
                        assign_feature = self._checkFeature(stack_directive)
                        
                        # checa o acoplamento para variáveis utilizadas em uma atribuição
                        count, list_var_coupling, list_feature_coupling = self._checkDeclCoupling(assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
            
            list_all_vars = list_vars_decl + dict_param_decl.keys()
        
        return [count, list_all_vars, list_var_coupling, list_feature_coupling]
    
    def __getAssignCouplingOccur(self, function):
        '''
        Retorna o número de acoplamentos do tipo 'atribuição <-> uso' 
        em um determinado método
        '''
        count = 0
        list_feature_coupling = []
        dict_decl = {}
        stack_directive = []
        list_var_assign = []
        list_var_coupling = []
        
        block = function.find(self.prefix_src + 'block')
        
        if block is not None:
            
            childs = block.getiterator('*')
            # varre todas as tags dentro de <block>
            for child in childs:
                # se for uma diretiva, coloca ou retira da pilha
                if child.tag.startswith(self.prefix_cpp) and child.tag != self.prefix_cpp + 'directive' \
                    and child.tag != self.prefix_cpp + 'define' and child.tag != self.prefix_cpp + 'undef' \
                    and child.tag != self.prefix_cpp + 'file':
                    stack_directive = self.__stackDirective(stack_directive, child)
                    continue
                
                # se for uma declaração, verifica se houve atribuição e checa o acoplamento
                elif child.tag == self.prefix_src + 'decl_stmt':
                    assign_feature = self._checkFeature(stack_directive)
                    
                    exprs = child.getiterator(self.prefix_src + 'expr')
                    for expr in exprs:
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        
                        # checa o acoplamento para variáveis utilizadas na atribuição
                        count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
                        
                # calcula o acoplamento em uma atribuição
                elif child.tag == 'expr_stmt':
                    expr = child.find(self.prefix_src + 'expr')
                    # erro quando ocorre <expr_stmt> aninhados
                    if expr is not None:
                        # pega os nomes das variáveis de uma atribuição
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        
                        # verifica em qual feature a atribuição está contida
                        assign_feature = self._checkFeature(stack_directive)
                        
                        # checa o acoplamento para variáveis utilizadas em uma atribuição
                        count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
                        
                # calcula o acoplamento em estruturas condicionais e loop
                elif child.tag == self.prefix_src + 'if' \
                    or child.tag == self.prefix_src + 'while' \
                    or child.tag == self.prefix_src + 'for' \
                    or child.tag == self.prefix_src + 'switch':
                    condition = child.find(self.prefix_src + 'condition')
                    expr = condition.find(self.prefix_src + 'expr')
                    if expr is not None:
                        expr_names = expr.getiterator(self.prefix_src + 'name')
                        call = expr.find(self.prefix_src + 'call')
                        list_var_assign = self._getExprVars(expr_names, call)
                        # verifica em qual feature a atribuição está contida
                        assign_feature = self._checkFeature(stack_directive)
                        
                        # checa o acoplamento para variáveis utilizadas em uma atribuição
                        count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
        
        return [count, list_var_coupling, list_feature_coupling]
    
    def __getVSoCOccur(self, function):
        '''
        Retorna o número de features VSoC em um determinado método
        '''
        stack_directive = []
        count = 0
        
        block = function.find(self.prefix_src + 'block')
        # pode haver uma cláusula THROWS na assinatura do método
        if block is None:
            expr_stmt = function.find(self.prefix_src + 'expr_stmt')
            expr = expr_stmt.find(self.prefix_src + 'expr')
            block = expr.find(self.prefix_src + 'block')
        
        # varre todas as tags dentro de <block>
        for child in block.getiterator('*'):
            # se for uma diretiva, coloca ou retira da pilha
            if child.tag == self.prefix_src + 'directive':
                if len(stack_directive) == 0:
                    count += 1
                stack_directive = self.__stackDirective(stack_directive, child)
                
        return count
        
    def __stackDirective(self, stack_directive, child):
        
        d_child = child.find(self.prefix_src + 'name')
        aux = ''
        if d_child is not None:
            aux = d_child.text
        else:
            expr = child.find(self.prefix_src + 'expr')
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

        # pode possuir uma 'endDirective' que foi aberta fora do método
        if self._isEndDirective(child.findtext(self.prefix_cpp + 'directive')) and len(stack_directive) > 0:
            stack_directive.pop()
        elif not self._isEndDirective(child.findtext(self.prefix_cpp + 'directive')) and \
            not self._isMiddleDirective(child.findtext(self.prefix_cpp + 'directive')) and \
            not self._isMiddleDeclDirective(child.findtext(self.prefix_cpp + 'directive')):
            stack_directive.append(aux)
        elif self._isMiddleDeclDirective(child.findtext(self.prefix_cpp + 'directive')):
            stack_directive.pop()
            stack_directive.append(aux)

        return stack_directive