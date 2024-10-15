import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os

# Function to browse and select an audio file
def browse_file():
    global audio_file
    audio_file = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.flac *.m4a"), ("All Files", "*.*"))
    )
    file_label.config(text=os.path.basename(audio_file))

# Function to browse the save location for the transcription file
def save_file():
    global output_file
    output_file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        title="Save Transcription As"
    )

# Function to transcribe the audio and save to a text file
def transcribe_audio():
    if not audio_file or not output_file:
        messagebox.showerror("Error", "Please select an audio file and save location.")
        return

    selected_model = model_var.get()

    # Load the selected model
    model = whisper.load_model(selected_model)
    
    # Perform the transcription
    result = model.transcribe(audio_file)
    transcription = result['text']

    # Save the transcription to a text file
    with open(output_file, 'w') as f:
        f.write(transcription)
    
    messagebox.showinfo("Success", f"Transcription saved to {output_file}")

# Create the main window
root = tk.Tk()
root.title("Whisper Audio Transcription")
root.geometry("400x300")

# Add widgets to select audio file
tk.Label(root, text="Select Audio File:").pack(pady=10)
file_label = tk.Label(root, text="No file selected")
file_label.pack()
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

# Dropdown menu to select the Whisper model
tk.Label(root, text="Select Model:").pack(pady=10)
model_var = tk.StringVar(value="base")
model_options = ["tiny", "base", "small", "medium", "large", "turbo"]
tk.OptionMenu(root, model_var, *model_options).pack()

# Button to select the output file location
tk.Button(root, text="Save Transcription As", command=save_file).pack(pady=10)

# Button to start transcription
tk.Button(root, text="Transcribe", command=transcribe_audio).pack(pady=20)

# Start the main loop
root.mainloop()