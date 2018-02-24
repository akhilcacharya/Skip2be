# Skip2be

Use text analysis on Google-generated captions in YouTube videos in order to detect and skip embedded advertisements. 

## Components 


### Data Fetching


Run ```fetch_sub.sh```: 

```
$ sh fetch_sub.sh [youtube_playlist]
```

This will download an English automated caption to the local disk in the form of a .vtt file and save them to data/vtt. You should probably make sure to actually have these directories before attempting to run the script. 

TODO: save these or script/cd them into their own directory (for VTT files)

### Data Transform 

Run the converter script. 

```
$ ./convert_vtt.py [VIDEO_ID].en.vtt 
```
or
```
$ ./convert_vtt.py
```
to convert all vtt files in data/vtt

This will dump 2 text files per vtt to the local disk. 

1) VIDEO_ID.chunk_output.tsv - Outputs a TSV of mapping between the start time in ms to the chunk of text generated by the ASR.

2) VIDEO_ID.token_output.tsv - Outputs a TSV mapping between the start time in ms to the token in the overall transcription. 

TODO: save these or script/cd them into their own directory (for TSV files). 


