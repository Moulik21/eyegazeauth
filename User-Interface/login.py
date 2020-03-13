import math
import os
import wx
import webbrowser
import wx.lib.buttons as buts
import sys
from passlib.hash import sha512_crypt

# get current file directory
curdir = os.path.dirname(os.path.realpath(__file__))
GRID_SIZE = 75


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
        # Blank icon workaround
        bmp = wx.Bitmap(1, 1)
        bmp.SetMaskColour(wx.BLACK)
        icon = wx.Icon(bmp)
        self.SetIcon(icon)


class MainPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.__do_layout()

    def __do_layout(self):
        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_16 = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        boxSizer = wx.BoxSizer(wx.VERTICAL)

        boxSizer.Add((-1, 20))

        # add a hello message to the panel
        headerText = wx.StaticText(self, label="Login using the method of your choice")
        headerText.SetFont(SEGOE_16)
        boxSizer.Add(headerText, 0, wx.LEFT, 30)

        boxSizer.Add((-1, 20))

        bmp = wx.Image(curdir + "/images/PinButton.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pinButton = wx.BitmapButton(self, wx.ID_ANY, bmp, style=wx.BORDER_NONE)
        pinButton.SetBackgroundColour(wx.WHITE)
        pinButton.SetWindowStyleFlag(wx.BU_LEFT)
        pinButton.Bind(wx.EVT_BUTTON, self.openNineGridFrame)
        boxSizer.Add(pinButton, 0, wx.LEFT, 30)

        boxSizer.Add((-1, 15))

        bmp = wx.Image(curdir + "/images/PictureButton.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        picButton = wx.BitmapButton(self, -1, bmp, style=wx.BORDER_NONE)
        picButton.SetBackgroundColour(wx.WHITE)
        picButton.Bind(wx.EVT_BUTTON, lambda event: self.openPicturePointsSelectFrame(event))
        boxSizer.Add(picButton, 0, wx.LEFT, 30)

        self.SetSizer(boxSizer)
        boxSizer.Layout()

    def openNineGridFrame(self, event):
        frame = NineGridFrame(None, wx.ID_ANY, "")
        frame.Show()

    def openPicturePointsSelectFrame(self, event):
        picturePathFile = open(curdir + "/picturepointsname.txt", "r")
        picturePath = picturePathFile.readline()
        image = wx.Image(picturePath, wx.BITMAP_TYPE_ANY)
        frame = PicturePointsSelectFrame(img=image, title="")
        frame.SetSize(wx.Size(image.Width, image.Height))
        # wx.MessageBox("To enter your password, click a series of 4 points on the image", " ", wx.OK | wx.ICON_INFORMATION)

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
        # Blank icon workaround
        bmp = wx.Bitmap(1, 1)
        bmp.SetMaskColour(wx.BLACK)
        icon = wx.Icon(bmp)
        self.SetIcon(icon)


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
        #self.expected = []
        self.offsets = []
        #self.getExpectedPassword()
        self.getOffsets()

    '''
    def getExpectedPassword(self):
        picturePointsPasswordFile = open(curdir + "/picturepointspassword.txt", "r")
        for i in range(4):
            point = picturePointsPasswordFile.readline()
            self.expected.append(point.strip())
    '''

    def getOffsets(self):
        offsetsFile = open(curdir + "/picturepointsoffset.txt", "r")
        for i in range(4):
            offset = offsetsFile.readline()
            self.offsets.append(offset.strip())

    def onClick(self, event):
        pos = event.GetPosition()
        self.selection.append(pos)
        dc = wx.MemoryDC(self.bmpImg)
        dc.SetBrush(wx.Brush(wx.GREEN))
        dc.DrawCircle(pos.x, pos.y, 7)
        dc.SelectObject(wx.NullBitmap)
        self.sbmpImg.SetBitmap(self.bmpImg)
        if (len(self.selection) == 4):

            self.selected_grids = []
            pswd_file = open(curdir + "/picturepointspassword.txt", "r")
            file_pswd = pswd_file.read()
            
            for i in range(4):
                offsetXY = self.offsets[i].split()
                # Move the user's selection closer to the center of the expected grid box
                transformedSelectionX = self.selection[i].x + int(offsetXY[0])
                transformedSelectionY = self.selection[i].y + int(offsetXY[1])
                gridBoxX = math.ceil(transformedSelectionX / GRID_SIZE)
                gridBoxY = math.ceil(transformedSelectionY / GRID_SIZE)
                self.selected_grids.append(str(gridBoxX) + " " + str(gridBoxY))


            if (sha512_crypt.verify(''.join(self.selected_grids), file_pswd)):
                print('Authentication successful')
                sys.exit(0)
            else:
                incorrectSelection = wx.MessageDialog(None,
                        "The password entered does not match the one stored. Retry?",
                        " ", wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
                # They want to retry
                if (incorrectSelection.ShowModal() == wx.ID_OK):
                    self.selection = []
                    self.bmpImg = self.img.ConvertToBitmap()
                    self.sbmpImg.SetBitmap(self.bmpImg)
                else:
                    self.GetParent().Close()

class NineGridFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = NineGridPanel(self)
        box_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(box_sizer)
        box_sizer.Fit(self)

        # Blank icon workaround
        bmp = wx.Bitmap(1, 1)
        bmp.SetMaskColour(wx.BLACK)
        icon = wx.Icon(bmp)
        self.SetIcon(icon)


class NineGridPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.selected_pictures = []
        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir + "/images/bicycle/bicycle1.jpg",
                                                                          wx.BITMAP_TYPE_ANY))
        self.bitmap_button_2 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/car/car1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_3 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/cat/cat1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_4 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/door/door1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_5 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir + "/images/flower/flower1.jpg",
                                                                          wx.BITMAP_TYPE_ANY))
        self.bitmap_button_6 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.curdir + "/images/guitar/guitar1.jpg",
                                                                          wx.BITMAP_TYPE_ANY))
        self.bitmap_button_7 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/lamp/lamp1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_8 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/moon/moon1.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_9 = wx.BitmapButton(self, wx.ID_ANY,
                                               wx.Bitmap(self.curdir + "/images/tree/tree1.jpg", wx.BITMAP_TYPE_ANY))

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
        self.bitmap_button_9.SetLabel('tree')
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
            pswd_file = open("User-Interface/password.txt", "r+")
            file_pswd = pswd_file.read()

            print(self.selected_pictures)

            if (sha512_crypt.verify(''.join(self.selected_pictures), file_pswd)):
                print('Authentication successful')
                sys.exit(0)
            else:
                self.selected_pictures = []
                self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))
                wx.MessageBox("Authentication failed", " ", wx.OK | wx.ICON_INFORMATION)
        else:
            self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
