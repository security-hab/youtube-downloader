import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pytubefix import YouTube

# Create main app window
app = ctk.CTk(fg_color='black')
app.title('YouTube Downloader')
app.geometry('300x300+700+200')
app.resizable(False, False)
app.iconbitmap('img/video.ico')

# Button dimensions
btnWidth: int = 100
btnHeight: int = 25
directory: str = ''  # Directory for saving the video

# Progress bar variable
progressVar = ctk.DoubleVar()
progressBar = ctk.CTkProgressBar(app, variable=progressVar)

# Images for the buttons
imgBtn = ctk.CTkImage(dark_image=Image.open('img/apps.png'), size=(15, 15))
imgPathBtn = ctk.CTkImage(dark_image=Image.open('img/folder.png'), size=(15, 15))
imgLabel = ctk.CTkImage(dark_image=Image.open('img/youtube.png'), size=(20, 20))

# Configure grid layout for the window
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

# Function to handle video download
def videoDownload():
    if not directory:
        messagebox.showwarning(
            'Error', 'Please select the directory where the file will be saved!')
        return
    try:
        yt = YouTube(entryLabel.get(), on_progress_callback=onProgress)  # Initialize YouTube object
        video_stream = yt.streams.get_highest_resolution()  # Get highest resolution stream
        progressVar.set(0)
        progressBar.grid(row=2, column=0, columnspan=2,
                         padx=10, pady=5, sticky='ew')
        app.update()  # Update the window to show progress bar
        video_stream.download(output_path=directory, filename='video.mp4')  # Download the video
        progressVar.set(1)
        messagebox.showinfo('Success', 'Your video has been successfully downloaded!')
    except Exception as ex:
        progressVar.set(0)
        messagebox.showerror('Error', f'An error occurred: {ex}')

# Callback function to update progress bar during video download
def onProgress(stream, chunk, bytes_remaining):
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytes_remaining
    progressVar.set(bytesDownloaded / totalSize)  # Update progress bar
    app.update_idletasks()  # Update the window with the new progress

# Function to allow user to select a directory for saving the video
def fileDirectory():
    global directory
    directory = filedialog.askdirectory()

    if directory:
        messagebox.showinfo(
            'Path', f'The file will be saved to the directory:\n{directory}')

# Function to paste text from clipboard into URL entry field
def pasteText(event=None):
    try:
        clipboardText = app.clipboard_get()  # Get text from clipboard
        if clipboardText:
            entryLabel.delete(0, tk.END)
            entryLabel.insert(0, clipboardText)  # Insert clipboard text into entry field
        else:
            entryLabel.delete(0, tk.END)
            entryLabel.insert(0, 'Clipboard is empty')  # If clipboard is empty, show a message
    except tk.TclError:
        entryLabel.delete(0, tk.END)
        entryLabel.insert(0, 'Error: Clipboard is empty')  # Handle error if clipboard is empty

# Bind paste action to Ctrl + V
app.bind('<Control-v>', lambda event: pasteText())

# Main title label
mainTitleLabel = ctk.CTkLabel(app, text='YouTube Downloader ',
                              font=('JetBrains Mono', 15, 'bold'), image=imgLabel, compound='right')
mainTitleLabel.grid(row=1, column=0, pady=10, columnspan=2, sticky='n')

# URL entry field
entryLabel = ctk.CTkEntry(app, placeholder_text='Enter URL link',
                          font=('JetBrains Mono', 12, 'bold'))
entryLabel.grid(row=1, column=0, pady=1, padx=5, sticky='ew', columnspan=2)

# Download button
entryBtn = ctk.CTkButton(app, text='Download', command=videoDownload, width=btnWidth, height=btnHeight, cursor='hand2',
                         font=('JetBrains Mono', 11, 'bold'),
                         image=imgBtn,
                         compound='right',
                         fg_color='red')
entryBtn.grid(row=1, column=0, padx=5, sticky='se')
entryLabel.bind('<Control-V>', pasteText)

# Path selection button
fileBtn = ctk.CTkButton(app, text='Path', command=fileDirectory, width=btnWidth, height=btnHeight, cursor='hand2',
                        font=('JetBrains Mono', 11, 'bold'),
                        image=imgPathBtn,
                        compound='right',
                        fg_color='red')
fileBtn.grid(row=1, column=1, padx=10, sticky='sw')

# Author label
authorLabel = ctk.CTkLabel(app, text='By security-hab',
                           fg_color='red',
                           font=('JetBrains Mono', 12, 'bold'))
authorLabel.grid(row=2, column=0, columnspan=2, sticky='sew')

# Run the app main loop
app.mainloop()
