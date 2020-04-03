import math
import os
import wx
import webbrowser
import wx.lib.buttons as buts
import sys
import random as r
import math
import cv2
import numpy as np
import threading
from passlib.hash import sha512_crypt
from math import atan2, degrees

# get current file directory
curdir = os.path.dirname(os.path.realpath(__file__))
GRID_SIZE = 75

FACE_PATH = curdir + "/../Eye-tracking/haarcascade_frontalface_default.xml"
EYE_PATH = curdir + "/../Eye-tracking/haarcascade_eye.xml"

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
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour('white')

        self.customTitleBar = CustomTitleBar(self)
        self.boxSizer.Add(self.customTitleBar, 0, wx.EXPAND)
        self.customTitleBar.Hide()

        self.panel = MainPanel(parent=self)
        self.boxSizer.Add(self.panel, 1, wx.EXPAND)
        self.panel.Show()

        if os.path.exists(curdir + "/picturepointsname.txt"):
            picturePathFile = open(curdir + "/picturepointsname.txt", "r")
            picturePath = picturePathFile.readline()
            self.image = wx.Image(picturePath, wx.BITMAP_TYPE_ANY)
            self.picturePointsSelectPanel = PicturePointsSelectPanel(parent=self, img=self.image)
            self.boxSizer.Add(self.picturePointsSelectPanel, 1, wx.EXPAND)
            self.picturePointsSelectPanel.Hide()


        self.nineGridPanel = NineGridPanel(self)
        self.boxSizer.Add(self.nineGridPanel, 1, wx.EXPAND)
        self.nineGridPanel.Hide()

        self.SetSizer(self.boxSizer)

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
        self.eyeTracker = EyeTracker()

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

        if not os.path.exists(curdir + "/9gridlabels.txt"):
            wx.MessageBox("9 grid login has not been set up", " ", wx.OK | wx.ICON_INFORMATION)
        else:
            parent = self.GetParent()
            parent.panel.Hide()
            parent.SetWindowStyleFlag(wx.BORDER_NONE)
            parent.customTitleBar.Show()
            parent.customTitleBar.Layout()
            parent.nineGridPanel.Show()
            parent.Fit()
            parent.nineGridPanel.Layout()
            parent.ShowFullScreen(True)

            parent.eye_track_thread = threading.Thread(target=self.startEyeTrack, args=(parent.nineGridPanel.on_button_press,))
            parent.eye_track_thread.start()

    def startEyeTrack(self, func):
        self.eyeTracker.getTiles(func)


    def openPicturePointsSelectFrame(self, event):

        if not os.path.exists(curdir + "/picturepointsname.txt"):
            wx.MessageBox("Picture points has not been set up", " ", wx.OK | wx.ICON_INFORMATION)
        else:
            parent = self.GetParent()
            parent.panel.Hide()
            # parent.SetSize(wx.Size(parent.image.Width, parent.image.Height))
            parent.SetWindowStyleFlag(wx.BORDER_NONE)
            parent.customTitleBar.Show()
            parent.customTitleBar.Layout()
            parent.picturePointsSelectPanel.Show()
            parent.Fit()
            parent.picturePointsSelectPanel.Layout()
            parent.Maximize(True)



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
        # self.expected = []
        self.offsets = []
        # self.getExpectedPassword()
        self.getOffsets()

    def getOffsets(self):
        offsetsFile = open(curdir + "/picturepointsoffset.txt", "r")
        for i in range(4):
            offset = offsetsFile.readline()
            self.offsets.append(offset.strip())

    def onClick(self, event):
        pos = event.GetPosition()
        self.selection.append(pos)
        parentCustomTitleBar = self.GetParent().customTitleBar
        children = parentCustomTitleBar.sizerTitleBar.GetChildren()
        dotsWidget = children[1].GetWindow()
        if (len(self.selection) == 1):
            dotsWidget.SetLabel("⚫ ⚪ ⚪ ⚪")
        if (len(self.selection) == 2):
            dotsWidget.SetLabel("⚫ ⚫ ⚪ ⚪")
        if (len(self.selection) == 3):
            dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚪")
        if (len(self.selection) == 4):
            dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚫")
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
                    dotsWidget.SetLabel("⚪ ⚪ ⚪ ⚪")
                else:
                    self.GetParent().eye_track_thread.join()
                    self.GetParent().Close()

class NineGridPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.selected_pictures = []

        # get labels
        self.labels = []

        if not os.path.exists(curdir + "/9gridlabels.txt"):
            return
        
        with open(self.curdir + '/9gridlabels.txt', 'r') as f:
            for line in f:
                self.labels.append(line.split())
        

        self.buttons = []

        for i in range(9):
            # create buttons
            picture_label = self.labels[0][i]
            pictures = os.listdir(self.curdir + '/images/9_grid/' + picture_label)
            picture_number = pictures.pop(r.randint(0, len(pictures) - 1))
            self.buttons.append(wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
                self.curdir + "/images/9_grid/{0}/{1}".format(picture_label, picture_number))))

            # set labels
            self.buttons[i].SetSize(self.buttons[i].GetBestSize())
            self.buttons[i].Bind(wx.EVT_BUTTON, self.button_handler)
            self.buttons[i].SetLabel(picture_label)

        self.box_sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.box_sizer_1)

        self.grid_sizer_1 = wx.GridBagSizer(100, 0)

        for i in range(3):
            for j in range(3):
                self.grid_sizer_1.Add(self.buttons[(i * 3) + j], (i + 1, j), (1, 1), flag=wx.ALIGN_CENTER)

        self.grid_sizer_1.AddGrowableRow(0)
        self.grid_sizer_1.AddGrowableRow(1)
        self.grid_sizer_1.AddGrowableRow(2)
        self.grid_sizer_1.AddGrowableCol(0)
        self.grid_sizer_1.AddGrowableCol(1)
        self.grid_sizer_1.AddGrowableCol(2)
        self.box_sizer_1.Add(self.grid_sizer_1, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 25, 0)
        self.Layout()
        # end wxGlade

    def on_button_press(self, tile):
        label = self.labels[len(self.selected_pictures)-1][tile-1]
        self.selected_pictures.append(label)
        parentCustomTitleBar = self.GetParent().customTitleBar
        children = parentCustomTitleBar.sizerTitleBar.GetChildren()
        dotsWidget = children[1].GetWindow()

        if len(self.selected_pictures) == 4:
            dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚫")
            pswd_file = open(curdir + "/9gridpassword.txt", "r+")
            file_pswd = pswd_file.read()

            print(self.selected_pictures)

            if (sha512_crypt.verify(''.join(self.selected_pictures), file_pswd)):
                print('Authentication successful')
                self.GetParent().eye_track_thread.join()
                sys.exit(0)
            else:
                self.selected_pictures = []
                dotsWidget.SetLabel("⚪ ⚪ ⚪ ⚪")
                wx.MessageBox("Authentication failed", " ", wx.OK | wx.ICON_INFORMATION)
                # go back to first set of pictures
                for i in range(9):
                    picture_label = self.labels[len(self.selected_pictures)][i]
                    pictures = os.listdir(self.curdir + '/images/9_grid/' + picture_label)
                    picture_number = pictures.pop(r.randint(0, len(pictures) - 1))

                    self.buttons[i].SetBitmapLabel(
                        wx.Bitmap(self.curdir + "/images/9_grid/{0}/{1}".format(picture_label, picture_number)))
                    self.buttons[i].SetLabel(picture_label)

        else:
            if (len(self.selected_pictures) == 1):
                dotsWidget.SetLabel("⚫ ⚪ ⚪ ⚪")
            if (len(self.selected_pictures) == 2):
                dotsWidget.SetLabel("⚫ ⚫ ⚪ ⚪")
            if (len(self.selected_pictures) == 3):
                dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚪")

            # set next set of buttons
            for i in range(9):
                picture_label = self.labels[len(self.selected_pictures)][i]
                pictures = os.listdir(self.curdir + '/images/9_grid/' + picture_label)
                picture_number = pictures.pop(r.randint(0, len(pictures) - 1))

                self.buttons[i].SetBitmapLabel(
                    wx.Bitmap(self.curdir + "/images/9_grid/{0}/{1}".format(picture_label, picture_number)))
                self.buttons[i].SetLabel(picture_label)

    def button_handler(self, event):
        label = event.GetEventObject().GetLabel()
        self.selected_pictures.append(label)
        parentCustomTitleBar = self.GetParent().customTitleBar
        children = parentCustomTitleBar.sizerTitleBar.GetChildren()
        dotsWidget = children[1].GetWindow()

        if len(self.selected_pictures) == 4:
            dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚫")
            pswd_file = open(curdir + "/9gridpassword.txt", "r+")
            file_pswd = pswd_file.read()

            print(self.selected_pictures)

            if (sha512_crypt.verify(''.join(self.selected_pictures), file_pswd)):
                print('Authentication successful')
                self.GetParent().eye_track_thread.join()
                sys.exit(0)
            else:
                self.selected_pictures = []
                dotsWidget.SetLabel("⚪ ⚪ ⚪ ⚪")
                wx.MessageBox("Authentication failed", " ", wx.OK | wx.ICON_INFORMATION)

                # go back to first set of pictures
                for i in range(9):
                    picture_label = self.labels[len(self.selected_pictures)][i]
                    pictures = os.listdir(self.curdir + '/images/9_grid/' + picture_label)
                    picture_number = pictures.pop(r.randint(0, len(pictures) - 1))

                    self.buttons[i].SetBitmapLabel(
                        wx.Bitmap(self.curdir + "/images/9_grid/{0}/{1}".format(picture_label, picture_number)))
                    self.buttons[i].SetLabel(picture_label)
        else:
            if (len(self.selected_pictures) == 1):
                dotsWidget.SetLabel("⚫ ⚪ ⚪ ⚪")
            if (len(self.selected_pictures) == 2):
                dotsWidget.SetLabel("⚫ ⚫ ⚪ ⚪")
            if (len(self.selected_pictures) == 3):
                dotsWidget.SetLabel("⚫ ⚫ ⚫ ⚪")

            # set next set of buttons
            for i in range(9):
                picture_label = self.labels[len(self.selected_pictures)][i]
                pictures = os.listdir(self.curdir + '/images/9_grid/' + picture_label)
                picture_number = pictures.pop(r.randint(0, len(pictures) - 1))

                self.buttons[i].SetBitmapLabel(
                    wx.Bitmap(self.curdir + "/images/9_grid/{0}/{1}".format(picture_label, picture_number)))
                self.buttons[i].SetLabel(picture_label)


