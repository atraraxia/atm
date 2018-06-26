import wx
import menu

if __name__ == "__main__":
    app = wx.App()
    menu.MyFrame(None).Show()
    app.MainLoop()