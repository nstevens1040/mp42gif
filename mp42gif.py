import argparse
import ffmpeg
import io
import tkinter as tk
from tkinter import filedialog as fd
import os
import sys
import colorama
from colorama import Fore,Back,Style,init
import shutil

init()
parser = argparse.ArgumentParser(description='Specify how your video gets converted into a GIF')
parser.add_argument(
    '--slice',
    action='store_true',
    dest='should_slice',
    help='--slice --starttime <int>(start time in seconds) --stoptime <int>(end time in seconds) :: both arguments reflect the amount of seconds from the beginning of the video',
    default=None,
    required=False
)
parser.add_argument(
    '--starttime', 
    action='append', 
    dest='slice_time',
    type=int,
    help='--starttime <int>(start time in seconds from the beginning of the video)',
    default=None,
    required='--slice' in sys.argv
)
parser.add_argument(
    '--stoptime', 
    action='append', 
    dest='slice_time',
    type=int,
    help='--stoptime <int>(stop time in seconds from the beginning of the video)',
    default=None,
    required='--slice' in sys.argv
)
parser.add_argument(
    '--playbackrate',
    action='store',
    dest='pbrate',
    type=float,
    help='--playbackrate <float>(integer or decimal that is non-negative, non-zero, & not 1) :: numbers greater than 1 speed the video up and numbers between 0 and 1 slow the video down',
    default=None,
    required=False
)
parser.add_argument(
    '--blend',
    action='store_true',
    dest='should_blend', 
    help='--blend <bool>(true or false) :: Determines whether the video gets "minterpolated"',
    default=None,
    required=False
)
results = parser.parse_args()

print(Style.BRIGHT)
for i in list(range(0,90)):
    print(Fore.WHITE + '#', end='')
print(Fore.WHITE + '#')
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888b     d888 8888888b.     d8888            Y88b          .d8888b.  8888888 8888888888 ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "8888b   d8888 888   Y88b   d8P888             Y88b        d88P  Y88b   888   888        ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "88888b.d88888 888    888  d8P 888              Y88b       888    888   888   888        ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888Y88888P888 888   d88P d8P  888       888888  Y88b      888          888   8888888    ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888 Y888P 888 8888888P\" d88   888               d88P      888  88888   888   888        ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888  Y8P  888 888       8888888888      888888 d88P       888    888   888   888        ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888   \"   888 888             888             d88P        Y88b  d88P   888   888        ", end='')
print(Fore.WHITE + "#")
print(Fore.WHITE + "# ", end='')
print(Fore.YELLOW + "888       888 888             888            d88P          \"Y8888P88 8888888 888        ", end='')
print(Fore.WHITE + "#")

for i in list(range(0,90)):
    print(Fore.WHITE + '#', end='')
print(Fore.WHITE + '#')

def cls():
    import os
    import sys
    if not sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')

def openafile():
    master = tk.Tk()
    master.title("Open your MP4 file")
    def callback():
        global TIOW
        TIOW=fd.askopenfile()
        master.destroy()
    tk.Label(master,text="Click 'Next' and then select your MP4 file.").grid(row=0)
    tk.Button(master,text='Next',command=callback).grid(row=1)
    master.attributes("-topmost", True)
    tk.mainloop()

