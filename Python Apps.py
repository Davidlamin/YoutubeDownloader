from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading


class Application:
    def __init__(self, root):
        self.root = root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.config(bg="#ffdddd")

        # Labels
        top_label = Label(self.root, text="Youtube Download Manager", fg='orange', font=('Type Xero', 70))
        top_label.grid(pady=(0, 10))

        link_label = Label(self.root, text="Please Paste Any YouTube Video Link Below", font=('Type Xero', 30))
        link_label.grid(pady=(0, 20))

        # Entry and Error Labels
        self.youtubeEntryVar = StringVar()
        self.youtubeEntry = Entry(self.root, width=70, textvariable=self.youtubeEntryVar, font=("Agency Fb", 25),
                                  fg='red')
        self.youtubeEntry.grid(pady=(0, 15), ipady=2)

        self.youtubeEntryError = Label(self.root, text="", font=("Concert One", 20))
        self.youtubeEntryError.grid(pady=(0, 8))

        # Directory Selection
        self.youtubeFileSaveLabel = Label(self.root, text="Choose Directory", font=("Concert One", 30))
        self.youtubeFileSaveLabel.grid()

        self.youtubeFileDirectoryButton = Button(self.root, text="Directory", font=("Bell MT", 15),
                                                 command=self.openDirectory)
        self.youtubeFileDirectoryButton.grid(pady=(10, 3))

        self.fileLocationLabel = Label(self.root, text="", font=("Freestyle Script", 25))
        self.fileLocationLabel.grid()

        # Download Type
        self.youtubeChooseLabel = Label(self.root, text="Choose the Download Type", font=("Variety", 30))
        self.youtubeChooseLabel.grid()

        self.downloadChoices = [("Audio MP3", 1), ("Video MP4", 2)]
        self.ChoicesVar = StringVar()
        self.ChoicesVar.set(1)

        # Radio buttons for download choice
        for text, mode in self.downloadChoices:
            youtubeChoice = Radiobutton(self.root, text=text, font=("Northwest old", 15), variable=self.ChoicesVar,
                                        value=mode)
            youtubeChoice.grid()

        # Download Button
        self.downloadButton = Button(self.root, text="Download", width=10, font=("Bell MT", 15),
                                     command=self.checkYoutubeLink)
        self.downloadButton.grid(pady=(30, 5))

    def checkYoutubeLink(self):
        # Match YouTube Link
        self.matchYoutubeLink = re.match(r"^https://www.youtube.com/.", self.youtubeEntryVar.get())
        if not self.matchYoutubeLink:
            self.youtubeEntryError.config(text="Invalid YouTube Link", fg='red')
            return

        # Check if directory is chosen
        if not self.openDirectory():
            self.fileLocationLabel.config(text="Please Choose a Directory", fg='red')
            return

        # Proceed to download window
        self.downloadWindow()

    def openDirectory(self):
        self.FolderName = filedialog.askdirectory()

        if self.FolderName:
            self.fileLocationLabel.config(text=self.FolderName, fg='green')
            return True
        else:
            return False

    def downloadWindow(self):
        self.newWindow = Toplevel(self.root)
        self.root.withdraw()

        # Create a SecondApp instance
        self.app = SecondApp(self.newWindow, self.youtubeEntryVar.get(), self.FolderName, self.ChoicesVar.get())


class SecondApp:
    def __init__(self, downloadWindow, youtubeLink, folderName, choices):
        self.downloadWindow = downloadWindow
        self.youtubeLink = youtubeLink
        self.folderName = folderName
        self.choices = choices
        self.yt = YouTube(self.youtubeLink)

        if self.choices == "1":
            self.video_type = self.yt.streams.filter(only_audio=True).first()
        elif self.choices == "2":
            self.video_type = self.yt.streams.first()

        # Create loading and progress elements
        self.loadingLabel = Label(self.downloadWindow, text="Downloading in Progress...", font=("Small fonts", 40))
        self.loadingLabel.grid(pady=(100, 0))

        self.loadingPercent = Label(self.downloadWindow, text="0%", fg='green', font=("Agency Fb", 40))
        self.loadingPercent.grid(pady=(50, 0))

        # Progress Bar
        self.progressbar = ttk.Progressbar(self.downloadWindow, length=500, orient='horizontal', mode='indeterminate')
        self.progressbar.grid(pady=(50, 0))
        self.progressbar.start()

        # Start download
        threading.Thread(target=self.downloadFile).start()

    def downloadFile(self):
        if self.choices == "1":
            self.yt.streams.filter(only_audio=True).first().download(self.folderName)
        elif self.choices == "2":
            self.yt.streams.first().download(self.folderName)

        self.progressbar.stop()

        # Download completion
        download_finished_label = Label(self.downloadWindow, text="Download Finished", font=("Agency Fb", 30))
        download_finished_label.grid(pady=(150, 0))

        download_filename_label = Label(self.downloadWindow, text=self.yt.title, font=("Terminal", 30))
        download_filename_label.grid(pady=(50, 0))

        # Display file size in MB
        mb_size = self.video_type.filesize / 1_000_000  # Convert to MB
        download_filesize_label = Label(self.downloadWindow, text=f"{mb_size:.2f} MB", font=("Agency Fb", 30))
        download_filesize_label.grid(pady=(50, 0))


if __name__ == "__main__":
    window = Tk()
    window.title("Youtube Download Manager")
    window.state("zoomed")

    app = Application(window)

    mainloop()


