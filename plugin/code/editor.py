# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 08:53:15 2019

@author: nipa
"""

import wx
import wx.lib.dialogs
import wx.stc as stc
import os
import model_prediction
import numpy as np

faces = {
        'times' : 'Times New Roman',
        'mono'  : 'Courier New',
        'helv'  : 'Arial',
        'other' : 'Comic Sans MS',
        'size'  : 13,
        'size2' : 8,
 }

class Car:
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, id, model, make, year):
        """Constructor"""
        self.id = id
        self.model = model
        self.make = make
        self.year = year       
 


class MainWindow(wx.Frame):
    def __init__(self, parent, title, style):
        self.dirname = ''
        self.filename = ''
        self.lineNumberEnabled = True
        self.leftMarginWidth = 25
        
        wx.Frame.__init__(self, parent, title = title, size=(800, 600))
        self.control = stc.StyledTextCtrl(self, style = wx.TE_MULTILINE | wx.TE_WORDWRAP )
        super(MainWindow, self).__init__(parent)
        
        
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        
        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5,0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)
        
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))
        
        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "New", "Create a new document")
        menuOpen = filemenu.Append(wx.ID_OPEN, "Open", "Open an existing document")
        menuSave = filemenu.Append(wx.ID_SAVE, "Save", "Save the current document")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save As", "Save a new document")
        filemenu.AppendSeparator()
        
        menuClose = filemenu.Append(wx.ID_EXIT, "Close", "Close the application")
        
        
        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "Undo", "Undo last action")
        menuRedo = editmenu.Append(wx.ID_OPEN, "Redo", "Redo last action")
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "Select All", "Select the entire document")
        menuCopy = editmenu.Append(wx.ID_COPY, "Copy", "Copy selected text")
        menuCut = editmenu.Append(wx.ID_CUT, "Cut", "Cut selected text")
        menuPaste = editmenu.Append(wx.ID_PASTE, "Paste", "Paste copied text")
        
        
        prefmenu = wx.Menu()
        menuLineNumber = prefmenu.Append(wx.ID_ANY, "Toggle line number", "Show/Hide line number")
        
        helpmenu = wx.Menu()
        menuHowTo = helpmenu.Append(wx.ID_ANY, "How to ...", "Get help using the editor")
        helpmenu.AppendSeparator()
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "About", "Read about the editor and it's making")
        
        
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")
        menuBar.Append(editmenu, "Edit")
        menuBar.Append(prefmenu, "Preferences")
        menuBar.Append(helpmenu, "Help")
        self.SetMenuBar(menuBar)
       
        	
        self.panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 
		
        self.text = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE | wx.TE_WORDWRAP) 
         
        self.predictions = [' ', ' ', ' ']   
        self.lst = wx.ListBox(self.panel, size = (100,-1), choices = self.predictions, style = wx.LB_SINGLE)
		
        box.Add(self.lst,0,wx.EXPAND) 
        box.Add(self.text, 1, wx.EXPAND) 
		
        self.panel.SetSizer(box) 
        self.panel.Fit() 
		
        self.Centre() 
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst) 
        self.Bind(wx.EVT_CHAR, self.OnCharEvent)
        
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)
        
        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        
        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLineNumber)
        
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        
        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineColumn)
        self.text.Bind(wx.EVT_CHAR, self.OnCharEvent)
        
        
        self.Show()
        
        
    def OnNew(self, e):
        self.filename = ''
        print("Hello new")
        self.control.SetValue('')
        
    def OnOpen(self, e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        print("Hello from open")
        if(dlg.ShowModal() == wx.ID_OK):
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename),'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
            
            
    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w', encoding = 'utf-8')
            f.write(self.text.GetValue())
            print(self.text.Getvalue())
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as",self.dirname, "Untitled","*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if(dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.text.GetValue())
                    print(self.text.GetValue())
                    f.close()
                dlg.Destroy()
                
            except:
                pass
        
    def OnSaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                
            if(dlg.ShowModal()==wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w', encoding = 'utf-8')
                f.write(self.text.GetValue())
                print(self.text.GetValue())
                f.close()
            dlg.Destroy()
            
        except:
            pass
            
    def OnClose(self, e):
        self.Destroy()
        self.Close(True)
         
         
     
    def OnUndo(self, e):
        self.control.Undo()
    
    def OnRedo(self, e):
        self.control.Redo()
        
    def OnSelectAll(self, e):
        self.control.SelectAll()
        
    def OnCopy(self, e):
        self.control.Copy()
        
    def OnCut(self, e):
        self.control.Cut()
        
    def OnPaste(self, e):
        self.control.Paste()
        
       
    def OnToggleLineNumbers(self, e):
        if(self.lineNumberEnabled):
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = True
        
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True
            
    def OnHowTo(self, e):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "This is how to", "How to use the ")
        dlg.ShowModal()
        print("Hello from how to")
        dlg.Destroy()
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(None, 'About', 'My advanced text editor for Bangla writing', wx.OK)
        #print("Hello from about")
        dlg.ShowModal()
        dlg.Destroy()
        
    def UpdateLineColumn(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line %s, Column %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)
        
    def OnCharEvent(self, e):
        keycode = e.GetKeyCode()
        altDown = e.AltDown()
        
        print(self.text.GetValue())
        
        self.text.AppendText(chr(keycode))
        
        #print(keycode)
        
        if (keycode == 32):
            resultValue = model_prediction.generate_text(self.text.GetValue(), 1,  model_prediction.max_sequence_len)
            #print(self.predictions)
            resultValue = np.array(resultValue)
            #print(resultValue)
            self.predictions = resultValue
            self.lst.Set(resultValue)
            #print("I'm here")
            

		
    def onListBox(self, event): 
        self.text.AppendText(event.GetEventObject().GetStringSelection() + " ")
        #resultValue = model_prediction.generate_text(self.text.GetValue(),0,  model_prediction.max_sequence_len)
        #print(self.predictions)
        
   
app = wx.App()
frame = MainWindow(None, "My text editor", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)  
app.MainLoop()
del app

