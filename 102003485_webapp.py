import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from moviepy.editor import *


def send_mail(email_id,resultfile):
    fromaddr = "simranmangat700@gmail.com"
    toaddr = email_id
   
# instance of MIMEMultipart
    msg = MIMEMultipart()
  
# storing the senders email address  
    msg['From'] = fromaddr
  
# storing the receivers email address 
    msg['To'] = toaddr
  
# storing the subject 
    msg['Subject'] = "Singer's Mashup!" 
  
# string to store the body of the mail
    body = '''For your chosen singer here is the mashup :'''
  
# attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
  
# open the file to be sent 
    # filename = resultfile
    # attachment = open(resultfile, "rb")

    with open(resultfile, 'rb') as f:
        audio = MIMEAudio(f.read(),_subtype="mp3")
    
    audio.add_header('Content-Disposition', 'attachment', filename='Mashup.mp3')
    msg.attach(audio)
  
# creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
    s.starttls()
  
# Authentication
    s.login(fromaddr,"ttgyiwytvhlxfmwi")
  
# Converts the Multipart msg into a string
    text = msg.as_string()
  
# sending the mail
    s.sendmail(fromaddr, toaddr, text)
  
# terminating the session
    s.quit()


def mashup(singer,x,y,email_id):

    # if len(sys.argv)!=4:
    #     print("Incorrect Number of Parameters")
    #     exit(0)
    # else:
    if(int(x)<10):
        print("Videos must be greater than 10")
        exit(0)
             
    if(int(y)<20):
            print("Trim size should be greater than 20sec")
            exit(0)
        # if (".mp3" != (os.path.splitext(sys.argv[4]))[1]):
        #             print("ERROR : Output file extension is wrong")
        #             exit(0)

    from youtube_search import YoutubeSearch
    name=singer
    n=int(x)
    duration=int(y)
    results = YoutubeSearch(name, max_results=n).to_dict()
    link=['https://www.youtube.com/'+results[i]['url_suffix'] for i in range(n)]
    from pytube import YouTube
    def Download(link):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_lowest_resolution()
        try:
            youtubeObject.download()
        except:
            print("An error has occurred")
        print("Download is completed successfully")
        # print("Downloading File "+str(i+1)+" .......")

    for i in range(0,n):    
        Download(link[i])

    directory = os.getcwd()


    files = os.listdir(directory)


    mp4_files = [file for file in files if file.endswith('.mp4')]

    # for file in mp4_files:
    #     print(file)

    # print(mp4_files)

    from moviepy.editor import VideoFileClip,AudioFileClip

    for i in range(0,len(mp4_files)):
        video = VideoFileClip(mp4_files[i])
        audio = video.audio
        audio.write_audiofile("audio_file"+str(i)+".mp3")

    from pydub import AudioSegment



    directory = os.getcwd()

    files = os.listdir(directory)

    mp3_files = [file for file in files if file.endswith('.mp3')]

    # for file in mp3_files:
    #     print(file)



    # Load the audio file
    audio = AudioFileClip(mp3_files[0])

    # Trim the audio file
    merged_audio = audio.subclip(0,0)
            

    for i in range(0,len(mp3_files)):
        audio = AudioFileClip(mp3_files[i])
        trimmed=audio.subclip(0,duration)
        merged_audio = concatenate_audioclips([merged_audio, trimmed])
    name1="mashup.mp3"
    merged_audio.write_audiofile(name1)

    send_mail(email_id,name1)


    st.success("Check your email, result audio file is successfully sent")
    


st.title("Mashup facility")
if __name__ == "__main__":

    singer= st.text_input("Enter the singer name")
    x= st.text_input("Enter number of videos")
    y= st.text_input("Enter duration of each video")
    email_id= st.text_input("Enter email id")
     
    submit_button=st.button("Send")
    if submit_button:
                    try:
                  
                        # df = pd.read_csv(file)
                        mashup(singer,x,y,email_id)
               
#                         delete_after_use=True
#                         if delete_after_use:
#                             for i in range(int(x)):
#                                 if os.path.exists("audio_file"+str(i)+".mp3"):
#                                     os.remove("audio_file"+str(i)+".mp3")
                    except Exception as e:
                        st.error(e)      
