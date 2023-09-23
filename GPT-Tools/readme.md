## GPT / OpenAI API for the command line
### Commands:
#### Translation from a video file (need FFMPEG):
* python gpt.py --translate --file "F:\gpt\Movie Name (2012).mp4" --start 00:11:13 --end 00:00:15
* _File paths with spaces in the path/file name need quotes as shown above_

#### Image generation from prompt or prompt in file:
* python gpt.py --img --name otter3 --prompt "Majestic eagle icon in military cyber style"
* python gpt.py --img --name otter3 --file prompt.txt

## Video summary screenshot:

![alt text](https://raw.githubusercontent.com/n0x5/scripts/master/GPT-Tools/test.png "Title")
