import wx


class CutDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Cutting fragments', size=(400, 300))
        p = wx.Panel(self)
        s = wx.BoxSizer(wx.VERTICAL)
        duration = parent.editor.get_fragment_duration()
        self.sld_1 = wx.Slider(p, value=0, minValue=0, maxValue=duration, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.sld_2 = wx.Slider(p, value=duration, minValue=0, maxValue=duration, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        b = wx.Button(p, id=wx.ID_OK, label='OK')
        b.Bind(wx.EVT_BUTTON, self.save)
        s.Add(self.sld_1, 2, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 30)
        s.Add(self.sld_2, 2, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 30)
        s.Add(b, 1, wx.ALIGN_CENTER, 1)
        p.SetSizer(s)

    def save(self, event):
        if self.IsModal():
            self.EndModal(event.Id)
        self.Destroy()


class SecondsInput(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Time in seconds", wx.DefaultPosition, size=(400, 200))
        self.parent = parent
        p = wx.Panel(self)
        s = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(p, -1, 'Please enter duration time of chosen effect in seconds')
        s.Add(t, 1, wx.ALIGN_CENTER, 1)
        t = wx.StaticText(p, -1, 'It  could be no less than zero and no more than  600 seconds')
        s.Add(t, 1, wx.ALIGN_CENTER, 1)
        self.e = wx.SpinCtrl(p, min=0, max=600, initial=10)
        s.Add(self.e, 1, wx.ALIGN_CENTER, 1)
        b = wx.Button(p, id=wx.ID_OK, label='OK')
        s.Add(b, 1, wx.ALIGN_CENTER, 1)
        b.Bind(wx.EVT_BUTTON, self.save)
        p.SetSizer(s)

    def save(self, event):
        if self.IsModal():
            self.EndModal(event.Id)
        self.Destroy()