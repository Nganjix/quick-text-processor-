#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Starlord
#
# Created:     26/06/2016
# Copyright:   (c) Starlord 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import os
import wx.richtext as rc
try:
    from agw import flatnotebook as fnb
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as fnb
import EnhancedStatusBar as ESB
class quicktext(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,'Quick Text Processor V2', pos=(40,40), size=(1200, 800))
        if os.path.exists('.\qt.png'):
            path = os.path.abspath(".\qt.png")
            icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainsizer)
        self.book = fnb.FlatNotebook(self, wx.ID_ANY, agwStyle=fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NODRAG|fnb.FNB_NO_X_BUTTON|fnb.FNB_BOTTOM)

        self.mainsizer.Add(self.book, 1, wx.EXPAND|wx.ALL)
        self.mainpanel = wx.Panel(self.book, -1)
        self.book.AddPage(self.mainpanel, 'Format Text')
        self.mainpaneltwo = wx.Panel(self.book, -1)
        self.book.AddPage(self.mainpaneltwo,'Compare Records' )
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.initSecondWindow)
        self.toppanel = wx.Panel(self.mainpanel, -1, size= (-1, 40))
        self.middlepanel= wx.Panel(self.mainpanel, -1, size = (-1, -1))
        self.mainvsizer = wx.BoxSizer(wx.VERTICAL)

        self.processbtn = wx.Button(self.toppanel, -1, 'Process', size=(100, 30))
        self.duplibtn = wx.Button(self.toppanel, -1, 'Clear Duplicates', size=(100, 30))
        self.clearbtn = wx.Button(self.toppanel, -1, 'Clear', size=(100, 30))


        toppanelsizer= wx.BoxSizer(wx.HORIZONTAL)

        self.choicelist = ['Apostrophe','Comma','Space']
        self.radiochoice = wx.RadioBox(self.toppanel, -1, "", (450, 50),(400, 50), self.choicelist, 3, wx.RA_SPECIFY_COLS)
        self.toppanel.Bind(wx.EVT_RADIOBOX,self.setChoice ,self.radiochoice)

        self.toppanel.Bind(wx.EVT_BUTTON, self.processInfo, id=self.processbtn.GetId())
        self.toppanel.Bind(wx.EVT_BUTTON, self.clearInfo, id=self.clearbtn.GetId())
        self.toppanel.Bind(wx.EVT_BUTTON, self.removeDuplicates, id=self.duplibtn.GetId())


        self.inputbox = rc.RichTextCtrl(self.middlepanel, size =(100, -1), style=wx.VSCROLL)
        self.outputbox = rc.RichTextCtrl(self.middlepanel, size = (-1, -1), style=wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH|wx.TE_RICH2)


        toppanelsizer.Add(self.processbtn, 0, wx.EXPAND | wx.TOP|wx.RIGHT|wx.LEFT, 5)
        toppanelsizer.Add(self.duplibtn, 0, wx.EXPAND | wx.TOP|wx.RIGHT, 5)
        toppanelsizer.Add(self.clearbtn, 0, wx.EXPAND | wx.RIGHT | wx.TOP, 5)
        toppanelsizer.Add(self.radiochoice, 0, wx.EXPAND | wx.LEFT, 50)
        self.toppanel.SetSizer(toppanelsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.inputbox, 0, wx.EXPAND | wx.ALL, 3)
        hsizer.Add(self.outputbox, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 3)
        self.middlepanel.SetSizer(hsizer)

        self.mainvsizer.Add(self.toppanel, 0, wx.EXPAND|wx.ALL, 3)
        self.mainvsizer.Add(self.middlepanel, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 3)
        self.mainpanel.SetSizer(self.mainvsizer)

        self.statusbar = ESB.EnhancedStatusBar(self, -1)
        self.statusbar.SetSize((-1, 25))

        self.statusbar.SetFieldsCount(5)
        self.SetStatusBar(self.statusbar)
        self.statusbar.SetStatusWidths([200, 150, 160,130, -1])

        self.gauge = wx.Gauge(self.statusbar, -1, 50, style = wx.GA_PROGRESSBAR)
        self.statictext = wx.StaticText(self.statusbar, -1, '  Waiting fot input .....')
        self.statictext1 = wx.StaticText(self.statusbar, -1, '')
        self.statictext2 = wx.StaticText(self.statusbar, -1, '')
        self.statictext3 = wx.StaticText(self.statusbar, -1, '')
        statusbarchildren = self.statusbar.GetChildren()

        self.statusbar.AddWidget(self.gauge,ESB.ESB_EXACT_FIT, ESB.ESB_EXACT_FIT, 3)
        self.statusbar.AddWidget(self.statictext,ESB.ESB_EXACT_FIT, ESB.ESB_EXACT_FIT, 0)
        self.statusbar.AddWidget(self.statictext1,ESB.ESB_EXACT_FIT, ESB.ESB_EXACT_FIT, 1)
        self.statusbar.AddWidget(self.statictext2,ESB.ESB_EXACT_FIT, ESB.ESB_EXACT_FIT, 2)
        self.statusbar.AddWidget(self.statictext3,ESB.ESB_ALIGN_LEFT, ESB.ESB_ALIGN_CENTER_VERTICAL, 4)

        self.choice = 'Apostrophe'
        self.statictext1.SetLabel('  In apostrophe mode .....')
    def initSecondWindow(self, event):
        self.secsizer = wx.BoxSizer(wx.VERTICAL)
        self.sectoppanel = wx.Panel(self.mainpaneltwo, -1, (-1, 50))
        self.secmidpanel = wx.Panel(self.mainpaneltwo, -1, (-1, -1))
        self.setStaticText1('   In comparison mode.....')
        self.sectopsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comparebtn = wx.Button(self.sectoppanel, -1, 'Compare', (150, 40))
        self.cancelbtn = wx.Button(self.sectoppanel, -1, 'Clear', (150, 40))
        self.emptytxt = wx.StaticText(self.sectoppanel, -1, '',size=(-1,40))
        self.sectopsizer.Add(self.comparebtn, 0, wx.EXPAND|wx.ALL, 5)
        self.sectoppanel.Bind(wx.EVT_BUTTON, self.compareList, id= self.comparebtn.GetId())
        self.sectoppanel.Bind(wx.EVT_BUTTON, self.cancelList, id= self.cancelbtn.GetId())
        self.sectopsizer.Add(self.cancelbtn, 0, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        self.sectopsizer.Add(self.emptytxt, 1, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)

        self.sectoppanel.SetSizer(self.sectopsizer)

        self.secsizer.Add(self.sectoppanel, 0, wx.EXPAND|wx.ALL, 5)
        self.secsizer.Add(self.secmidpanel,1, wx.EXPAND| wx.LEFT|wx.BOTTOM|wx.RIGHT, 3)

        midsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.firinputbox = rc.RichTextCtrl(self.secmidpanel, -1, size=(100, -1))
        self.secinputbox = rc.RichTextCtrl(self.secmidpanel, -1, size=(100, -1))
        self.secoutputbox = rc.RichTextCtrl(self.secmidpanel, -1, size=(-1, -1),style=wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH|wx.TE_RICH2)

        midsizer.Add(self.firinputbox, 0, wx.EXPAND|wx.ALL, 3)
        midsizer.Add(self.secinputbox, 0, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, 3)
        midsizer.Add(self.secoutputbox, 1, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, 3)

        self.secmidpanel.SetSizer(midsizer)
        self.mainpaneltwo.SetSizer(self.secsizer)
        self.mainpaneltwo.Layout()
        self.mainpaneltwo.SendSizeEvent()
    def compareList(self, event):
        uniquelist = []
        if (self.firinputbox != '' and self.firinputbox != '\n' and self.secinputbox != '' and self.secinputbox != '\n'):
            self.totallist = len(self.firinputbox.GetValue().strip('\n').split('\n')) + len(self.secinputbox.GetValue().strip('\n').split('\n'))
            self.counter = 0
            self.setStaticText(' Waiting for processing ...')
            self.gauge.SetRange(self.totallist)
            self.statictext3.SetLabel('  Running Comparison.....')
            uniquelist = self.returnComparison(self.firinputbox.GetValue().strip('\n').split('\n'), self.secinputbox.GetValue().strip('\n').split('\n')) + self.returnComparison(self.secinputbox.GetValue().strip('\n').split('\n'), self.firinputbox.GetValue().strip('\n').split('\n'))
            if uniquelist != []:
                comparestring  = "'"+str("'".join(uniquelist))+"'"
                self.secoutputbox.WriteText(comparestring)
                self.checkMax(comparestring)
                self.setStaticText(' Processing Completed Successfully')
            self.statictext2.SetLabel(' Found %s unique records'%(str(len(uniquelist))))
            self.setStaticText3('  Done :-) !!!')
            self.defillGauge()
    def setStaticText(self, txt):
        self.statictext.SetLabel(txt)
    def setStaticText1(self, txt):
        self.statictext1.SetLabel(txt)
    def setStaticText2(self, txt):
        self.statictext2.SetLabel(txt)
    def setStaticText3(self, txt):
        self.statictext3.SetLabel(txt)
    def cancelList(self, event):
        self.secinputbox.Clear()
        self.firinputbox.Clear()
        self.secoutputbox.Clear()
        self.setStaticText('  All cleared..')
    def returnComparison(self, list1, list2):
        localist= []
        for i in list1:
            if i not in list2:
                if self.counter <= self.totallist:
                    self.gauge.SetValue(self.counter)
                localist.append(i)
            self.counter += 1
        return localist
    def defillGauge(self):
        if self.totallist >= 0:
            newvalue = self.totallist
            for i in range(self.totallist):
                newvalue -= 1
                if newvalue >= 0:
                    self.gauge.SetValue(newvalue)

    def setChoice(self, event):
        radioSelected = event.GetEventObject()
        i = 0
        for item in self.choicelist:
            if item == radioSelected.GetStringSelection():
                self.choice = radioSelected.GetStringSelection()
            i += 0
    def clearInfo(self, event):
        self.inputbox.Clear()
        self.outputbox.Clear()
        self.setStaticText3('')
        self.statictext.SetLabel('  All cleared....... ')
    def processInfo(self, event):
        if self.choice == 'Apostrophe':
            self.formatText("','")
            self.statictext1.SetLabel('   In apostrophe mode .....')
        elif self.choice == 'Comma':
            self.formatText(",")
            self.statictext1.SetLabel('   In comma mode .....')
        else:
            self.formatText("\t")
            self.statictext1.SetLabel('   In space mode .....')
    def removeDuplicates(self, event):
        self.outputbox.Clear()
        self.setStaticText('')
        if self.inputbox != '' and self.inputbox != '\n' and self.inputbox.GetValue().strip('\n').split('\n') != []:
            nondupl = list(set(self.inputbox.GetValue().strip('\n').split('\n')))
            duplidisplay = "'"+"','".join(nondupl)+"'"
            if duplidisplay !=  "''":
                self.outputbox.WriteText(duplidisplay)
                self.checkMax(duplidisplay)
                self.setStaticText(' Removed %s duplicates'%(len(self.inputbox.GetValue().strip('\n').split('\n')) - len(nondupl)))
            else:
                self.setStaticText('No duplicates to remove')
    def formatText(self, mode):
        idxes = []
        if str(self.inputbox.GetValue()) != '':
            self.setStaticText("  Processed "+str(self.inputbox.GetNumberOfLines())+" Records ")
        else:
            self.setStaticText("  Processed 0 records")
        i = 0
        for idx in self.inputbox.GetValue().strip('\n').split('\n'):
                idxes.append(idx.strip('\n').strip('\t'))
                i += 1
        newlist = mode.join(idxes).strip('\n')
        if self.inputbox.GetValue() != '' and self.inputbox.GetValue() != '\n' and self.choice == 'Apostrophe':

            newerlist = "'"+newlist+"'"
        else:
            newerlist = newlist
        self.outputbox.Clear()
        self.outputbox.BeginAlignment(rc.TEXT_ALIGNMENT_LEFT)
        self.outputbox.WriteText(newerlist)
        self.checkMax(newerlist)
        self.outputbox.EndAlignment()
        self.outputbox.SelectAll()
    def checkMax(self, limits):
        if len(limits) > 65395:
            self.maxCharExceeded()
    def maxCharExceeded(self):
        self.statictext3.SetForegroundColour('#F95330')
        self.statictext3.SetLabel('Max 65395 chars(9500 records) reached, records maybe hidden from view but still selectable ')
if __name__ == '__main__':
    app =wx.App(False)
    frame = quicktext()
    frame.Show()
    app.MainLoop()


