import os

import wx
import webbrowser
import wx.lib.buttons as buts

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = MainFrame(parent=None, title="", pos=(100, 100))
        frame.SetSize(wx.Size(600, 500))
        frame.Show()


class MainFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, parent, title, pos):
        super().__init__(parent=parent, title=title, pos=pos)
        self.OnInit()

    def OnInit(self):
        panel = MainPanel(parent=self)
        self.SetBackgroundColour('white')

class PicturePointsFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title)
        self.OnInit()
        self.Show()

    def OnInit(self):
        panel = PicturePointsPanel(parent=self)
        self.SetBackgroundColour('white')

class MainPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super().__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        # add a hello message to the panel
        headerText = wx.StaticText(self, label="Set eye-gazing password", pos=(20, 20))
        font18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Use your eyes to enter your password", pos=(20, 65))
        font13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        infoText.SetFont(SEGOE_13)

        instrText = wx.StaticText(self, label="Select the password format of your preference:", pos=(20, 110))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        instrText.SetFont(SEGOE_12)

        #get current file directory
        curdir = os.path.dirname(os.path.realpath(__file__))

        bmp = wx.Image(curdir + "/images/PinButton.PNG", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pinButton = wx.BitmapButton(self, -1, bmp, pos=(25, 148), size=(400, 60))
        pinButton.SetBackgroundColour(wx.WHITE)
        pinButton.SetWindowStyleFlag(wx.BU_LEFT)

        bmp = wx.Image(curdir + "/images/PictureButton.PNG", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        picButton = wx.BitmapButton(self, -1, bmp, pos=(25, 205), size=(400, 60))
        picButton.SetBackgroundColour(wx.WHITE)
        picButton.Bind(wx.EVT_BUTTON, self.openPicturePointsFrame)

    def onSubmit(self, event):
        # stuff for the submit button to do
        webbrowser.open('https://wxpython.org/Phoenix/docs/html/index.html')

    def openPicturePointsFrame(self, event):
        frame = PicturePointsFrame(title="")
        frame.SetSize(wx.Size(700, 600))
        #self.frame_number += 1

class PicturePointsPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super().__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        headerText = wx.StaticText(self, label="Set eye-gazing picture points password", pos=(20, 20))
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Select a picture to use or choose your own:", pos=(20, 65))
        infoText.SetFont(SEGOE_12)

        #current file directory
        curdir = os.path.dirname(os.path.realpath(__file__))

        sample1Img = wx.Image(curdir + "/images/sample1.jpg", wx.BITMAP_TYPE_ANY)
        sample1ImgIcon = sample1Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample1ImgIcon = sample1ImgIcon.ConvertToBitmap()
        sample1Button = wx.BitmapButton(self, -1, sample1ImgIcon, pos=(25, 98), size=(192, 108))
        sample1Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        sample2Img = wx.Image(curdir + "/images/sample2.jpg", wx.BITMAP_TYPE_ANY)
        sample2ImgIcon = sample2Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample2ImgIcon = sample2ImgIcon.ConvertToBitmap()
        sample2Button = wx.BitmapButton(self, -1, sample2ImgIcon, pos=(225, 98), size=(192, 108))
        sample2Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        sample3Img = wx.Image(curdir + "/images/sample3.jpg", wx.BITMAP_TYPE_ANY)
        sample3ImgIcon = sample3Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample3ImgIcon = sample3ImgIcon.ConvertToBitmap()
        sample3Button = wx.BitmapButton(self, -1, sample3ImgIcon, pos=(425, 98), size=(192, 108))
        sample3Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        sample4Img = wx.Image(curdir + "/images/sample4.jpg", wx.BITMAP_TYPE_ANY)
        sample4ImgIcon = sample4Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample4ImgIcon = sample4ImgIcon.ConvertToBitmap()
        sample4Button = wx.BitmapButton(self, -1, sample4ImgIcon, pos=(25, 214), size=(192, 108))
        sample4Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        sample5Img = wx.Image(curdir + "/images/sample5.jpg", wx.BITMAP_TYPE_ANY)
        sample5ImgIcon = sample5Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample5ImgIcon = sample5ImgIcon.ConvertToBitmap()
        sample5Button = wx.BitmapButton(self, -1, sample5ImgIcon, pos=(225, 214), size=(192, 108))
        sample5Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        sample6Img = wx.Image(curdir + "/images/sample6.jpg", wx.BITMAP_TYPE_ANY)
        sample6ImgIcon = sample6Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample6ImgIcon = sample6ImgIcon.ConvertToBitmap()
        sample6Button = wx.BitmapButton(self, -1, sample6ImgIcon, pos=(425, 214), size=(192, 108))
        sample6Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)

        chooseImgButton = wx.Button(self, label="Choose your own", pos=(25, 345), size=(145, 35))
        chooseImgButton.SetBackgroundColour(wx.WHITE)
        chooseImgButton.SetFont(SEGOE_12)
        chooseImgButton.Bind(wx.EVT_BUTTON, self.onOpenFile)

    def selectSampleImage(self, event):
        print("Selected ")

    def onOpenFile(self, event):
        wildcard = "Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png|" \
                       "All files (*.*)|*.*"
        #wildcard = "BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print("You chose the following file(s):")
            for path in paths:
                print(path)
        dlg.Destroy()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()