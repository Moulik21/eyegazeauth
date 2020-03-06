import os
import wx
import webbrowser
import wx.lib.buttons as buts
from passlib.hash import sha512_crypt

# get current file directory
curdir = os.path.dirname(os.path.realpath(__file__))

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

class MainPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super().__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        # add a hello message to the panel
        headerText = wx.StaticText(self, label="Set eye-gazing password", pos=(20, 20), size=wx.Size(50, 500))
        font18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Use your eyes to enter your password", pos=(20, 65), size=wx.Size(40, 500))
        font13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        infoText.SetFont(SEGOE_13)

        instrText = wx.StaticText(self, label="Select the password format of your preference:", pos=(20, 110), size=wx.Size(30, 500))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        instrText.SetFont(SEGOE_12)

        bmp = wx.Image(curdir + "/images/PinButton.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pinButton = wx.BitmapButton(self, -1, bmp, pos=(25, 148), size=(400, 60))
        pinButton.SetBackgroundColour(wx.WHITE)
        pinButton.SetWindowStyleFlag(wx.BU_LEFT)
        pinButton.Bind(wx.EVT_BUTTON, self.openNineGridFrame)

        bmp = wx.Image(curdir + "/images/PictureButton.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        picButton = wx.BitmapButton(self, -1, bmp, pos=(25, 205), size=(400, 60))
        picButton.SetBackgroundColour(wx.WHITE)
        picButton.Bind(wx.EVT_BUTTON, self.openPicturePointsFrame)
        
    def openPicturePointsFrame(self, event):
        frame = PicturePointsFrame(title="")
        frame.SetSize(wx.Size(700, 600))
        #self.frame_number += 1

    def openNineGridFrame(self, event):
        frame = NineGridFrame(None, wx.ID_ANY, "")
        frame.Show()


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

class PicturePointsPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super().__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        headerText = wx.StaticText(self, label="Set eye-gazing picture points password", pos=(20, 20), size=wx.Size(50, 500))
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Select a picture to use or choose your own:", pos=(20, 65), size=wx.Size(50, 500))
        infoText.SetFont(SEGOE_12)

        sample1Img = wx.Image(curdir + "/images/sample1.jpg", wx.BITMAP_TYPE_ANY)
        sample1ImgIcon = sample1Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample1ImgIcon = sample1ImgIcon.ConvertToBitmap()
        sample1Button = wx.BitmapButton(self, -1, sample1ImgIcon, pos=(25, 98), size=(192, 108))
        sample1Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample1Img))

        sample2Img = wx.Image(curdir + "/images/sample2.jpg", wx.BITMAP_TYPE_ANY)
        sample2ImgIcon = sample2Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample2ImgIcon = sample2ImgIcon.ConvertToBitmap()
        sample2Button = wx.BitmapButton(self, -1, sample2ImgIcon, pos=(225, 98), size=(192, 108))
        sample2Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample2Img))

        sample3Img = wx.Image(curdir + "/images/sample3.jpg", wx.BITMAP_TYPE_ANY)
        sample3ImgIcon = sample3Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample3ImgIcon = sample3ImgIcon.ConvertToBitmap()
        sample3Button = wx.BitmapButton(self, -1, sample3ImgIcon, pos=(425, 98), size=(192, 108))
        sample3Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample3Img))

        sample4Img = wx.Image(curdir + "/images/sample4.jpg", wx.BITMAP_TYPE_ANY)
        sample4ImgIcon = sample4Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample4ImgIcon = sample4ImgIcon.ConvertToBitmap()
        sample4Button = wx.BitmapButton(self, -1, sample4ImgIcon, pos=(25, 214), size=(192, 108))
        sample4Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample4Img))

        sample5Img = wx.Image(curdir + "/images/sample5.jpg", wx.BITMAP_TYPE_ANY)
        sample5ImgIcon = sample5Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample5ImgIcon = sample5ImgIcon.ConvertToBitmap()
        sample5Button = wx.BitmapButton(self, -1, sample5ImgIcon, pos=(225, 214), size=(192, 108))
        sample5Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample5Img))

        sample6Img = wx.Image(curdir + "/images/sample6.jpg", wx.BITMAP_TYPE_ANY)
        sample6ImgIcon = sample6Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample6ImgIcon = sample6ImgIcon.ConvertToBitmap()
        sample6Button = wx.BitmapButton(self, -1, sample6ImgIcon, pos=(425, 214), size=(192, 108))
        sample6Button.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event, sample6Img))

        chooseImgButton = wx.Button(self, label="Choose your own", pos=(25, 345), size=(145, 35))
        chooseImgButton.SetBackgroundColour(wx.WHITE)
        chooseImgButton.SetFont(SEGOE_12)
        chooseImgButton.Bind(wx.EVT_BUTTON, self.onOpenFile)

    def openPicturePointsSelectFrame(self, event, img):
        frame = PicturePointsSelectFrame(img=img, title="")
        frame.SetSize(wx.Size(img.Width, img.Height))
        wx.MessageBox("To set your password, click a series of 4 points on the image", " ", wx.OK | wx.ICON_INFORMATION)

    def onOpenFile(self, event):
        wildcard = "Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png|" \
                       "All files (*.*)|*.*"
        #wildcard = "BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            chosenImg = wx.Image(path, wx.BITMAP_TYPE_ANY)
            self.openPicturePointsSelectFrame(event, chosenImg)
        dlg.Destroy()


class PicturePointsSelectFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, img, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, pos=(0, 0))
        self.OnInit(img)
        self.Show()

    def OnInit(self, img):
        panel = PicturePointsSelectPanel(parent=self, img=img)
        self.SetBackgroundColour('white')

class PicturePointsSelectPanel(wx.Panel):
    selection = []
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent, img):
        super().__init__(parent=parent)
        self.img = img
        self.bmpImg = self.img.ConvertToBitmap()
        self.sbmpImg = wx.StaticBitmap(self, -1, self.bmpImg, (1, 1), (self.img.GetWidth(), self.img.GetHeight()))
        self.sbmpImg.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        self.selection = []
        self.Show(True)

    def onClick(self, event):
        pos = event.GetPosition()
        self.selection.append(pos)
        dc = wx.MemoryDC(self.bmpImg)
        dc.SetBrush(wx.Brush(wx.GREEN))
        dc.DrawCircle(pos.x, pos.y, 7)
        dc.SelectObject(wx.NullBitmap)
        self.sbmpImg.SetBitmap(self.bmpImg)
        if (len(self.selection) == 4):
            happySelection = wx.MessageDialog(None, "Are you happy with your selection?", " ", wx.YES | wx.NO | wx.ICON_INFORMATION)
            if happySelection.ShowModal() == wx.ID_NO:
                self.selection = []
                #dc.Clear()
                #self.Show(True)
                #dc.SelectObject(self.img)
                self.bmpImg = self.img.ConvertToBitmap()
                self.sbmpImg.SetBitmap(self.bmpImg)
            else:
                print("Save selection")
                self.GetParent().Close()
                wx.MessageBox("Password has been saved", " ", wx.OK | wx.ICON_INFORMATION)

class NineGridFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = NineGridPanel(self)
        box_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(box_sizer)
        box_sizer.Fit(self)

class NineGridPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.selected_pictures = []
        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/bicycle/bicycle1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_2 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/car/car1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_3 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/cat/cat1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_4 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/door/door1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_5 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/flower/flower1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_6 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/guitar/guitar1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_7 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/lamp/lamp1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_8 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/moon/moon1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_9 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir+ "/images/tree/tree1.jpg", wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        self.bitmap_button_1.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_1.SetLabel('bicycle')

        self.bitmap_button_2.SetSize(self.bitmap_button_2.GetBestSize())
        self.bitmap_button_2.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_2.SetLabel('car')

        self.bitmap_button_3.SetSize(self.bitmap_button_3.GetBestSize())
        self.bitmap_button_3.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_3.SetLabel('cat')

        self.bitmap_button_4.SetSize(self.bitmap_button_4.GetBestSize())
        self.bitmap_button_4.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_4.SetLabel('door')

        self.bitmap_button_5.SetSize(self.bitmap_button_5.GetBestSize())
        self.bitmap_button_5.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_5.SetLabel('flower')

        self.bitmap_button_6.SetSize(self.bitmap_button_6.GetBestSize())
        self.bitmap_button_6.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_6.SetLabel('guitar')

        self.bitmap_button_7.SetSize(self.bitmap_button_7.GetBestSize())
        self.bitmap_button_7.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_7.SetLabel('lamp')

        self.bitmap_button_8.SetSize(self.bitmap_button_8.GetBestSize())
        self.bitmap_button_8.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_8.SetLabel('moon')

        self.bitmap_button_9.SetSize(self.bitmap_button_9.GetBestSize())
        self.bitmap_button_9.Bind(wx.EVT_BUTTON, self.button_handler)
        self.bitmap_button_1.SetLabel('tree')
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        self.grid_sizer_1 = wx.GridBagSizer(0, 0)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, 'Select the first picture')
        self.label_1.SetFont(wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI'))
        self.grid_sizer_1.Add(self.label_1, (0, 0), (1, 3), wx.ALIGN_LEFT, 0)
        self.grid_sizer_1.Add(self.bitmap_button_1, (1, 0), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_2, (1, 1), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_3, (1, 2), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_4, (2, 0), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_5, (2, 1), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_6, (2, 2), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_7, (3, 0), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_8, (3, 1), (1, 1), 0, 0)
        self.grid_sizer_1.Add(self.bitmap_button_9, (3, 2), (1, 1), 0, 0)
        self.SetSizerAndFit(self.grid_sizer_1)
        self.grid_sizer_1.AddGrowableRow(1)
        self.grid_sizer_1.AddGrowableRow(2)
        self.grid_sizer_1.AddGrowableRow(3)
        self.grid_sizer_1.AddGrowableCol(0)
        self.grid_sizer_1.AddGrowableCol(1)
        self.grid_sizer_1.AddGrowableCol(2)
        self.Layout()
        # end wxGlade    

    def button_handler(self, event):
        label = event.GetEventObject().GetLabel()
        lst = ['first', 'second', 'third', 'fourth']
        self.selected_pictures.append(label)

        if len(self.selected_pictures) == 4:
            happySelection = wx.MessageDialog(None, "Your password is: " + ' '.join(self.selected_pictures), " ", wx.YES | wx.NO)
            if happySelection.ShowModal() == wx.ID_NO:
                self.selected_pictures = []
                self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))
            else:
                pswd_hash = sha512_crypt.hash(''.join(self.selected_pictures))

                pswd_file = open("User-Interface/password.txt","w")
                pswd_file.seek(0)
                pswd_file.write(pswd_hash)
                self.GetParent().Close()
                wx.MessageBox("Password has been saved", " ", wx.OK | wx.ICON_INFORMATION)
        else:
            self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