class CustomTitleBar(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        # Creating the custom title bar
        self.btnExit = wx.Button(self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.BU_NOTEXT)
        self.panelBody = wx.Panel(self, wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.OnBtnExitClick, self.btnExit)
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        closeImg = wx.Image(curdir + "/images/CloseIcon.png", wx.BITMAP_TYPE_ANY)
        closeImgIcon = closeImg.Scale(13, 13, wx.IMAGE_QUALITY_HIGH)
        closeImgIcon = closeImgIcon.ConvertToBitmap()
        self.btnExit.SetBitmap(closeImgIcon)
        self.btnExit.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):
        # Sizers:
        self.sizerTitleBar = wx.FlexGridSizer(1, 3, 0, 0)

        # Titlebar:
        self.progressDots = wx.StaticText(self, wx.ID_ANY, "⚪ ⚪ ⚪ ⚪", size=wx.Size(100, -1))
        self.progressDots.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizerTitleBar.Add(50, -1)
        self.sizerTitleBar.Add(self.progressDots, 0, wx.ALIGN_CENTER, 0)
        self.sizerTitleBar.Add(self.btnExit, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, -20)
        # self.sizerTitleBar.AddGrowableRow(0)
        self.sizerTitleBar.AddGrowableCol(1)

        self.SetSizer(self.sizerTitleBar)
        self.Layout()

    def OnBtnExitClick(self, event):
        self.GetParent().Close()


class TileTracker:
    def __init__(self, func):
        self.history_size = 10
        self.minimum_repeats = 6
        self.func = func
        self.history = [-1] * self.history_size
        self.last_location = -1
        self.tile_picks = []

    def record(self, tile):
        for x in range(self.history_size - 1):
            self.history[x] = self.history[x + 1]
        self.history[self.history_size - 1] = tile
        self.check_for_change(tile)

    def check_for_change(self,tile):
        count = 0
        for x in range(self.history_size):
            if self.history[x] == tile:
                count += 1
        if(count >= self.minimum_repeats and tile != self.last_location):
            self.last_location = tile
            print(tile)
            self.tile_picks.append(tile)
            wx.CallAfter(self.func, tile)


