from gui_dialogs import SecondsInput, CutDialog
from video_editor import VideoEditor
import os
import wx
import wx.media

dirName = os.path.dirname(os.path.abspath(__file__))


class MainFrame(wx.Frame):
    def __init__(self, editor):
        wx.Frame.__init__(self, None, -1, "Video editor", wx.DefaultPosition, wx.Size(800, 600))
        splitter = wx.SplitterWindow(self)
        self.editor = editor
        self.controls_panel = wx.Panel(splitter, style=wx.BORDER_SUNKEN)
        self.cp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_controls()
        self.controls_panel.SetSizer(self.cp_sizer)
        storage_splitter = wx.SplitterWindow(splitter)
        self.videos = wx.Panel(storage_splitter, style=wx.BORDER_SUNKEN)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.videos.SetSizer(self.v_sizer)
        v_t = wx.StaticText(self.videos, -1, 'Video fragments:')
        self.v_sizer.Add(v_t)
        self.add_video_button(0).SetFocus()
        self.images = wx.Panel(storage_splitter, style=wx.BORDER_SUNKEN)
        self.i_sizer = wx.BoxSizer(wx.VERTICAL)
        self.images.SetSizer(self.i_sizer)
        i_t = wx.StaticText(self.images, -1, 'Images:')
        self.i_sizer.Add(i_t)
        storage_splitter.SplitVertically(self.videos, self.images)
        storage_splitter.SetSashGravity(0.5)
        splitter.SplitHorizontally(storage_splitter, self.controls_panel)
        splitter.SetSashGravity(0.9)
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        import_image = file_menu.Append(-1, '&Import image \tCtrl+I', 'click here to add an image in a project')
        self.Bind(wx.EVT_MENU, self.on_import, import_image)
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

    def add_video_button(self, idx):
        v_btn = wx.Button(self.videos, id=idx, label=self.editor.video_names[idx])
        self.v_sizer.Add(v_btn)
        v_btn.Bind(wx.EVT_BUTTON, self.change_video_selection)
        self.videos.Layout()
        return v_btn

    def add_image_button(self, idx):
        i_btn = wx.Button(self.images, id=idx, label=self.editor.image_names[idx])
        self.i_sizer.Add(i_btn)
        i_btn.Bind(wx.EVT_BUTTON, self.change_image_selection)
        self.images.Layout()
        return i_btn

    def change_video_selection(self, event):
        self.editor.change_selected_video(event.Id)

    def change_image_selection(self, event):
        self.editor.change_selected_image(event.Id)

    def add_controls(self):
        self.add_control(wx.Button(self.controls_panel, label='CUT'), self.cut)
        self.add_control(wx.Button(self.controls_panel, label='CONCAT'), self.concat)
        self.add_control(wx.Button(self.controls_panel, label='ADD IMAGE'), self.add_image)
        self.add_control(wx.Button(self.controls_panel, label='SAVE'), self.save)

    def add_control(self, btn, handler):
        btn.Bind(wx.EVT_BUTTON, handler)
        self.cp_sizer.Add(btn)

    def cut(self, event):
        dialog = CutDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            start = dialog.sld_1.GetValue()
            end = dialog.sld_2.GetValue()
            if start > end:
                start, end = end, start
            self.editor.cut_fragment(start, end),
            self.add_video_button(self.editor.get_video_length() - 1)
        dialog.Destroy()

    def concat(self, event):
        selected = self.editor.video_names[self.editor.video_idx]
        ch = wx.SingleChoiceDialog(None, 'Choose a fragment to add to {}'.format(selected), 'Choosing fragment',
                                   self.editor.video_names)
        if ch.ShowModal() == wx.ID_OK:
            selection = ch.GetSelection()
            self.editor.concat_fragments(selection)
        ch.Destroy()
        self.add_video_button(self.editor.get_video_length() - 1)

    def add_image(self, event):
        dialog = SecondsInput(self)
        if dialog.ShowModal() == wx.ID_OK:
            self.editor.connect_image(dialog.e.GetValue()),
            self.add_video_button(self.editor.get_video_length() - 1)
        dialog.Destroy()

    def save(self, event):
        dir_path = wx.DirSelector('Choose a folder to save the file')
        if dir_path != '':
            dlg = wx.TextEntryDialog(None, 'Enter new file name', 'Saving file')
            dlg.SetValue(self.editor.video_names[self.editor.video_idx])
            if dlg.ShowModal() == wx.ID_OK:
                file_name = dlg.GetValue()
                try:
                    self.editor.save_result(os.path.join(dir_path, file_name))
                except FileExistsError as e:
                    wx.MessageBox(e.strerror, 'Error', wx.ICON_ERROR)
            dlg.Destroy()

    def on_import(self, event):
        dialog = wx.FileDialog(None, "Choose an image to import", wildcard="Image (*.jpg; *.png)|*.jpg; *.png",
                               style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.editor.add_image(os.path.join(dialog.GetDirectory(), dialog.GetFilename()))
            self.editor.change_selected_image(self.editor.get_image_length() - 1)
            self.add_image_button(len(self.editor.images_list) - 1).SetFocus()


def main():
    app = wx.App()
    file_selector = wx.FileSelector(message="Choose a video file to work with", wildcard="Video file (*.mp4)|*.mp4")
    if file_selector != "":
        editor = VideoEditor(file_selector)
        fr = MainFrame(editor)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(dirName, "icon.png")))
        fr.SetIcon(icon)
        fr.SetSize(600, 600)
        fr.Show()
        app.MainLoop()
    else:
        wx.MessageBox("File is not selected. Application would be closed.", 'Error', wx.OK | wx.ICON_ERROR)
        app.Destroy()


if __name__ == "__main__":
    main()
