import os
import wx
import markdownConverter

app = wx.App()

dialog = wx.FileDialog(None, "Choose a file to convert", "", "", "*.md", wx.FD_OPEN)
if (dialog.ShowModal() == wx.ID_OK):
	filename = os.path.join(dialog.GetDirectory(), dialog.GetFilename())
	markdownConverter.convert_markdown(filename)

app.MainLoop()
