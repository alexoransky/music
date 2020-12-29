Project music
=============

The objective is to explore various music scales and intervals using
MIDI synthesizers and CLI or GUI visualizations.

Here is a list of Python tools for music:
https://wiki.python.org/moin/PythonInMusic

The project works with SimpleSynth or FluidSynth (preferred).
Both synths work with Sound Font SF2 instrument sample files.
Polyphone tool can be used to edit files:
https://www.polyphone-soundfonts.com/download

Basically, the music theory part that is needed is described in wikipedia: 

https://en.wikipedia.org/wiki/Semitone#Minor_second
https://en.wikipedia.org/wiki/Just_intonation
https://en.wikipedia.org/wiki/Interval_(music)
https://en.wikipedia.org/wiki/Diatonic_scale
https://en.wikipedia.org/wiki/Scale_(music)
https://en.wikipedia.org/wiki/Minor_scale#Melodic_minor_scale
https://en.wikipedia.org/wiki/Chromatic_scale
https://en.wikipedia.org/wiki/Heptatonic_scale
https://en.wikipedia.org/wiki/MIDI
https://en.wikipedia.org/wiki/Scientific_pitch_notation
https://en.wikipedia.org/wiki/Chord_(music)

FluidSynth
----------
FluidSynth is used to generate sound on both macOS and Linux.
http://www.fluidsynth.org
APIs:
http://www.fluidsynth.org/api/index.html

FLuidSynth starts with many warning messages on Arch Linux.  However, it does not seem to affect anything.
Here is the command to use ALSA:
  fluidsynth -is -a alsa -m alsa_seq -r 48000 /usr/share/soundfonts/FluidR3_GM.sf2
  
ALSA lib pcm_dsnoop.c:641:(snd_pcm_dsnoop_open) unable to open slave
ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
connect(2) call to /dev/shm/jack-1000/default/jack_0 failed (err=No such file or directory)
attempt to connect to server failed
connect(2) call to /dev/shm/jack-1000/default/jack_0 failed (err=No such file or directory)
attempt to connect to server failed
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave
connect(2) call to /dev/shm/jack-1000/default/jack_0 failed (err=No such file or directory)
attempt to connect to server failed
FluidSynth runtime version 2.1.3
Copyright (C) 2000-2020 Peter Hanappe and others.
Distributed under the LGPL license.
SoundFont(R) is a registered trademark of E-mu Systems, Inc.
fluidsynth: warning: Failed to set thread to high priority
fluidsynth: warning: Failed to set thread to high priority 

Sometimes an update to alsa-lib breaks the FS imterface, refer to notes from 06/13/2020 on how to fix the issue.

FluidSynth opens the following MIDI ports:
 'FLUID Synth (40619):Synth input port (40619:0) 128:0'
 'FLUID Synth (40619):Synth input port (40619:1) 128:1'
 'FLUID Synth (40619):Synth input port (40619:10) 128:10'
 'FLUID Synth (40619):Synth input port (40619:11) 128:11'
 'FLUID Synth (40619):Synth input port (40619:12) 128:12'
 'FLUID Synth (40619):Synth input port (40619:13) 128:13'
 'FLUID Synth (40619):Synth input port (40619:14) 128:14'
 'FLUID Synth (40619):Synth input port (40619:15) 128:15'
 'FLUID Synth (40619):Synth input port (40619:2) 128:2'
 'FLUID Synth (40619):Synth input port (40619:3) 128:3'
 'FLUID Synth (40619):Synth input port (40619:4) 128:4'
 'FLUID Synth (40619):Synth input port (40619:5) 128:5'
 'FLUID Synth (40619):Synth input port (40619:6) 128:6'
 'FLUID Synth (40619):Synth input port (40619:7) 128:7'
 'FLUID Synth (40619):Synth input port (40619:8) 128:8'
 'FLUID Synth (40619):Synth input port (40619:9) 128:9'

