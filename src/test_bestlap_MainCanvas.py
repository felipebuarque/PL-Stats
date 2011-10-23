# -*- coding: utf-8 -*-
'''
Created on 13/09/2010

@author: felipe
'''
import unittest
import os, xlrd
from statistics import Statistics


class CheckDirectiveMainCanvas(unittest.TestCase):
    '''
    Classe responsável pelos testes do script
    '''
    def setUp(self):
        '''
        Carrega os dados da classe Screen que estão na planilha
        '''
        results_dir = '/home/felipe/workspace-msc/pl-stats-TEST/_pl-stats/results/'
        os.chdir(results_dir)
        rb = xlrd.open_workbook('directives.xls')
        self.sheet = rb.sheet_by_name('directives')
    
    def testHideNotify(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.hideNotify':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testChangeScreen1(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.changeScreen1':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testCreateScreens(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.createScreens':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testIsLoading(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.isLoading':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
    
    def testProccessKeyReleases(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.proccessKeyReleases':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
    
    def testLoadTrackSelectionMenuResources(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.loadTrackSelectionMenuResources':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
    
    def testKeyReleased(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.keyReleased':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 2)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 2)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 1)
                    break
            break
        
    def testKeyPressed(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.keyPressed':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 3)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 3)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 2)
                    break
            break
        
    def testPopScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.popScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testGetKeyStates(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.getKeyStates':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testPauseCurrentScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.pauseCurrentScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testGetScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.getScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testShowNotify(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.showNotify':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testGetNextStackIndex(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.getNextStackIndex':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testGoBack(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.goBack':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 1)
                    break
            break
        
    def testGetLastStackIndex(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.getLastStackIndex':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testMainCanvas(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.MainCanvas':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 3)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 5)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 4)
                    break
            break
        
    def testKillThread(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.killThread':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testUpdate(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.update':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 1)
                    break
            break
        
    def testGetCurrentScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.getCurrentScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testShowMenu(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.showMenu':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testFreeTrackSelectionMenuResources(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.freeTrackSelectionMenuResources':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testResumeCurrentScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.resumeCurrentScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testHideMenu(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.hideMenu':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testchangeScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.changeScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break
        
    def testPaint(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.paint':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 2)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 1)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 3)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 2)
                    break
            break
        
    def testPushScreen(self):
        for col_index in range(self.sheet.ncols):
            for row_index in range(self.sheet.nrows):
                if self.sheet.cell(row_index, col_index).value == 'com.meantime.j2me.MainCanvas.pushScreen':
                    self.assertEqual(self.sheet.cell(row_index, col_index+1).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+2).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+3).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+4).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+5).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+6).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+7).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+8).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+9).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+10).value, 0)
                    self.assertEqual(self.sheet.cell(row_index, col_index+11).value, 0)
                    break
            break

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()