# /usr/bin/env/python

import wx

global RETURN_2PGAME , RETURN_AIGAME, RETURN_UNKNOWN, RETURN_LANGAME
RETURN_UNKNOWN = 0
RETURN_2PGAME = 1
RETURN_AIGAME = 2
RETURN_LANGAME_HOST = 31
RETURN_LANGAME_CLIENT = 32

class LandingPage():
    def __init__(self):
        self.app = wx.App()
        self.exit = 0

    def run(self):
        mf = MainFrame(None,self)
        self.app.MainLoop()
        return self.exit

    def exitcode(self,code):
        self.exit = code


class MainFrame(wx.Frame):
    def __init__(self, parent, dispatch, title="Philip's checkers game", size=(250,400)):
        super(MainFrame, self).__init__(parent, title=title, size=size)
        self.dispatcher = dispatch
        self.mainpanel = MainPanel(self)
        self.lanpanel = LANPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mainpanel, 1, wx.EXPAND)
        self.sizer.Add(self.lanpanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.setMainPanel()
        self.Show()

    def setLANpanel(self):
        self.mainpanel.Hide()
        self.lanpanel.Show()
        self.Layout()

    def setMainPanel(self):
        self.mainpanel.Show()
        self.lanpanel.Hide()
        self.Layout()



class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)
        self.parent = parent
        self.setupLayout()

    def setupLayout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour('#ffffff')
        # buttons
        newBtn = wx.Button(self, label='New Game', size=(150,10))
        aiBtn = wx.Button(self, label='New AI Game', size=(150,10))
        lanBtn = wx.Button(self, label='New LAN Game', size=(150,10))
        settingsBtn = wx.Button(self, label='Settings', size=(150,10))

        vbox.AddMany([
            (newBtn, 1, wx.EXPAND|wx.ALL, 10),
            (aiBtn, 1, wx.EXPAND|wx.ALL, 10),
            (lanBtn, 1, wx.EXPAND|wx.ALL, 10),
            (settingsBtn, 1, wx.EXPAND|wx.ALL, 10),
            ])

        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.onNew, id=newBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.onAI, id=aiBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.onLAN, id=lanBtn.GetId())

    def onNew(self,e):
        print "onnew"
        self.GetParent().dispatcher.exitcode(RETURN_2PGAME)
        self.GetParent().Destroy()


    def onAI(self,e):
        self.GetParent().dispatcher.exitcode(RETURN_AIGAME)
        self.GetParent().Destroy()

    def onLAN(self, e):
        self.GetParent().setLANpanel()


class LANPanel(wx.Panel):
    def __init__(self, parent):
        super(LANPanel, self).__init__(parent)
        self.setupLayout()

    def setupLayout(self):
        self.SetBackgroundColour('#eeeeee')

        #sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # addr line
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        addr = wx.StaticText(self, label='Host:')
        self.iAddr = wx.TextCtrl(self)
        h1.Add(addr)
        h1.Add(self.iAddr, 1,flag=wx.EXPAND|wx.LEFT, border=10)
        vbox.Add(h1, 0, flag=wx.ALL|wx.EXPAND, border=10)

        # port line
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        port = wx.StaticText(self, label='Port:')
        self.iPort = wx.TextCtrl(self)

        h2.Add(port,)
        h2.Add(self.iPort,1,flag=wx.LEFT|wx.EXPAND, border=10)

        vbox.Add(h2, 0,flag=wx.ALL|wx.EXPAND, border=10)

        self.iHost = wx.CheckBox(self, label='Connect as host')
        vbox.Add(self.iHost, flag=wx.ALL, border=10)

        # button row
        buttonrow = wx.BoxSizer(wx.HORIZONTAL)
        hostbutton = wx.Button(self,label='Connect', size=(75,30))
        cancelbutton = wx.Button(self,label='Cancel', size=(75,30))
        buttonrow.Add(hostbutton, 1,flag=wx.EXPAND)
        buttonrow.Add(cancelbutton, 1, flag=wx.EXPAND|wx.LEFT, border=10)

        vbox.Add(buttonrow, flag=wx.ALL|wx.EXPAND, border=10)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.onConnect, id=hostbutton.GetId())
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=cancelbutton.GetId())


    def onConnect(self,e):
        addr = self.iAddr.GetValue()
        port = self.iPort.GetValue()
        host = self.iHost.GetValue()

        print (addr, port, host)


    def onCancel(self,e):
        self.GetParent().setMainPanel()


if __name__ == '__main__':
    LandingPage(None)
