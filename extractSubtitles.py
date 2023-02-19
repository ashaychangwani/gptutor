# import os
# import io
# import wave
# from google.cloud import speech_v1p1beta1 as speech
# from argparse import ArgumentParser

# # Create an argument parser to accept the input audio file path
# parser = ArgumentParser(description='Generate subtitles from a WAV audio file')
# parser.add_argument('audio_path', help='Input audio file path')
# args = parser.parse_args()

# # Extract the file name and extension
# file_name, file_ext = os.path.splitext(args.audio_path)

# #Check if the file is a WAV audio file
# if file_ext != '.wav':
#     print("Error: Input file must be a WAV audio file")
#     exit()

# # Load the audio file
# with wave.open(args.audio_path, 'rb') as audio_file:
#     audio_data = audio_file.readframes(audio_file.getnframes())

# # Set up the speech recognition client
# client = speech.SpeechClient()

# # Set the configuration options for the recognition request
# config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=audio_file.getframerate(), language_code="en-US", enable_word_time_offsets=True)

# # Create the recognition request and process the audio data
# audio = speech.RecognitionAudio(content=audio_data)
# response = client.recognize(config=config, audio=audio)

# # Create a new subtitle file with the same name as the audio file
# subtitle_file = file_name + '.srt'

# # Write the captions to the subtitle file
# with io.open(subtitle_file, 'w', encoding='utf-8') as f:
#     for i, result in enumerate(response.results):
#         # Get the start and end times for each result
#         start_time = result.alternatives[0].words[0].start_time
#         end_time = result.alternatives[0].words[-1].end_time

#         # Format the timestamps as SRT format
#         start_time_str = '{:02d}:{:02d}:{:02d},{:03d}'.format(
#             start_time.seconds // 3600, (start_time.seconds % 3600) // 60, 
#             start_time.seconds % 60, start_time.microseconds // 1000)
#         end_time_str = '{:02d}:{:02d}:{:02d},{:03d}'.format(
#             end_time.seconds // 3600, (end_time.seconds % 3600) // 60, 
#             end_time.seconds % 60, end_time.microseconds // 1000)

#         # Write the subtitle number, timestamp, and text to the file
#         f.write(str(i+1) + '\n')
#         f.write(start_time_str + ' --> ' + end_time_str + '\n')
#         f.write(result.alternatives[0].transcript + '\n\n')



#==========================================================================================================
import pvleopard
import os


leopard = pvleopard.create(access_key="DuzTtzBNY2nEekopxTScCjygqVah/iAfO9LyFG9VphSvS0BewfxrQQ==")

# transcript, words = leopard.process_file("C:\\Users\\shubh\\Downloads\\0_GMT20221107-215522_Recording.")
transcript, words = leopard.process_file("C:\\Users\\shubh\\Downloads\\GMT20220907-205510_Recording.wav")

print(transcript)

#==========================================================================================================

# import speech_recognition as sr
# from os import path
# from pydub import AudioSegment

# # # convert mp3 file to wav                                                       
# # sound = AudioSegment.from_mp3("transcript.mp3")
# # sound.export("transcript.wav", format="wav")


# # transcribe audio file                                                         
# AUDIO_FILE = r"C:\\Users\shubh\Downloads\\0_GMT20221107-215522_Recording.wav"

# # use the audio file as the audio source                                        
# r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#         audio = r.record(source)  # read the entire audio file                  

#         print("Transcription: " + r.recognize_google(audio))

