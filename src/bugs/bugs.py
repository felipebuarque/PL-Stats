# -*- coding: utf-8 -*-
'''
Created on 21/01/2011

@author: felipe
'''
import xlrd, xlwt
import urllib2
from BeautifulSoup import BeautifulSoup
import os

FLAG_HAS_DIRECTIVE = 'has #ifdef'

CRITERIA_HAS_IFDEF = 'has #ifdefs'
CRITERIA_HAS_CONDITIONAL_COMPILATION = 'has "conditional compilation" words'
CRITERIA_HAS_DIRECTIVE = 'has "directive" word'
CRITERIA_HAS_ATTACHMENT = 'has attachment'

class BugReport(object):
    '''
    Read project sheets and find references in bug reports
    '''
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.project_name = 'Apache+httpd-2'
        self.project_target = ''
        self.project_results_dir = self.project_dir + '_pl-stats/results/'
        self.directive_sheet = self.project_results_dir + 'directives.xls'
        self.coupling_sheet = self.project_results_dir + 'dependencies.xls'
        self.bug_reports = ['https://issues.apache.org/bugzilla/', #Apache+httpd-2
                            'https://bugzilla.kernel.org/',
                            'http://gcc.gnu.org/bugzilla/',
                            'https://bugzilla.gnome.org/',
                            'http://bugs.ghostscript.com/',
                            'http://bugzilla.mplayerhq.hu/', #MPlayer
                            'https://defect.opensolaris.org/bz/',
                            ]
        self.bug_criteria = {CRITERIA_HAS_IFDEF: True,
                             CRITERIA_HAS_CONDITIONAL_COMPILATION: True,
                             CRITERIA_HAS_DIRECTIVE: True,
                             CRITERIA_HAS_ATTACHMENT: True}

    def testNumberOfUnderlines(self):
        '''
        '''
        list = []
        count_underline = 0
        count_dependence_underline = 0
        book = xlrd.open_workbook(self.coupling_sheet)
        sheet = book.sheet_by_index(0)
        
        for row in range(sheet.nrows)[1:sheet.nrows - 2]:
            dep_vars = ""
            dec_coup_count = sheet.cell(rowx=row, colx=1).value
            assign_coup_count = sheet.cell(rowx=row, colx=4).value
            
            fqdn = sheet.cell(rowx=row, colx=0).value
            fqdn = fqdn.split('.')
            filename = fqdn[0]
            method_name = fqdn[1]
            list.append(method_name)
            
            if method_name.__contains__('_'):
                count_underline += 1
                
                if dec_coup_count != 0 or assign_coup_count != 0:
                    count_dependence_underline += 1
        
        print 'Total de métodos: %d' % (len(list))
        print 'Métodos com "_": %d - %.2f' % (count_underline, (float(count_underline)/float(len(list)))*100)
        print 'Métodos com dependência e "_": %d - %.2f' % (count_dependence_underline, (float(count_dependence_underline)/float(len(list)))*100)

    def getMethodsFromSheets(self):
        '''
        Read the dependencies sheet_dependencies and return a dict {fqdn: [variables]}
        '''
        dict_methods = {}
        list_methods_with_ifdefs = []
        
        book_directives = xlrd.open_workbook(self.directive_sheet)
        sheet_directives = book_directives.sheet_by_index(0)
        book_dependencies = xlrd.open_workbook(self.coupling_sheet)
        sheet_dependencies = book_dependencies.sheet_by_index(0)
        
        # Get methods with #ifdef (from directives sheet)
        for rownum in range(sheet_directives.nrows)[1:sheet_directives.nrows - 19]:
            fqdn = sheet_directives.cell(rowx=rownum, colx=0).value
            aux = fqdn.split('.')
            method_name = aux[1]
            
            if method_name.__contains__('_'):
                has_ifdef = sheet_directives.cell(rowx=rownum, colx=10).value
                if has_ifdef != 0:
                    list_methods_with_ifdefs.append(fqdn)
        
        # Get methods with dependencies (from dependencies sheet)
        for rownum in range(sheet_dependencies.nrows)[1:sheet_dependencies.nrows - 2]:
            dep_vars = ""
            dec_coup_count = sheet_dependencies.cell(rowx=rownum, colx=1).value
            assign_coup_count = sheet_dependencies.cell(rowx=rownum, colx=4).value
            fqdn = sheet_dependencies.cell(rowx=rownum, colx=0).value
            aux = fqdn.split('.')
            method_name = aux[1]
            
            if method_name.__contains__('_'):
                if dec_coup_count != 0 or assign_coup_count != 0:
                    # get declare coupling vars
                    dec_vars = sheet_dependencies.cell(rowx=rownum, colx=2).value
                    # get assignment coupling vars
                    assign_vars = sheet_dependencies.cell(rowx=rownum, colx=5).value
                    # set the dictionary with a list of declare and coupling vars
                    dep_vars = dec_vars + assign_vars
                    dep_vars = dep_vars.split(', ')
                    dep_vars = list(set(dep_vars))
                
                dict_methods[fqdn] = dep_vars
        
        for fqdn in list_methods_with_ifdefs:
            if type(dict_methods[fqdn]).__name__ != 'list':
                dict_methods[fqdn] = FLAG_HAS_DIRECTIVE
            
        return dict_methods
    
    def bugsCount(self):
        '''
        Return the number of bugs for each method
        '''
        url = self.bug_reports[0]
        # Simple search
        #url += 'buglist.cgi?query_format=specific&order=relevance+desc&bug_status=__all__&product=%s&content=%s'
        
        # Advanced search
        url += 'buglist.cgi?type0-1-0=matches&query_format=advanced&value0-1-0="%s"&field0-1-0=content&field0-0-0=content&type0-0-0=matches&value0-0-0="%s"&product=%s'
        
        dict_methods = self.getMethodsFromSheets()
        total_methods = len(dict_methods)
        
        # Counters
        methods_count = 0
        bugs_in_methods_with_dependencies = 0
        bugs_in_methods_without_dependencies = 0
        count_methods_with_dependencies = 0
        count_methods_without_dependencies = 0
        count_methods_with_bugs = 0
        total_bugs = 0
        ######
        
        dict_methods_with_bugs = {}
        
        print ''
        print 'TOTAL OF METHODS: %d' % (total_methods)
        print ''

        for fqdn,vars in dict_methods.items():
            try:
