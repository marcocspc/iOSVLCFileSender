# iOSVLCFileSender
A python script to send files to iOS's VLC web interface.

## Usage

- First of all, install python 3 for your distribution.
- After installing python 3, install python pip.
- Then use python pip to install requests_toolbelt module:
`python3 -m pip install requests_toolbelt --user`
- Only after this you will be able to start using the script.
- If you want help about the parameters you need to pass to it, just type:
`python3 uploadToIpad.py` on command line and the script will show you
how to use it.

## Important

- The script is configured to search your iPad using "ipad.lan" DNS.
- If you want to change that, and in most cases it will be necessary,
open the script into your favorite text editor and edit the line `IPAD = "ipad.lan"`
to `IPAD = "whatever.ip.your.ipad.uses"`.

## Hints

- If you want to send big files, don't forget to configure the screen to never
go off and maintain VLC open onto screen, that will prevent iOS from closing VLC.
- If you really want to block your iPad while transferring big files, you can generate
a 10sec white noise (with low volume) audio on Audacity, export it to mp3, upload it using the
script, then put it on VLC, play it and set VLC to repeat the audio forever. Then block the screen.
VLC will be playing the audio, so iOS won't shutdown the application, but remember to stop the audio
playback when the file upload finishes. If you want a more detailed explanation on how to do this, please
tell me! :)

## TODO

- Add e-mail (gmail) notification when file upload is completed.
