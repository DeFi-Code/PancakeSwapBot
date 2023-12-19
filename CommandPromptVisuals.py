import pyautogui
import win32gui

# Getting Screen dimension
ScreenWidth, ScreenHeight = pyautogui.size()

# CMD position configuiration
appname = 'Windows PowerShell'
width = 800
length = 400
xpos = ScreenWidth - width
ypos = 0


def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if appname in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(hwnd, xpos, ypos, width, length, True)


def changeCmdPosition():
    win32gui.EnumWindows(enumHandler, None)
    
    
    #eof
