# -*- coding: utf-8 -*-
'''
Created on 20/11/2010

@author: felipe
'''
from statistics import Statistics

import os, sys
import xml.etree.ElementTree as ET
from lxml import etree

class StatisticsJava(Statistics):
    '''
    Classe responsável por gerar as estatísticas do pl-stats para projetos em Java
    '''
    def __init__(self, project_dir, src_dir, work_dir, results_dir):
        super(StatisticsJava, self).__init__(project_dir, src_dir, work_dir, results_dir)

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
        parser = etree.XMLParser(remove_blank_text=True)
        
        os.chdir(self.xml_dir)
        for file in os.listdir(self.xml_dir):
            try:
                document = etree.parse(file, parser)
            except Exception as e:
                print e
                sys.exit(-1)
                       
            # pega o nome do pacote da função
            pack_name = self._getPackageName(document)
            
            # pega o nome do arquivo sem '.java'
            filename = file.split('.')
            file_name = filename[0] + '.'
            print file_name + 'java'

            # pega as tags <class>
            cl = document.find('class')
            
            # pega as tags <function>
            functions = self.__getFunctionTags(document)
            
            method_repeated = 0
            for func in functions:
                # pega o nome do método
                method_name = self._getMethodName(file_name, pack_name, func)
                
                # verifica se o método já existe na lista de métodos e modifica o nome (caso exista)
                method_name, method_repeated = self._checkMethodName(dict_methods, method_name, method_repeated)
                
                # modifica as tags de comentário que são diretivas de compilação
                self.__changeCommentTags(func)
                document.write(file)
                
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
                coupling, list_vars_decl, list_vars, list_features = self.__getDeclCouplingOccur(func)
                dict_coupling = {'coupling': coupling, 'declared': list_vars_decl, 'vars': list_vars, 'features': list_features}
                dict_coupling_du[method_name] = dict_coupling
                
                # pega a métrica de acoplamento do tipo atribuição<->uso
                coupling, list_vars, list_features = self.__getAssignCouplingOccur(func)
                dict_coupling = {'coupling': coupling, 'vars': list_vars, 'features': list_features}
                dict_coupling_au[method_name] = dict_coupling
                
#                print dict_coupling_du[method_name]
#                print dict_coupling_au[method_name]

                dict_directive_metrics = {}
                dict_coupling = {}
        
        return [dict_methods, dict_features, dict_cbr, dict_vsoc, dict_coupling_du, dict_coupling_au]
    
    def __changeCommentTags(self, function):
        '''
        Altera as tags do XML onde os comentários são diretivas
        '''
#        comments = function.getiterator('comment')
        for comment in function.iter('comment'):
            for directive in Statistics.list_directives:
                if comment.text.__contains__(directive):
                    aux = comment.text.split('#')
                    dir = aux[1].split(' ')
                    comment.tag = 'directive'
                    comment.text = '#'
                    comment.attrib.clear()
                    type = etree.SubElement(comment, 'type', attrib={})
                    type.text = dir[0]
                    if len(dir) > 1:
                        decl = ET.SubElement(comment, 'decl', attrib={})
                        decl.text = ''
                        for feature in dir[1:]:
                            decl.text += feature
    
    def __getFunctionTags(self, document):
        '''
        Retorna uma lista de elementos de tag <function>
        '''
        return [f for f in document.getiterator('*') if f.tag == 'constructor' or f.tag == 'function']
        # um arquivo .java pode vir sem a tag <class>