class EyeTracker():
    def __init__(self):
        self.initHaarCascade()

    def initHaarCascade(self):
        self.face_cascade = cv2.CascadeClassifier(FACE_PATH)
        self.eye_cascade = cv2.CascadeClassifier(EYE_PATH)
        detector_params = cv2.SimpleBlobDetector_Params()
        detector_params.filterByArea = True
        detector_params.maxArea = 1500
        self.detector = cv2.SimpleBlobDetector_create(detector_params)

    def detect_eyes(self, img, classifier):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
        width = np.size(img, 1) # get face frame width
        height = np.size(img, 0) # get face frame height
        left_eye = None
        right_eye = None
        for (x, y, w, h) in eyes:
            if y > height * 2 / 5:
                pass
            eyecenter = x + w / 2  # get the eye center
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if eyecenter < width * 0.5:
                left_eye = img[y:y + h, x:x + w]
            else:
                right_eye = img[y:y + h, x:x + w]

        return left_eye, right_eye

    def detect_faces(self, img, classifier):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        if len(coords) > 1:
            biggest = (0, 0, 0, 0)
            for i in coords:
                if i[3] > biggest[3]:
                    biggest = i
            biggest = np.array([i], np.int32)
        elif len(coords) == 1:
            biggest = coords
        else:
            return None
        for (x, y, w, h) in biggest:
            frame = img[y:y + h, x:x + w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame

    def blob_process(self, img, threshold, detector):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=2)
        img = cv2.dilate(img, None, iterations=4)
        img = cv2.medianBlur(img, 5)
        keypoints = detector.detect(img)

        return keypoints

    def cut_eyebrows(self, img):
        height, width = img.shape[:2]
        eyebrow_h = int(height / 4)
        img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
        return img

    def nothing(self, x):
        pass

    def getTiles(self, func):
        cap = cv2.VideoCapture(0)
        #cv2.namedWindow('image')
        #cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

        tile_tracker = TileTracker(func)
        while True:
            _, frame = cap.read()
            face_frame = self.detect_faces(frame, self.face_cascade)
            if face_frame is not None:

                eyes = self.detect_eyes(face_frame, self.eye_cascade)
                for eye in eyes:
                    if eye is not None:
                        thresh = 0
                        #threshold = cv2.getTrackbarPos('threshold', 'image')
                        eye = self.cut_eyebrows(eye)
                        keypoints = self.blob_process(eye, thresh, self.detector)
                        while(not keypoints and thresh < 100):
                            keypoints = self.blob_process(eye, thresh, self.detector)
                            thresh += 5
                        eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                        if(keypoints and len(keypoints)>0):
                            height, width = eye.shape[:2]
                            eye_box_center = [width/2, height/2]
                            pupil_point = keypoints[0].pt

                            xDiff = pupil_point[0] - eye_box_center[0]
                            yDiff = pupil_point[1] - eye_box_center[1]
                            distance = math.sqrt(xDiff * xDiff + yDiff * yDiff)

                            yDiff = -yDiff #account for the fact that the y axis moves downwards
                            angle = degrees(atan2(yDiff, xDiff))
                            result = -1
                            if distance < 6:
                                #forward
                                result = 5
                            elif angle > 0 and angle < 25:
                                #left
                                result = 4
                            elif angle >= 25 and angle <65:
                                #top left
                                result = 1
                            elif angle >= 65 and angle <110:
                                #up
                                result = 2
                            elif angle >= 110 and angle <120:
                                #top right
                                result = 3
                            elif angle >= 120 and angle <200:
                                #right
                                result = 6
                            elif angle >= 200 and angle <245:
                                #bottom right
                                result = 9
                            elif angle >= 245 and angle <290:
                                #down
                                result = 8
                            elif angle >= 290 and angle <335:
                                #bottom left
                                result = 7
                            elif angle >=335:
                                #left
                                result = 4
                            tile_tracker.record(result)
            #cv2.imshow('image', frame)
            if (len(tile_tracker.tile_picks) == 4):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()


'''
TODO
UNDERSTAND HOW TO ADJUST THE THRESHOLD
Maybe read up on how blob technique acutally works?
Need to dynamically set the threshold.... we're gonna need a calibrate function...

OBSERVATIONS
Tracking works a lot better at MODERATE LIGHTING
Make sure your eyes are not reflecting a lot of light
'''