def mp4Slice(VIDIN,startframe,endframe):
    os.mkdir(WORKDIR + "/slice/")
    VIDOUT = WORKDIR + "/slice/" + VIDIN.split("/")[(len(VIDIN.split("/")) - 1)] # Full path to output video
    INPATH = []
    count = 0
    for i in VIDIN.split('/'):
        if count > (len(VIDIN.split('/')) - 4):
            INPATH.append(i)
        count = count + 1
    
    INDIR = '/'.join(INPATH)
    VIDPATH = []
    count = 0
    for i in VIDOUT.split('/'):
        if count > (len(VIDOUT.split('/')) - 4):
            VIDPATH.append(i)
        count = count + 1
    
    VIDDIR = '/'.join(VIDPATH)
    print(Fore.GREEN + "Slicing:\n    ", end='')
    print(Fore.YELLOW + "'./" + INDIR + "'")
    print(Fore.WHITE + "        start_frame:",end='')
    print(Fore.YELLOW + "    " + str(startframe))
    print(Fore.WHITE + "        end_frame:",end='')
    print(Fore.YELLOW + "      " + str(endframe)) 
    print(Fore.GREEN + "Sliced output file will be saved to:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDDIR + "'")
    try:
        ffmpeg.run(ffmpeg.output(ffmpeg.input(VIDIN).trim(start_frame=results.startframe,end_frame=results.endframe),VIDOUT),capture_stdout=True, capture_stderr=True, input=None, quiet=True, overwrite_output=True)
    except:
        ERRCATCH = 1
    GARBAGE.append(VIDOUT)
    GARBAGE.append(WORKDIR + "/slice")
    return VIDOUT

def dRate(VIDIN,RATE=0.5):
    INPATH = []
    count = 0
    for i in VIDIN.split('/'):
        if count > (len(VIDIN.split('/')) - 4):
            INPATH.append(i)
        count = count + 1
    
    INDIR = '/'.join(INPATH)
    FOLRA = []
    count = 0
    for i in VIDIN.split("."):
        if count < (len(VIDIN.split(".")) - 1):
            FOLRA.append(i)
        count = count + 1
    INVE = float(1) / float(RATE) # Value needed for 'setpts' is the inverse of 'pbrate'
    PTS = str(INVE) + '*PTS' # Create string for 'setpts'
    os.mkdir(WORKDIR + "/rate/") # New folder with same name as previous mkdir command, but with '_rate_' appended
    VIDOUT = WORKDIR + "/rate/" + VIDIN.split("/")[(len(VIDIN.split("/")) - 1)] # Full path to output video
    VIDPATH = []
    count = 0
    for i in VIDOUT.split('/'):
        if count > (len(VIDOUT.split('/')) - 4):
            VIDPATH.append(i)
        count = count + 1
    
    VIDDIR = '/'.join(VIDPATH)
    print(Fore.GREEN + "Setting playback rate for:\n    ", end='')
    print(Fore.YELLOW + "'./" + INDIR + "'")
    print(Fore.WHITE + "        to: ", end='')
    print(Fore.YELLOW + str(RATE))
    print(Fore.GREEN + "Resultant video will be saved to:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDDIR + "'")
    try:
        LOG2 = ffmpeg.run(ffmpeg.output(ffmpeg.input(VIDIN).setpts(PTS),VIDOUT),capture_stdout=True, capture_stderr=True, input=None, quiet=True, overwrite_output=True)
    except:
        ERRCATCH = 1
    GARBAGE.append(VIDOUT)
    GARBAGE.append(WORKDIR + "/rate")
    return VIDOUT

def blend(VIDIN):
    FOLRA = []
    count = 0
    for i in VIDIN.split("/"):
        if count > (len(VIDIN.split("/")) - 4):
            FOLRA.append(i)
        count = count + 1
    VIDP = '/'.join(FOLRA)
    PROBE=ffmpeg.probe(VIDIN) # Probe for video data
    FPS=int(PROBE['streams'][0]['avg_frame_rate'].split('/')[0]) / int(PROBE['streams'][0]['avg_frame_rate'].split('/')[1]) # determine video FPS as a decimal 
    os.mkdir(WORKDIR + "/blend/") # New folder with same name as previous mkdir command, but with '_rate_' appended
    VIDOUT = WORKDIR + "/blend/" + VIDIN.split("/")[(len(VIDIN.split("/")) - 1)] # Full path to output video
    VIDPATH = []
    count = 0
    for i in VIDOUT.split('/'):
        if count > (len(VIDOUT.split('/')) - 4):
            VIDPATH.append(i)
        count = count + 1
    
    VIDDIR = '/'.join(VIDPATH)
    print(Fore.GREEN + "Blending frames for:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDP + "'")
    print(Fore.GREEN + "Resultant output file will be saved to:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDDIR + "'")
    
    try:
        ffmpeg.run(ffmpeg.output(ffmpeg.input(VIDIN).filter('minterpolate',round(FPS,2),"blend"),VIDOUT),capture_stdout=True, capture_stderr=True, input=None, quiet=True, overwrite_output=True)
    except:
        ERRCATCH = 1
    GARBAGE.append(VIDOUT)
    GARBAGE.append(WORKDIR + "/blend")
    return VIDOUT

def palette(VIDIN):
    FOLRA = []
    count = 0
    for i in VIDIN.split("."):
        if count < (len(VIDIN.split(".")) - 1):
            FOLRA.append(i)
        count = count + 1
    PAL = WORKDIR + "/palette.png" # Full path to palette.png file
    VIDPATH = []
    count = 0
    for i in VIDIN.split('/'):
        if count > (len(VIDIN.split('/')) - 4):
            VIDPATH.append(i)
        count = count + 1
    
    VIDDIR = '/'.join(VIDPATH)
    PNGPATH = []
    count = 0
    for i in PAL.split('/'):
        if count > (len(PAL.split('/')) - 4):
            PNGPATH.append(i)
        count = count + 1
    
    PNGDIR = '/'.join(PNGPATH)
    print(Fore.GREEN + "Creating reference palette for:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDDIR + "'")
    print(Fore.GREEN + "Saving reference palette to:\n    ", end='')
    print(Fore.YELLOW + "'./" + PNGDIR + "'")
    try:
        ffmpeg.run(ffmpeg.output(ffmpeg.input(VIDIN).filter('palettegen',256,False,'ffffff','diff'),PAL),capture_stdout=True, capture_stderr=True, input=None, quiet=True, overwrite_output=True)
    except:
        ERRCATCH = 1
    GARBAGE.append(PAL)
    GARBAGE.append(WORKDIR)
    return PAL

def mkGIF(VIDIN,PAL):
    OUTFO = []
    count = 0
    for i in WORKDIR.split('/'):
        if count < (len(WORKDIR.split('/')) -1):
            OUTFO.append(i)
        count = count + 1
    OUTDIR = '/'.join(OUTFO)
    OUTNAME = []
    count = 0
    for i in (VIDIN.split('/')[(len(VIDIN.split('/')) - 1)]).split('.'):
        if count < (len((VIDIN.split('/')[(len(VIDIN.split('/')) - 1)]).split('.')) -1):
            OUTNAME.append(i)
        count = count + 1
    OUTFILE = '/'.join(OUTNAME)
    GIF = OUTDIR + "/" + OUTFILE + ".gif" # Full path to GIF file

    VIDPATH = []
    count = 0
    for i in VIDIN.split('/'):
        if count > (len(VIDIN.split('/')) - 4):
            VIDPATH.append(i)
        count = count + 1
    
    VIDDIR = '/'.join(VIDPATH)
    GIFPATH = []
    count = 0
    for i in GIF.split('/'):
        if count > (len(GIF.split('/')) - 4):
            GIFPATH.append(i)
        count = count + 1
    
    GIFDIR = '/'.join(GIFPATH)
    print(Fore.GREEN + "Creating GIF file from:\n    ", end='')
    print(Fore.YELLOW + "'./" + VIDDIR + "'")
    print(Fore.GREEN + "    Saving GIF file to:\n    ", end='')
    print(Fore.YELLOW + "'./" + GIFDIR + "'")
    try:
        ffmpeg.run(ffmpeg.output(ffmpeg.overlay(
            ffmpeg.filter(
                [
                    ffmpeg.input(VIDIN).filter_multi_output('split')[1], # Video stream copy 2 from 'split' filter
                    ffmpeg.input(PAL) # Stream from PNG palette 
                ],
                'paletteuse'
            ),
            ffmpeg.input(VIDIN).filter_multi_output('split').stream(0) # Video stream copy 1 from 'split' filter
        ),GIF),capture_stdout=True, capture_stderr=True, input=None, quiet=True, overwrite_output=True)
    except:
        ERRCATCH = 1
    return GIF

global ERRCATCH
global GARBAGE
global WORKDIR
ERRCATCH = 0
GARBAGE = []

openafile()
VIDIN = TIOW.name
startframe = 916
endframe = 1363

FOLRA = []
count = 0
for i in VIDIN.split("."):
    if count < (len(VIDIN.split(".")) - 1):
        FOLRA.append(i)
    count = count + 1
WORKDIR = ".".join(FOLRA)
os.mkdir(WORKDIR) # Create new folder named after the video file
print(Fore.GREEN + "Working directory:\n    ",end='')
print(Fore.YELLOW + WORKDIR + '/')

if ERRCATCH == 0:
    if results.should_slice:
        if not results.slice_time[0] == None and not results.slice_time[1] == None:
            OUTVID = mp4Slice(VIDIN,results.slice_time[0],results.slice_time[1])
            if ERRCATCH == 0:
                print(Fore.WHITE + "        Slicing succeeded!\n")
            else:
                print(Fore.RED + "Slicing failed!`n")
    else:
        OUTVID = VIDIN
    if ERRCATCH == 0:
        if not results.pbrate == None:
            OUTVID = dRate(OUTVID,results.pbrate)
            if ERRCATCH == 0:
                print(Fore.WHITE + "        Playback rate change succeeded!\n")
            else:
                print(Fore.RED + "Playback rate reduction failed!`n")
        if ERRCATCH == 0:
            if results.should_blend:
                OUTVID = blend(OUTVID)
                if ERRCATCH == 0:
                    print(Fore.WHITE + "        Frame blending succeeded!\n")
                else:
                    print(Fore.RED + "Frame blending failed!`n")
            if ERRCATCH == 0:
                PAL = palette(OUTVID)
                if ERRCATCH == 0:
                    print(Fore.WHITE + "        Reference palette creation succeeded!\n")
                    OUTGIF = mkGIF(OUTVID,PAL)
                    if ERRCATCH == 0:
                        print(Fore.WHITE + "        GIF creation succeeded!\n")
                        print(Fore.YELLOW + "Cleaning up intermediate files:")
                        for fsitem in GARBAGE:
                            if os.path.isfile(fsitem):
                                VIDPATH = []
                                count = 0
                                for i in fsitem.split('/'):
                                    if count > (len(fsitem.split('/')) - 4):
                                        VIDPATH.append(i)
                                    count = count + 1

                                VIDDIR = '/'.join(VIDPATH)
                                print(Fore.RED + "    Deleting: ", end='')
                                print(Fore.YELLOW + "./" + VIDDIR)
                                os.remove(fsitem)
                            else:
                                VIDPATH = []
                                count = 0
                                for i in fsitem.split('/'):
                                    if count > (len(fsitem.split('/')) - 4):
                                        VIDPATH.append(i)
                                    count = count + 1
                                
                                VIDDIR = '/'.join(VIDPATH)
                                print(Fore.RED + "    Deleting: ", end='')
                                print(Fore.YELLOW + "./" + VIDDIR + '/')
                                shutil.rmtree(fsitem)
                    else:
                        print(Fore.RED + "GIF creation failed!`n")
                else:
                    print(Fore.RED + "Reference palette creation failed!`n")