Lilypond
--------
Lilypond is the software that allows to store music in text-based files instead of sheets.
http://lilypond.org
Frescobaldi is GUI for the Lilypond:
https://www.frescobaldi.org


04/15/2020
----------
Project created
Added notes, diatonic intervals.

04/18/2020
----------
Added heptatonic scales, 12-TET.
The project will be using PyGame to play MIDI.
https://www.pygame.org/news
Installed SympleSynth to check MIDI output. The sound is not great. Need to install something better.

04/25/2020
----------
Will try FluidSynth with sound fonts:
https://sites.google.com/site/soundfonts4u/
FluidSynth will be CLI only, installed with homebrew.
homebrew install fluid-synth
It turns out that PyFluidSynth only supports FS 1.11.1, so this one has to be installed instead:
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/34dcd1ff65a56c3191fa57d3dd23e7fffd55fae8/Formula/fluid-synth.rb

The instruments will be NiceKeys B JN 1.4 (full keys with small piano).
Bunch of sound fonts are here:
https://sites.google.com/site/soundfonts4u/

Initialize fluidsynth with a small sound font to use the CLI.  This is not needed for python program.
fluidsynth -o midi.driver=coremidi -o audio.driver=coreaudio -o audio.coreaudio.device=default -o audio.period-size=256 /Users/alex/PycharmProject/music/data/Nice-Keys-B-Plus-JN1.4.sf2

We will be using PyFLuidSynth for a Python API wrapper.
https://github.com/nwhitehead/pyfluidsynth
It turns that it is for Python 2, so I patched it. Copy the patches/fluidsynthpath.py to where it is installed:
(macOS): /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/fluidsynth.py
(Linux): /usr/lib/python3.8/site-packages/fluidsynth.py

Install osascript
This is needed to control output volume in macOS. FS outputs some noise when the destructor is called.

FluidSynth settings is a great reference on how to control the synth.
http://www.fluidsynth.org/api/fluidsettings.xml#synth.gain

All that is incorporated with examples in the Synth class.

Added chords.

04/26/2020
----------
Explored Polyphone.  I really needed just a tool that would list presets in the SF2 file.
Updated chord print names.
Added Sus2 and Sus4 chords.

For GUI- installed Qt 5.12.8.  PySide2 seems to support only 5.12 as of now.

05/01/2020
----------
Added octave numbers to note names.
Reworked note names.
Added chord inversions.

05/02/2020
----------
Added .gitignore.

There is a project that draws a piano keyboard in the terminal:
https://github.com/s-d-m/pianoterm/blob/master/src/music_player.cc
Which is based on termbox library to draw anything in the terminal:
https://github.com/nsf/termbox

Interesting intro into WebMIDI:
https://www.smashingmagazine.com/2018/03/web-midi-api/

05/08/2020
----------
Arturia KeyStep 32 has arrived.  Works great with GarageBand.
FluidSynth requires a tool to bridge the controller's output MIDI port to its input port.
Found a MIDI router to map those:
https://github.com/icaroferre/MIDIRouter
Apparently it is Python Qt app, so it is great. Will be able to re-use parts.

Another MIDI route, called MIDI patchbay is not compatible with MacOS Catalina, is an Xcode project
and the has been in works for 6 months by now.

05/09/2020
----------
Added a MIDI router that uses mido lib to map the ports.
The router forwards MIDI messages from the designated input port to tbe designated output port.
It also queues all MIDI messages that are generated by the keyboard so that another thread
an access them.

05/10/2020
----------
Added a MIDI parser to print notes and chords that are being played.

05/18/2020
----------
Added the project on github.
Started porting to Linux. Fluidsynth 2.1.2 is installed on Arch.  
Fluidsynth 2.1.2 has updated APIs: http://www.fluidsynth.org/api/
I had to patch the fluidsynth.py to support those.  This is not complete bindings but works for this project.

05/19/2020
----------
Removed the code to reduce the volume in macOS when FLuidSynth is stopping.
Added a delay of 1 second instead.

