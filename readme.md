Project
-------

The project is to enable MIDI playback and keyboard visualization of
various music scales.

The project works on macOS Catalina and Linux.
It is tested with Python 3.8.2 on macOS 10.15.4 and Arch Linux 5.6.14.


Dependencies
------------

- FluidSynth
- Various Python APIs (see details below)


Installation
------------

1. Install Python

2. (macOS only) Install XCode CLT from:
https://developer.apple.com/download/more/

3. Install FluidSynth:

   For installation of FS for Linux, use instructions for apt-get, pacman etc. to
install the latest FluidSynth.

   macOS:
   
   https://github.com/frescobaldi/frescobaldi/wiki/MIDI-playback-on-Mac-OS-X

   Note that PyFluidSynth does not support FluidSynth 2.x as of 4/25/2020:
   
   https://github.com/nwhitehead/pyfluidsynth/issues/19
   
   There are patches created for old FS vs.1.11.1 as well as the new FS 2.x, see details in step 4.

   If you choose to install the old FS v1.11.1, 
instead of 'homebrew install fluid-synth' 
which installs the latest FS, use:

   brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/34dcd1ff65a56c3191fa57d3dd23e7fffd55fae8/Formula/fluid-synth.rb

4. Install PyFluidSynth (1.2.5 and so on) and patch it

   pip install pyfluidsynth

   pyfluidsynth requires patching because it lacks tuning functions.

   Copy the patches/fluidsynthpath.py to where it is installed:

   (macOS): /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/fluidsynth.py
   
   (Linux): 
   /usr/lib/python3.8/site-packages/fluidsynth.py
   or
   ~/.local/lib/python3.8/site-packages/fluidsynth.py

   Refer to FluidSynth APIs for patching the later versions:
   http://www.fluidsynth.org/api/index.html

5. Download sound fonts in SF2 format

   Sound fonts are required for the synthesizer and can be found here:
   https://musescore.org/en/handbook/soundfonts-and-sfz-files#list

   Sound fonts need to be place in data folder.

6. Install mido library to work with MIDI keyboards

   pip install mido

   pip install python-rtmidi

7. Install termcolor, num2words and other Python APIs as necessary


SimpleSynth Installation
------------------------

(macOS only)

The project will work fine with SympleSynth but the sound will be inferior to the FluidSynth's.
SimpleSynth requires PyGame.midi library to output sound.
SimpleSynth was tried on macOS only.

1. Install SDL, SDL2 and other prerequisites to output MIDI:
brew install sdl sdl2 sdl_image sdl_mixer sdl_ttf portmidi

2. Install pygame
pip install pygame

3. Install SimpleSynth, see instructions:
https://notahat.com/simplesynth/

4. Use main_pygame as an example.
Leave SympleSynth running while you run Python scripts.
Note that main_pygame will work with any synthesizer, it just needs to be running.


Other resources
---------------
https://musescore.org/en/handbook/soundfonts-and-sfz-files#list

https://sites.google.com/site/soundfonts4u/
