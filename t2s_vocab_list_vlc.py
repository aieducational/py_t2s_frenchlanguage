from gtts import gTTS
from pydub import AudioSegment
import os
import time
import openpyxl

# Specify the path to your Excel file containing French words
excel_file_path = os.path.expanduser("~/Documents/Duolingo/wordlist.xlsx")

# Load the Excel file and select the appropriate sheet (modify as needed)
workbook = openpyxl.load_workbook(excel_file_path)
sheet = workbook.active  # You can change this to select a specific sheet if needed

# Extract French words from the Excel sheet
word_column = 1  # Assuming the French words are in the first column (A)

words = []
for row in sheet.iter_rows(min_col=word_column, max_col=word_column, values_only=True):
    for cell_value in row:
        if cell_value is not None:
            words.append(str(cell_value).strip())

# Set the path for saving the concatenated audio file
output_directory = os.path.expanduser("~/python")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

output_path = os.path.join(output_directory, "output.mp3")

# Generate individual audio segments and concatenate them
all_audio_segments = []
for word in words:
    tts = gTTS(word, lang='fr')  # 'fr' is the language code for French
    tts.save("temp.mp3")  # Temporary file for each word
    audio_segment = AudioSegment.from_mp3("temp.mp3")
    all_audio_segments.append(audio_segment)
    os.remove("temp.mp3")

concatenated_audio = AudioSegment.silent(duration=0)  # Create a silent segment to start

for audio_segment in all_audio_segments:
    concatenated_audio += audio_segment + AudioSegment.silent(duration=5000)  # 5-second pause

# Save the concatenated audio
concatenated_audio.export(output_path, format="mp3")

# Play the generated audio file using VLC
os.system(f"vlc {output_path}")

# Close the Excel file
workbook.close()