#        if class_tag is not None:
#            block = class_tag.find('block')
#            return [f for f in block.iterchildren() if f.tag == 'constructor' or f.tag == 'function']
    
    def __getDirectiveOccur(self, function, directive):
        '''
        Retorna o número de ocorrências da diretiva <directive> em um método <function>
        '''
        aux = directive.split(' ')
        dir = aux[0].split('#')
        dir_count = 0

        for child in function.iter('directive'):
            dir_name = child.findtext('type').split(' ')
            dir_name = dir_name[0].split('\t')
            if dir_name[0] == dir[1]:
                dir_count += 1

        return dir_count
    
    def __getFeatureOccur(self, function):
        '''
        Retorna o número de Features em um dado método
        '''
        list_features = []
        for child in function.iter('directive'):
            type = child.findtext('type').split(' ')
            type = type[0].split('\t')
            if not self._isEndDirective(type[0]) and \
                not self._isMiddleDirective(type[0]):
                decl = child.findtext('decl').split('\t')
                if not list_features.__contains__(decl[0]):
                    list_features.append(decl[0])
        
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
        # pode possuir uma 'endDirective' que foi aberta fora do método
        if self._isEndDirective(child.findtext('type')) and len(stack_directive) > 0:
            stack_directive.pop()
        elif not self._isEndDirective(child.findtext('type')) and not self._isMiddleDirective(child.findtext('type')) and not self._isMiddleDeclDirective(child.findtext('type')):
            stack_directive.append(child.findtext('decl'))
        elif self._isMiddleDeclDirective(child.findtext('type')):
            stack_directive.pop()
            stack_directive.append(child.findtext('decl'))

        return stack_directive

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
                
        block = function.find('block')
        # pode haver uma cláusula THROWS na assinatura do método
        if block is None:
            expr_stmt = function.find('expr_stmt')
            expr = expr_stmt.find('expr')
            block = expr.find('block')

        # varre todas as tags dentro de <block>
        for child in block.getiterator('*'):
            # se for uma diretiva, coloca ou retira da pilha
            if child.tag == 'directive':
                stack_directive = self.__stackDirective(stack_directive, child)
                continue
            
            # se for uma declaração, coloca a variável declarada no dicionário
            elif child.tag == 'decl_stmt':
                list_vars_decl, dict_decl, stack_directive = self._getVarDeclared(list_vars_decl, dict_decl, stack_directive, child)
                # checa se uma variável está sendo usada em uma declaração
                # verifica em qual feature a atribuição está contida
                assign_feature = self._checkFeature(stack_directive)
                
                for expr in child.iter('expr'):
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
                    list_var_assign = self._getExprVars(expr_names, call)
                    
                    # checa o acoplamento para variáveis utilizadas em uma atribuição
                    count, list_var_coupling, list_feature_coupling = self._checkDeclCoupling(assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
            
            # calcula o acoplamento em uma atribuição
            elif child.tag == 'expr_stmt':
                expr = child.find('expr')
                # erro quando ocorre <expr_stmt> aninhados
                if expr is not None:
                    # pega os nomes das variáveis de uma atribuição
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
                    list_var_assign = self._getExprVars(expr_names, call)
                    
                    # verifica em qual feature a atribuição está contida
                    assign_feature = self._checkFeature(stack_directive)
                    
                    # checa o acoplamento para variáveis utilizadas em uma atribuição
                    count, list_var_coupling, list_feature_coupling = self._checkDeclCoupling(assign_feature, dict_decl, dict_param_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)

            # calcula o acoplamento em estruturas condicionais e loop
            elif child.tag =='if' or child.tag == 'while' or \
                child.tag == 'for' or child.tag == 'switch':
                condition = child.find('condition')
                expr = condition.find('expr')
                if expr is not None:
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
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
        dict_param_decl = {}
        stack_directive = []
        list_var_assign = []
        list_var_coupling = []
        
        block = function.find('block')
        # pode haver uma cláusula THROWS na assinatura do método
        if block is None:
            expr_stmt = function.find('expr_stmt')
            expr = expr_stmt.find('expr')
            block = expr.find('block')
        # varre todas as tags dentro de <block>
        for child in block.getiterator('*'):
            # se for uma diretiva, coloca ou retira da pilha
            if child.tag == 'directive':
                stack_directive = self.__stackDirective(stack_directive, child)
                continue
            
            # se for uma declaração, verifica se houve atribuição e checa o acoplamento
            elif child.tag == 'decl_stmt':
                assign_feature = self._checkFeature(stack_directive)
                
                exprs = child.getiterator('expr')
                for expr in exprs:
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
                    list_var_assign = self._getExprVars(expr_names, call)
                    
                    # checa o acoplamento para variáveis utilizadas na atribuição
                    count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
                    
            # calcula o acoplamento em uma atribuição
            elif child.tag == 'expr_stmt':
                expr = child.find('expr')
                # erro quando ocorre <expr_stmt> aninhados
                if expr is not None:
                    # pega os nomes das variáveis de uma atribuição
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
                    list_var_assign = self._getExprVars(expr_names, call)
                    
                    # verifica em qual feature a atribuição está contida
                    assign_feature = self._checkFeature(stack_directive)
                    
                    # checa o acoplamento para variáveis utilizadas em uma atribuição
                    count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)
            
            # calcula o acoplamento em estruturas condicionais e loop
            elif child.tag =='if' or child.tag == 'while' or \
                child.tag == 'for' or child.tag == 'switch':
                condition = child.find('condition')
                expr = condition.find('expr')
                if expr is not None:
                    expr_names = expr.getiterator('name')
                    call = expr.find('call')
                    list_var_assign = self._getExprVars(expr_names, call)
                    # verifica em qual feature a atribuição está contida
                    assign_feature = self._checkFeature(stack_directive)
                    
                    # checa o acoplamento para variáveis utilizadas em uma atribuição
                    count, dict_decl, list_var_coupling, list_feature_coupling = self._checkAssignCoupling(assign_feature, dict_decl, list_var_assign, count, list_var_coupling, list_feature_coupling)

        return [count, list_var_coupling, list_feature_coupling]
    
    def __appendVarAssigned(self, dict_assign, stack_directive, child):
        '''
        Coloca no dicionário as variáveis utilizadas em uma atribuição
        '''
        # pega as variáveis em ambos os lados da atribuição
        expr = child.find('expr')
        vars = expr.findall('name')
        if len(stack_directive) > 0:
            for var in vars:
                if var.text not in dict_assign:
                    dict_assign[var.text] = stack_directive.pop()
                    stack_directive.append(dict_assign[var.text])
        else:
            for var in vars:
                if var.text not in dict_assign:
                    dict_assign[var.text] = 'Mandatory'
        
        # pega as variáveis que são parâmetros de método numa atribuição
        arguments = expr.getiterator('argument')
        for arg in arguments:
            arg_names = arg.getiterator('name')
            if len(stack_directive) > 0:
                for arg_name in arg_names:
                    if arg_name.text not in dict_assign:
                        dict_assign[arg_name.text] = stack_directive.pop()
                        stack_directive.append(dict_assign[arg_name.text])
            else:
                for arg_name in arg_names:
                    if arg_name.text not in dict_assign:
                        dict_assign[arg_name.text] = 'Mandatory'
        
        return [dict_assign, stack_directive]
    
    def __getParamExprVars(self, arguments):
        '''
        Retorna uma lista das variáveis utilizadas como parâmetro de método
        em uma atribuição
        '''
        list_vars = []
        aux = ''
        for arg in arguments:
            expr = arg.find('expr')
            if expr is not None:
                names = expr.getiterator('name')
                for name in names:
                    if name.text is not None and not self._isBooleanNullVar(name):
                        if name.tail is not None and name.tail == '.':
                            aux += name.text + name.tail
                            continue
                        else:
                            aux += name.text
                            list_vars.append(aux)
                            aux = ''

#        print list_vars
        return list_vars