#                if methods_count == 120: break

                aux = fqdn.split('.')
                filename = aux[0] + '.c'
                method_name = aux[1]

                methods_count += 1
                bugs_count = 0
                list_bugs_ids = []
                
                # Set the url with parameters and request
                # Simple search
                # query = url % (self.project_name, '"%s.c"%%2B"%s"' % (filename, method_name))
                
                # Advanced search
                query = url % (method_name, filename, self.project_name)

                response = urllib2.urlopen(query)
                page = response.read()
                response.close()
                
                soup = BeautifulSoup(page)
                
                # Verify if page contains 'Zarro' string
                result = soup.find(attrs={'class': 'bz_result_count'})
                list_result = [i.string for i in result.contents if i.string.__contains__('Zarro')]
                
                if len(list_result) > 0:
                    print '%d - %s.%s: ZARRO boogs found!' % (methods_count, filename, method_name)
                else:
                    count_methods_with_bugs += 1
                    
                    result = result.contents[0].lstrip()
                    result = result.split(' ')
                    bugs_count = result[0]
                    
                    if bugs_count == 'One':
                        bugs_count = 1
                        bugs_name = 'boog'
                    else:
                        bugs_count = int(bugs_count)
                        bugs_name = 'boogs'

                    print '%d - %s: %d %s found!' % (methods_count, fqdn, bugs_count, bugs_name)
                    
                    # Get the list of bugs IDs
                    bugs_id_reference = soup.findAll(attrs={'class': 'first-child bz_id_column'})
                    list_bugs_ids = [bug.find('a').string for bug in bugs_id_reference]
                    
                total_bugs += bugs_count
                
                # Verify if is a method with dependencies
                if type(vars).__name__ == 'list':
                    count_methods_with_dependencies += 1
                    bugs_in_methods_with_dependencies += bugs_count
                    # Assign the bugs ids to method
                    if bugs_count > 0:
                        dict_methods_with_bugs[fqdn] = list_bugs_ids
                else:
                    count_methods_without_dependencies += 1
                    bugs_in_methods_without_dependencies += bugs_count
            
            except Exception as e:
                print 'Exception (bugsCount): %s' % (e.__str__())
        
        print ''
        print 'Methods with boogs: %d' % (count_methods_with_bugs)
        print 'Methods without boogs: %d' % (total_methods - count_methods_with_bugs)
        print ''
        print 'Boogs in methods with dependencies: %d' % (bugs_in_methods_with_dependencies)
        print 'Boogs in methods without dependencies: %d' % (bugs_in_methods_without_dependencies)
        print ''
        print 'TOTAL OF BOOGS: %d' % (total_bugs)
        print ''
        
        return bugs_in_methods_with_dependencies, bugs_in_methods_without_dependencies, count_methods_with_dependencies, \
                count_methods_without_dependencies, count_methods_with_bugs, dict_methods, dict_methods_with_bugs


    def checkBugs(self, dict_methods_with_dependencies):
        '''
        Check if dependencies are related with method bugs
        '''
        condition = ""
        for fqdn,bugs_ids in dict_methods_with_dependencies.items():
            if self.bug_criteria[CRITERIA_HAS_IFDEF]:
                pass
            
            if self.bug_criteria[CRITERIA_HAS_CONDITIONAL_COMPILATION]:
                pass
            
            if self.bug_criteria[CRITERIA_HAS_DIRECTIVE]:
                pass
            
            if self.bug_criteria[CRITERIA_HAS_ATTACHMENT]:
                pass


    def exportBugsCountToXLS(self, bugs_in_methods_with_dependencies, bugs_in_methods_without_dependencies, \
                             methods_with_dependencies, methods_without_dependencies, count_methods_with_bugs, \
                             dict_methods, dict_methods_with_bugs):
        '''
        Export bug report results to xls spreadsheet
        '''
        total_methods = methods_with_dependencies + methods_without_dependencies
        total_bugs = bugs_in_methods_with_dependencies + bugs_in_methods_without_dependencies
        
        os.chdir(self.project_results_dir)
        try:
            wb = xlwt.Workbook(encoding="utf-8")
            sheet = wb.add_sheet("bug results")
            
            # cabeçalho
            row_count = 0
            col_count = 0
            row = sheet.row(row_count)
            row.write(col_count+1, 'Methods')
            row.write(col_count+2, '%')
            row.write(col_count+3, 'Bugs in methods')
            row.write(col_count+4, '%')
            ###
            
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'With dependencies')
            row.write(col_count+1, '%d' % (methods_with_dependencies))
            row.write(col_count+2, '%.2f' % ((float(methods_with_dependencies)/float(total_methods))*100))
            row.write(col_count+3, '%d' % (bugs_in_methods_with_dependencies))
            row.write(col_count+4, '%.2f' % ((float(bugs_in_methods_with_dependencies)/float(total_bugs))*100))
            
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'Without dependencies')
            row.write(col_count+1, '%d' % (methods_without_dependencies))
            row.write(col_count+2, '%.2f' % ((float(methods_without_dependencies)/float(total_methods))*100))
            row.write(col_count+3, '%d' % (bugs_in_methods_without_dependencies))
            row.write(col_count+4, '%.2f' % ((float(bugs_in_methods_without_dependencies)/float(total_bugs))*100))
            
            row_count += 2
            row = sheet.row(row_count)
            row.write(col_count, 'Total')
            row.write(col_count+1, '%d' % (total_methods))
            row.write(col_count+3, '%d' % (total_bugs))
            
            row_count += 1
            row = sheet.row(row_count)
            row.write(col_count, 'With bugs')
            row.write(col_count+1, '%d' % (count_methods_with_bugs))
            
            row_count += 3
            row = sheet.row(row_count)
            row.write(col_count, 'Methods')
            row.write(col_count+1, 'Has dependencies?')
            row.write(col_count+2, 'Has #ifdefs?')
            row.write(col_count+3, 'Bugs IDs')

            for fqdn,vars in dict_methods.items():
                has_dependencies = "N"
                has_ifdefs = "N"
                ids = ""
                row_count += 1
                row = sheet.row(row_count)
                row.write(col_count, fqdn)
                if type(dict_methods[fqdn]).__name__ == 'list':
                    has_dependencies = 'Y'
                if has_dependencies == 'Y' or dict_methods[fqdn] == FLAG_HAS_DIRECTIVE:
                    has_ifdefs = 'Y'
                if dict_methods_with_bugs.keys().__contains__(fqdn):
                    ids = ", ".join(dict_methods_with_bugs[fqdn])
                row.write(col_count+1, has_dependencies)
                row.write(col_count+2, has_ifdefs)
                row.write(col_count+3, ids)
                
            row_count += 3
            row = sheet.row(row_count)
            row.write(col_count, "Total")
            row.write(col_count+1, xlwt.Formula('COUNTIF(B10:B%d, "Y")' % (len(dict_methods)+9)))
            row.write(col_count+2, xlwt.Formula('COUNTIF(C10:C%d, "Y")' % (len(dict_methods)+9)))
            row.write(col_count+3, xlwt.Formula('COUNTIF(D10:D%d, "<>"&" ")' % (len(dict_methods)+9)))
            
            wb.save('bugs.xls')
        except Exception as e:
            print 'Exception (exportBugsCountToXLS): ' + e.__str__()

#dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/MPlayer-1.0rc2/'
dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/httpd-2.2.17/'
#dir = '/home/felipe/Dropbox/FSE/sheets/results/httpd-2.2.17/'
b = BugReport(dir)
#b.testNumberOfUnderlines()
bmwd, bmwod, mwd, mwod, mwb, methods, methods_with_bugs = b.bugsCount()
b.exportBugsCountToXLS(bmwd, bmwod, mwd, mwod, mwb, methods, methods_with_bugs)
