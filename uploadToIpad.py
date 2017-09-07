#!/usr/bin/python3

import sys
import os
import requests
from requests_toolbelt.multipart import encoder

#GLOBAL VARIABLES
IPAD = "ipad.lan" #IPAD ip address
FORM = "upload.json" #post page name, do not modify
PAGE_URL = "http://" + IPAD + "/" + FORM #do not modify
PROGRESS_MAXIMUM = 50 # Modify this to change the length of the progress bar

#updates the progress bar
def update_progress(progress):
    barLength = PROGRESS_MAXIMUM
    status = ""

    if isinstance(progress, int):
        progress = float(progress)
    elif not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"

    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    elif progress >= 1:
        progress = 1
        status = "Done...\r\n"

    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    print('\r' + (text), end="")

#creates a callback function (aka the function that is called when progress monitor updates the amount of data sent)
def create_callback(encoder):
    encoder_len = encoder.len

    def print_progress(monitor):
        update_progress(monitor.bytes_read/encoder_len)

    return print_progress

#sends the file
def send_file (file):

    #creates the multipart encoder
    e = encoder.MultipartEncoder(
        fields={'files[]': (os.path.basename(file.name), file, 'text/plain')}
    )

    #creates callback function
    print_progress = create_callback(e)

    #creates the multipart encoder monitor
    m = encoder.MultipartEncoderMonitor(e, print_progress)

    headers= { 'Content-Type': m.content_type }

    #send the file to ipad's vlc
    r = requests.post(PAGE_URL, data=m, headers=headers)

    #if status_code is 200, show that the upload was a success
    if (r.status_code == 200):
        print("Upload done. SUCCESS!")
    else:
        print("Upload ERROR!")
        print(str(r.status_code) + " " + str(r.error))

# --------------------------------MAIN CODE-----------------------------

#get all arguments
arguments = sys.argv

#check if --file-or-dir is set
if ("--file-or-dir" in arguments):

    try:
        #check if file is NOT a directory
        if os.path.isfile(os.path.realpath(arguments[arguments.index("--file-or-dir") + 1])):
            with open(arguments[arguments.index("--file-or-dir") + 1], "rb") as file:
                #send file
                print("Sending file " + os.path.basename(file.name))
                send_file(file)
        elif os.path.isdir(os.path.realpath(arguments[arguments.index("--file-or-dir") + 1])):
            #if argument is a directory, send all file inside directory
            print("Sending all files inside directory.")
            for eachFileName in os.listdir(arguments[arguments.index("--file-or-dir") + 1]):
                with open(eachFileName, "rb") as subFile:
                    print("Sending file " + os.path.basename(subFile.name))
                    send_file(subFile)

    except Exception as e:
        print(str(e))
#else, check if --multiple-files is present
elif ("--multiple-files" in arguments):
    #calculate indexes
    start = arguments.index("--multiple-files") + 1
    end = len(arguments)

    #start a loop to send one file per time, if a directory is found, every
    #file inside that will be uploaded
    for i in range(start, end):
        try:
            with open(arguments[i], "rb") as file:
                #check if file is NOT a directory
                if os.path.isfile(os.path.realpath(file.name)):
                    #send file
                    print("Sending file " + str(i - start + 1) + " of " + str(end - start) + ": " + os.path.basename(file.name))
                    send_file(file)
                elif os.path.isdir(os.path.realpath(file.name)):
                    #send all file inside directory
                    print("Sending all files inside directory.")
                    for subFile in os.listdir(file):
                        print("Sending file " + str(i - start + 1) + " of " + str(end - start) + ": " + os.path.basename(subFile.name))
                        send_file(subFile)
        except Exception as e:
            print(str(e))

else:
    print("Use only --file-or-dir <file_or_dir_path> or --multiple-files <file_1> <file_2> ... <file_x>")