05/20/2020
----------
Need to investigate how to create a PyQt tabbed app without the Qt GUI builder.
Added a simple GUI app with tabs.  

05/21/2020
----------
The GUI app is moved to midi project.

05/22/2020
----------
Added support for FLuid Synth to the GUI app.
Added a simple MIDI router to the GUI app.

05/25/2020
----------
LilyPond is program to convert text based muisic score file to sheet music.
It provides a de-facto standard file format (.ly) thaqt allows for specifying complex music pieces.
My idea is to use .ly files to play music using FluidSynth.
I will have to convert my scietific pitch notation (c#3) to Helmholz-like pitch notation (cis') 
in order to use those files.

Lilypond generates a MIDI file, so that can be used to play the music. 
There is python-ly project to read the music from .ly files into Python data structures.

05/26/2020
----------
Added a simple MIDI file player that is based on mido library.

05/30/2020
----------
Finished rework of the simple MIDI player- added a thread for playback, ability to pause/release
the playback, jump to the message or time mark.
Still need to add a synth channel-MIDI port-file track map.
As of now, it does not work type 2 (asynchronous) MIDI files.
I started working on the multi-thread player but that pause/release breaks synchronization
between threads even for type 1 files.

05/31/2020
----------
Today, I have added an ability add play a fragment of the file (from any note to any note) 
to the MIDIFilePlayer.

06/03/2020
----------
Reworked the player to use a simple state machine.

06/06/2020
----------
Started working on a metronome function.  The metronome click and bell sounds are MIDI notes 33 and 34 and
defined are in General MIDI Level 2:
https://soundprogramming.net/file-formats/general-midi-drum-note-numbers/
It turns out that not many sound fonts actually have those. They are in this sound font made by Rick Simon, 
in bank 128, preset 0 (127:000) but (128:004) seems to sound better.
Note that 128:056 with notes 45 and 46 sounds even better. 
https://musescore.org/en/node/109371

In order to explore and edit sound fonts, I installed Polyphone tool:
https://www.polyphone-soundfonts.com

06/12/2020
----------
After updating alsa-lib to 1.2.3-1, FLuidSynth generates an error:
ALSA lib dlmisc.c:338:(snd_dlobj_cache_get0) Cannot open shared library libasound_module_pcm_pulse.so (libasound_module_pcm_pulse.so: libasound_module_pcm_pulse.so: cannot open shared object file: No such file or directory)
fluidsynth: error: Failed to open the "default" audio device

Reverted to alsa-lib 1.2.2-1:
sudo pacman -U https://archive.archlinux.org/packages/a/alsa-lib/alsa-lib-1.2.2-1-x86_64.pkg.tar.zst
And also changed /etc/pacman.conf to ignore alsa-lib updates
IgnorePkg   = alsa-lib

Old versions can be found in:
https://archive.archlinux.org/packages/a/alsa-lib/

06/13/2020
----------
Finished the metronome class. I had to change the synth and the router class a little.

06/27/2020
----------
Started exploring just tuning and tuning to 432 Hz (Verdi's A).
FluidSynth allows changes in tuning but it does it as offset in cents from 440 Hz standard.

Conversion from Hz to cents and back:
http://www.sengpielaudio.com/calculator-centsratio.htm
See Frequency to musical note converter

I have added Tuning class to be able to change A from 440 Hz to any other number and started working on
just intonation.  I have added 5-limit tuning.

Just intonation: building a 12-note scale for 5-limit tuning:
https://en.wikipedia.org/wiki/Five-limit_tuning

Intervals are calculator with a factor:
F = 3^x x 5^y x 2^z
Where x, y znd z are defined in the following grid (z is a function of x and y, x = [-2, 2], y = [-1, 1]):
    -2  -1  0   1   2
1   1   0   -2  -3  -5
0   4   2   0   -1  -3
-1  6   4   3   1   0

Interval is then calculated using the following formula:
I = 1200 x log2(F)

This generates the following table:
    -2  -1  0   1    2
1   182 884 386 1088 590
0   996 498 0   702  204
1   610 112 814 316  1018

Every note in column -2 is enharmonic to a note in column 2 (eg 610 and 590).
Then only 12 notes has to be selected from the 15 defined by the table.
Note at (-2, -1) with interval of 610 is removed first.  Then two other notes
are removed, thus, with the removal of 610, 3 scales can be generated:
1. 610, 182, 1018
2. 610, 996, 204
3. 610, 996, 182

09/05/2020
----------
Started working on the UI again.  Investigated urwid BarGraph widget to create a terminal view.
Also, found this project that uses Qt5:
https://github.com/killalea/digital-keyboard
It seems to be the most promising.

09/11/2020
----------
Added a tabbed GUI app that displays a keyboard.
The project that I found (digital keybaord) was inspirational, I learned how the scene and labels can be used.
Everything else had to be rewritten.

9/12/2020
----------
Collected all common MIDI and Synth tasks in the AudioSupport class.

9/13/2020
----------
A note on "Cannot mix incompatible Qt library" when running Qt Designer or qt5ct tool or other Qt tools due to the inconsuistent update in Qt libs.
In my case it was an update from Qt 5.15.0 to 5.15.1.  
This is resolved by updating qt5-styleplugins, although it might take a few days.  Also, the tool does not store the config, henerates a sigfault.

For the project, added display of notes and chords that are being played.
  
12/14/2020
----------
Got back to the project after a long break- was busy at work. Also, had to reinstall the system.
Anyway, slowly started recalling where I left the project a few months back.

12/15/2020
----------
One of the ideas is to put together a chords tool that would:
- display the notes that the entered chord has
- play the chord
- display the chord on the guitar neck
- display the chord on the piano keyboard

The first two items are already implemented in the main.py module.

pyfluidsynth was updated to 1.3.0 and needed to be patched again.

12/16/2020
----------
Moved a few modules around, created keyboard, audio and theory packages.

Started looking at FFT again.  Foound this (also on PyPi:
https://pyfftw.readthedocs.io/en/latest/

Also, there is an example that generates a real time FFT histogram:
https://python-sounddevice.readthedocs.io/en/latest/examples.html#plot-microphone-signal-s-in-real-time

The latter uses sounddevice (0.4.1 as of now) which is a Python APIs for PortAudio.

12/19/2020
----------
Spent couple days exploring FFT options and building the tuner.  
The idea is to have an FFT that produces a list of frequencies and magnitudes that
would be suitable for working with the tuner and the chord recognizer.

The FFT class so far uses a short FFT algorithm, numpy, scipy and sounddevice APIs. 

There is a second solution that uses a short time FT algorithm, numpy and pyaudio:
https://mzucker.github.io/2016/08/07/ukulele-tuner.html

There is a good explanation how STFT works:
https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/#:~:text=The%20Short%20Time%20Fourier%20Transform%20(STFT)%20is%20a,a%20waterfall%20plot%20which%20shows%20frequency%20against%20time.
https://github.com/KevinNJ/Projects/tree/master/Short%20Time%20Fourier%20Transform

An excellent book that explains the design choices behind STFT:
https://www.dsprelated.com/freebooks/sasp/

12/22/2020
----------
Reorganized the code- store samples in a deque so that they can be processed in a separate thread.

12/24/2020
----------
Added separate classes for input devices that are based on SoundDevice and PyAudio.

12/26/2020
----------
Yesterday was looking for ways to not waste time to do FFT on the spectrum above 5 KHz. 
75% of the sonic spectrum is not needed for music anyway and DFT requires all samples to provide
desired frequency resolution and, therefore, slow.  
Found Chirp Z-transform (CZT) algorithm.  The CZT allows to "zoom-in" on a specific frequency band 
and not to process the rest:
https://pypi.org/project/czt/
https://github.com/garrettj403/CZT/

12/28/2020
----------
Finally, updated the tuner class to work with either the STFT or CZT transform.
CZT works faster and a lot more precise in the desired range.
