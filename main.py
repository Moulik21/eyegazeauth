import os
import sys
import wx
import webbrowser
import wx.lib.buttons as buts
from passlib.hash import sha512_crypt

class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(clearSigInt=True)

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
        super(MainFrame, self).__init__(parent=parent, title=title, pos=pos)
        self.OnInit()

    def OnInit(self):
        panel = MainPanel(parent=self)
        self.SetBackgroundColour('white')

class NewPictureFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        box_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(box_sizer)
        box_sizer.Fit(self)
        self.Show()
    
    '''
    def __init__(self, parent, title, pos):
        super(NewPictureFrame, self).__init__(parent=parent, title=title, pos=pos)
        self.OnInit()


        self.OnInit()
    '''

    def OnInit(self):
        panel = NewPicturePanel(parent=self)
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


class LoginFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title)
        self.OnInit()
        self.Show()

    def OnInit(self):
        panel = LoginPanel(parent=self)
        self.SetBackgroundColour('white')

class TextPasswordFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title)
        self.OnInit()
        self.Show()

    def OnInit(self):
        panel = TextPasswordPanel(parent=self)
        self.SetBackgroundColour('white')



class MainPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        # add a hello message to the panel
        headerText = wx.StaticText(self, label="Set eye-gazing password", pos=(20, 20), size=wx.Size(50,20))
        font18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Use your eyes to enter your password", pos=(20, 65), size=wx.Size(40, 20))
        font13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        infoText.SetFont(SEGOE_13)

        instrText = wx.StaticText(self, label="Select the password format of your preference:", pos=(20, 110), size=wx.Size(40, 30))
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

        textPasswordButton = wx.Button(self, label="Text Style Password", pos=(25, 265), size=(200, 50))
        textPasswordButton.SetBackgroundColour(wx.WHITE)
        textPasswordButton.SetFont(SEGOE_12)
        textPasswordButton.Bind(wx.EVT_BUTTON, self.openTextPasswordFrame)

        loginButton = wx.Button(self, label="Text Login", pos=(500, 75), size=(90, 50))
        loginButton.SetBackgroundColour(wx.WHITE)
        loginButton.SetFont(SEGOE_12)
        loginButton.Bind(wx.EVT_BUTTON, self.openLoginFrame)

    def onSubmit(self, event):
        # stuff for the submit button to do
        webbrowser.open('https://wxpython.org/Phoenix/docs/html/index.html')

    def openPicturePointsFrame(self, event):
        #frame = PicturePointsFrame(title="")
        frame = NewPictureFrame(None, wx.ID_ANY, "")
        #self.frame_number += 1

    def openLoginFrame(self, event):
        frame = LoginFrame(title="")
        frame.SetSize(wx.Size(700, 600))

    def openTextPasswordFrame(self, event):
        frame = TextPasswordFrame(title="")
        frame.SetSize(wx.Size(700, 600))

class MyPanel(wx.Panel):
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
        self.label_1.SetFont(wx.Font(25, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial'))
        self.label_1.SetMinSize(wx.Size(600, 39))
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
        self.selected_pictures.append(label)\

        if len(self.selected_pictures) == 4:
            self.label_1.SetLabel('Passwowrd set')
            pswd_hash = sha512_crypt.hash(''.join(self.selected_pictures))
            print("Hash: " + str(pswd_hash))
        else:
            self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))

class TextPasswordPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super(TextPasswordPanel, self).__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        usernameText = wx.StaticText(self, label="Username", pos=(20, 20), size=wx.Size(40, 30))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        usernameText.SetFont(SEGOE_12)
        self.usernameBox = wx.TextCtrl(self, pos=(20, 60))

        passwordText = wx.StaticText(self, label="Password", pos=(20, 100), size=wx.Size(40, 30))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        passwordText.SetFont(SEGOE_12)
        self.passwordBox = wx.TextCtrl(self,style = wx.TE_PASSWORD, pos=(20, 140))

        self.setButton = wx.Button(self, label="Set Password", pos=(20, 180), size=(150, 50))
        self.setButton.SetBackgroundColour(wx.WHITE)
        self.setButton.SetFont(SEGOE_12)
        self.setButton.Bind(wx.EVT_BUTTON, self.setPassword)

    def setPassword(self, event):

        username = self.usernameBox.GetValue()
        password = self.passwordBox.GetValue()
        pswd_file = open("password.txt","w")

        pswd_hash = sha512_crypt.hash(password)

        pswd_file.seek(0)
        pswd_file.write(pswd_hash)

        print("Password set succesfully!")

        frame = MainFrame(parent=None, title="", pos=(100, 100))
        frame.SetSize(wx.Size(700, 600))



class LoginPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent=parent)

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        usernameText = wx.StaticText(self, label="Username", pos=(20, 20), size=wx.Size(40, 30))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        usernameText.SetFont(SEGOE_12) 
        self.usernameBox = wx.TextCtrl(self, pos=(20, 60))

        passwordText = wx.StaticText(self, label="Password", pos=(20, 100), size=wx.Size(40, 30))
        font12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        passwordText.SetFont(SEGOE_12)
        self.passwordBox = wx.TextCtrl(self,style = wx.TE_PASSWORD, pos=(20, 140))

        self.loginButton = wx.Button(self, label="Login", pos=(20, 180), size=(50, 30))
        self.loginButton.SetBackgroundColour(wx.WHITE)
        self.loginButton.SetFont(SEGOE_12)
        self.loginButton.Bind(wx.EVT_BUTTON, self.loginUser)


    def loginUser(self, event):

        username = self.usernameBox.GetValue()
        password = self.passwordBox.GetValue()

        pswd_file = open("password.txt","r+")


        #manually write a password
        #pswd_hash = sha512_crypt.hash(password)
        #pswd_file.seek(0)
        #pswd_file.write(pswd_hash)

        
        file_pswd = pswd_file.read()

        if (sha512_crypt.verify(password, file_pswd)):
            print("Correct")
            sys.exit(0)
        else:
            print("Wrong")


        

class PicturePointsPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self, parent):
        super(PicturePointsPanel, self).__init__(parent=parent)

        self.password = ""

        SEGOE_12 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_13 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')
        SEGOE_18 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Segoe UI')

        headerText = wx.StaticText(self, label="Set eye-gazing picture points password", pos=(20, 20), size=wx.Size(150, 40))
        headerText.SetFont(SEGOE_18)

        infoText = wx.StaticText(self, label="Select a picture to use or choose your own:", pos=(20, 65), size=wx.Size(150, 40))
        infoText.SetFont(SEGOE_12)

        #current file directory
        curdir = os.path.dirname(os.path.realpath(__file__))

        sample1Img = wx.Image(curdir + "/images/sample1.jpg", wx.BITMAP_TYPE_ANY)
        sample1ImgIcon = sample1Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample1ImgIcon = sample1ImgIcon.ConvertToBitmap()
        sample1Button = wx.BitmapButton(self, -1, sample1ImgIcon, pos=(25, 98), size=(192, 108))
        sample1Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample1Button.SetLabel("1")

        sample2Img = wx.Image(curdir + "/images/sample2.jpg", wx.BITMAP_TYPE_ANY)
        sample2ImgIcon = sample2Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample2ImgIcon = sample2ImgIcon.ConvertToBitmap()
        sample2Button = wx.BitmapButton(self, -1, sample2ImgIcon, pos=(225, 98), size=(192, 108))
        sample2Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample2Button.SetLabel("2")

        sample3Img = wx.Image(curdir + "/images/sample3.jpg", wx.BITMAP_TYPE_ANY)
        sample3ImgIcon = sample3Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample3ImgIcon = sample3ImgIcon.ConvertToBitmap()
        sample3Button = wx.BitmapButton(self, -1, sample3ImgIcon, pos=(425, 98), size=(192, 108))
        sample3Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample3Button.SetLabel("3")

        sample4Img = wx.Image(curdir + "/images/sample4.jpg", wx.BITMAP_TYPE_ANY)
        sample4ImgIcon = sample4Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample4ImgIcon = sample4ImgIcon.ConvertToBitmap()
        sample4Button = wx.BitmapButton(self, -1, sample4ImgIcon, pos=(25, 214), size=(192, 108))
        sample4Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample4Button.SetLabel("4")

        sample5Img = wx.Image(curdir + "/images/sample5.jpg", wx.BITMAP_TYPE_ANY)
        sample5ImgIcon = sample5Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample5ImgIcon = sample5ImgIcon.ConvertToBitmap()
        sample5Button = wx.BitmapButton(self, -1, sample5ImgIcon, pos=(225, 214), size=(192, 108))
        sample5Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample5Button.SetLabel("5")

        sample6Img = wx.Image(curdir + "/images/sample6.jpg", wx.BITMAP_TYPE_ANY)
        sample6ImgIcon = sample6Img.Scale(192, 108, wx.IMAGE_QUALITY_HIGH)
        sample6ImgIcon = sample6ImgIcon.ConvertToBitmap()
        sample6Button = wx.BitmapButton(self, -1, sample6ImgIcon, pos=(425, 214), size=(192, 108))
        sample6Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        sample6Button.SetLabel("6")

        #sample7Img = wx.Image(curdir + "/images/SaveButton.png", wx.BITMAP_TYPE_ANY)
        #sample7ImgIcon = sample7Img.Scale(59, 32, wx.IMAGE_QUALITY_HIGH)
        #sample7ImgIcon = sample7ImgIcon.ConvertToBitmap()
        #sample7Button = wx.BitmapButton(self, -1, sample7ImgIcon, pos=(425, 414), size=(59, 32))
        #sample7Button.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        #sample7Button.SetLabel("Save")
        saveImgButton = wx.Button(self, label="Save Password", pos=(300, 345), size=(145, 35))
        saveImgButton.SetBackgroundColour(wx.WHITE)
        saveImgButton.SetFont(SEGOE_12)
        saveImgButton.Bind(wx.EVT_BUTTON, self.selectSampleImage)
        saveImgButton.SetLabel("Save")

        chooseImgButton = wx.Button(self, label="Choose your own", pos=(25, 345), size=(145, 35))
        chooseImgButton.SetBackgroundColour(wx.WHITE)
        chooseImgButton.SetFont(SEGOE_12)
        chooseImgButton.Bind(wx.EVT_BUTTON, self.onOpenFile)

    def selectSampleImage(self, event):
        btn = event.GetEventObject().GetLabel()
        #password = ""
        print("Selected " + str(btn))

        if btn == "Save":
            pswd_hash = sha512_crypt.hash(self.password)
            print("Hash: " + str(pswd_hash))
            self.password = ""

        else:
            self.password += btn
            print(self.password)

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

class NewPicturePanel(wx.Panel):
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
        self.label_1.SetFont(wx.Font(25, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial'))
        self.label_1.SetMinSize(wx.Size(600, 39))
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
        self.selected_pictures.append(label)\

        if len(self.selected_pictures) == 4:
            self.label_1.SetLabel('Passwowrd set')
            pswd_hash = sha512_crypt.hash(''.join(self.selected_pictures))
            print("Hash: " + str(pswd_hash))
        else:
            self.label_1.SetLabel('Select the {s} picture'.format(s=lst[len(self.selected_pictures)]))


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
