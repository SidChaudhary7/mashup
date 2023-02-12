import streamlit as st
from youtubepy import Video
import os
import smtplib
import pandas as pd
from youtube_search import YoutubeSearch
from pytube import YouTube
from moviepy.editor import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# if len(sys.argv)!=5:
#     print("Incorrect Number of Parameters")
#     exit(0)
# else:
#     if(int(sys.argv[2])<=10):
#         print("Videos must be greater than 10")
#         exit(0)
#     if(int(sys.argv[3])<=20):
#         print("Trim size should be greater than 20sec")
#         exit(0)
#     if (".mp3" != (os.path.splitext(sys.argv[4]))[1]):
#                 print("ERROR : Output file extension is wrong")
#                 exit(0)



#name = name of the singer

# name=sys.argv[1]

# n=number of videos you want to download

# n=int(sys.argv[2])

def send_email_with_attachment(email, password, to, subject, body, file_path):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    with open(file_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', "attachment; filename= %s" % file_path)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, msg.as_string())
    server.quit()

def make_video(name,n,time):
    results = YoutubeSearch(name, max_results=n).to_dict()

    new = pd.DataFrame.from_dict(results)  

    df=new['url_suffix']
    df='https://youtube.com'+df

    for i in range(len(df)):
        video = YouTube(df.loc[i]).streams.filter(only_audio=True).first().download()
        base, ext = os.path.splitext(video)
        new_file = base + '.mp3'
        os.rename(video, new_file)
       
    directory = 'c:/Users/SIDDHARTH CHAUDHARY/Desktop/assignment-2'
    files = os.listdir(directory)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    for file in mp3_files:
        print(file)

    ad = AudioFileClip(mp3_files[0])
    merged_audio=ad.subclip(0,0)

# time=int(sys.argv[3])
    for i in range(0,len(mp3_files)):
        audio = AudioFileClip(mp3_files[i])
        trimmed_audio = audio.subclip(0, time)
        merged_audio = concatenate_audioclips([merged_audio, trimmed_audio])

    merged_audio.write_audiofile("out.mp3")


def main():
    result="Your request have been sent"
    st.title("welcome to song mashup")
    name=st.text_input("Enter Singer Name","Type Here...")
    n=st.number_input("Enter number of videos",min_value=11)
    time=st.number_input("Enter duration of each video",min_value=21)
    rec_email = st.text_input("Enter Email")
    # /email=st.text_input("Enter email id","Type Here...")
    if st.button("Submit"):
        make_video(name,n,time)
        st.success(result)
        email = "siddharthchaudhary0007@gmail.com"
        password = "siddharth0007"
        to = rec_email
        subject = "Email with Attachment from Streamlit app"
        body = "This is a test email with attachment sent from a Streamlit app."
        file_path = os.getcwd()+"/out.mp3"
        send_email_with_attachment(email, password, to, subject, body, file_path)
        st.subheader("MAIL sent")

if __name__=='__main__':
    main()

