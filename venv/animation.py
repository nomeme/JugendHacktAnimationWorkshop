#!bin/python

import wx
import wx.svg
import time
import math
import os

class AnimationWindow(wx.Frame):
    def __init__(self, parent, title, size):
        super(AnimationWindow, self).__init__(parent, title = title, size = size)
        self.Images = self.listFiles("./img/")
        self.InitUI()
        self.loadImage(self.Images[0])
        self.Timer = wx.Timer(self, 1337)
        self.Bind(wx.EVT_TIMER, self.OnPaint)
        self.timeOld = int(round(time.time() * 1000))
        self.AngleOld = 0
        self.Rpm = 0;
        self.Fps = 0;
        self.Timer.Start(self.getFrameTime(1));

    def InitUI(self):
        self.MainPanel = wx.Panel(self)
        self.MainBox = wx.BoxSizer(wx.VERTICAL)

        self.DrawPanel = wx.Panel(self.MainPanel)
        #self.DrawPanel.SetBackgroundColour((255, 255, 0))
        self.MainBox.Add(self.DrawPanel, 5, wx.EXPAND)

        self.RpmPanel = self.InitControlPanel(self.MainPanel)
        self.MainBox.Add(self.RpmPanel, 1, wx.EXPAND)

        self.MainPanel.SetSizer(self.MainBox)
        #self.MainPanel.SetBackgroundColour((255, 0, 255))

        self.DrawPanel.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Centre()
        self.Show(True)

    def InitControlPanel(self, panel):
        #self.ControlPanel = wx.Panel(self)
        panel = wx.Panel(panel)
        sizer = wx.GridBagSizer(3, 6)

        mainRpmLabel = wx.StaticText(panel, label = "Set the rotations per minute")
        sizer.Add(mainRpmLabel, pos = (0, 0), span = (1, 2))

        smallRpmLabel = wx.StaticText(panel, label = "RPM:")
        sizer.Add(smallRpmLabel, pos = (2, 0), span = (1, 1), border = 100)

        rpmSpinner = wx.SpinCtrl(panel, value = '0')
        rpmSpinner.SetRange(0,100000)
        rpmSpinner.Bind(wx.EVT_SPINCTRL, self.OnRpmChanged)
        sizer.Add(rpmSpinner, pos = (2, 1))

        mainFpsLabel = wx.StaticText(panel, label = "Set frames per second")
        sizer.Add(mainFpsLabel, pos = (0, 3), span = (1, 2))

        smallFpsLabel = wx.StaticText(panel, label = "FPS:")
        sizer.Add(smallFpsLabel, pos = (2, 2), span = (1, 1))

        #style = wx.TE_PROCESS_ENTER | wx.SP_ARROW_KEYS
        fpsSpinner = wx.SpinCtrl(panel, value = '0')
        fpsSpinner.SetRange(1, 60)
        fpsSpinner.Bind(wx.EVT_SPINCTRL, self.OnFpsChanged)
        sizer.Add(fpsSpinner, pos = (2, 3))

        listBox = wx.ListBox(panel, choices = self.Images, style = wx.LB_SINGLE)
        listBox.Bind(wx.EVT_LISTBOX, self.OnImageSelected)
        listBox.SetSelection(0)
        sizer.Add(listBox, pos = (0, 5), span = (3, 2))

        panel.SetSizer(sizer)
        #panel.SetBackgroundColour((0, 255, 255))
        return panel

    def OnRpmChanged(self, e):
        print(e.GetPosition())
        self.Rpm = e.GetPosition();

    def OnFpsChanged(self, e):
        print("OnFpsChanged")
        self.Fps = e.GetPosition();
        self.Timer.Stop()
        self.Timer.Start(self.getFrameTime(self.Fps))
        self.timeOld = int(round(time.time() * 1000))

    def OnImageSelected(self, e):
        print(self.Images[e.GetSelection()])
        self.loadImage(self.Images[e.GetSelection()])

    def getAngle(self, rpm, millis):
        # At first we need to compute rotations per millisecond
        rpms = rpm / (1000 * 60)
        factor = rpms * millis
        angle = 360 * factor
        return angle

    def getFrameTime(self, fps):
        return 1000/fps

    def OnPaint(self, e):
        timeNow = int(round(time.time() * 1000))
        timeDiff = timeNow - self.timeOld
        print("foo")
        dc = wx.PaintDC(self.DrawPanel)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        #dcdim = min(self.Size.width, self.Size.height)
        dcdim = min(self.DrawPanel.Size.width, self.DrawPanel.Size.height)
        imgdim = min(self.svgImg.width, self.svgImg.height)
        scale = dcdim / imgdim
        width = int(self.svgImg.width * scale)
        height = int(self.svgImg.height* scale)

        context = wx.GraphicsContext.Create(dc)
        context.Translate(width/2, height/2)
        angle = float(self.AngleOld) + float(self.getAngle(self.Rpm, timeDiff))
        context.Rotate(math.radians(angle))
        context.Translate(-width/2, -height/2)
        self.svgImg.RenderToGC(context, scale)

        self.timeOld = timeNow
        self.AngleOld = angle;


        #dc.DrawBitmap(wx.Bitmap("python.jpg"),10,10,True)
        #color = wx.Colour(255,0,0)
        #b = wx.Brush(color)

        #dc.SetBrush(b)
        #dc.DrawCircle(300,125,50)
        #dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        #dc.DrawCircle(300,125,30)

        #font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        #dc.SetFont(font)
        #dc.DrawText("Hello wxPython",200,10)

        #pen = wx.Pen(wx.Colour(0,0,255))
        #dc.SetPen(pen)
        #dc.DrawLine(200,50,350,50)
        #dc.SetBrush(wx.Brush(wx.Colour(0,255,0), wx.CROSS_HATCH))
        #dc.DrawRectangle(380, 15, 90, 60) 

    def listFiles(self, path):
        list = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith(".svg"):
                    print(filename)
                    list.append(path + filename)
        return list

    def loadImage(self, path):
        self.svgImg = wx.svg.SVGimage.CreateFromFile(path)
        #self.imgPng = cairo.svg.svg2png(path)

def main():
    app = wx.App()
    #top = wx.Frame(None, title="Animation", size=(640,640))
    fop = AnimationWindow(None, title="Animation", size = (640, 640))
    #top.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
