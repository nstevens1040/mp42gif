# mp42gif
Python script to convert an MP4 file into an animated GIF.  
# Quick Start  
Download the executable  
   - **Windows**  
```ps1
iwr "https://github.com/nstevens1040/mp42gif/releases/download/v1.0.0/mp42gif.exe" -OutFile "mp42gif.exe"
Unblock-File .\mp42gif.exe
```  
   - **macOS / nix**  
```ps1
curl "https://github.com/nstevens1040/mp42gif/releases/download/v1.0.0/mp42gif" --output "mp42gif"
chmod +x ./mp42gif
```  
or use the script  
   - **cross-platform**

```sh
git clone https://github.com/nstevens1040/mp42gif.git
cd mp42gif
pip3 install -r requirements.txt
```  
# Usage  
```sh
usage: mp42gif.exe [-h] [--input VIDIN] [--slice] [--starttime SLICE_TIME] [--stoptime SLICE_TIME] [--playbackrate PBRATE] [--blend]

Specify how your video gets converted into a GIF

optional arguments:
  -h, --help            show this help message and exit
  --input VIDIN         --input <str>(file path to your mp4 file)
  --slice               --slice --starttime <int>(start time in seconds) --stoptime <int>(end time in seconds) :: both arguments reflect the amount of seconds from the beginning of the video
  --starttime SLICE_TIME
                        --starttime <int>(start time in seconds from the beginning of the video)
  --stoptime SLICE_TIME
                        --stoptime <int>(stop time in seconds from the beginning of the video)
  --playbackrate PBRATE
                        --playbackrate <float>(integer or decimal that is non-negative, non-zero, & not 1) :: numbers greater than 1 speed the video up and numbers between 0 and 1 slow the video down
  --blend               --blend <bool>(true or false) :: Determines whether the video gets "minterpolated"
```  
