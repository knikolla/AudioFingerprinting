# Usage

The project can be run executing ```aufin.py``` through the command line with the appropriate commands. 

## Insert Song
To insert a song in the database do:

```python aufin.py insert <location_of_file>```

Then enter the appropriate metadata when prompted. 

For example:

```
python aufin.py insert ../music/ZA.Grazie.wav
Title: Grazie
Author: Zero Assoluto
Album: Una Pioggia di Parole
```

## Identify Song
### From File
To identify a song from file do:
```python aufin.py find file <location_of_file> <start_sample> <end_sample>```

Fro example the following command will query for the Grazie.wav file, starting from sample number 500 000 to sample number 800 000:

```python.aufin.py find file ../recordins/Grazie.wav 500000 800000```

If the sample numbers are omitted the system will search for the entire song, which is unnecessary. 

### From Mic
To identify a song from the microphone do:
```python aufin.py find mic```

The system will listen for the number of seconds specified in the ```config.py``` file. 