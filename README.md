## Get Started

1. Set the site_dir variable in the process.sh file to the directory where you wish to store the movie transcripts and mp3 data.
2. run `pip install -r requirements.txt` to install the required dependencies.


## Command Usage

./process.sh --audio-track 3 01_使徒、襲来.ass 01_使徒、襲来.mkv

This command fetches the movie transcript from the subtitle file (.ass file) and the third audio track in the file and
creates an html page where each subtitle dialogue is displayed. Each sentence has a button next to it, which will play
the dialogue from the extracted mp3 file.
*N.B: As an mp3 file will be extracted from the movie file, this command will take up disk space.*

You can also provide just the subtitle file and the script will only generate the webpage containing the transcript:

./process.sh 01_使徒、襲来.ass

Generated web page example: 
<img width="1205" alt="example-page" src="https://github.com/DavideP98/jp-sentence-mining/assets/36838126/28954d98-df52-42f2-aeae-c3e4601c9118">
