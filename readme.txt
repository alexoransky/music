Project
-------

The project is to enable MIDI playback and keyboard visualization of
various music scales.

The project works on macOS Catalina 10.15.4 with Python 3.8.2.


Dependencies
------------

pygame 1.9.6 - for MIDI playback
num2words    - for displaying ordinals


Installation
------------

1. Install Python

2. (macOS only) Install XCode CLT from:
https://developer.apple.com/download/more/

3. Choose between SimpleSynth and FluidSynth.
A MIDI synthesizer is needed to play notes.
  The project works fine with SympleSynth but the sound is primitive.
  SimpleSynth requires PyGame.midi library to output sound.
  Follow installation steps Xa, like 3a for SimpleSynth.

FluidSynth is a full-blown synthesizer.  It requires sounds from sound font.
FluidSynth uses PyFluidSynth as a Python FS API wrapper.
Follow installation steps Xb, like 3b for FluidSynth.

3a. Install SDL, SDL2 and other prerequisites to output MIDI:
brew install sdl sdl2 sdl_image sdl_mixer sdl_ttf portmidi
4a. Install pygame
pip3 install pygame
5a. Install SimpleSynth, see instructions:
https://notahat.com/simplesynth/
6a. Use main_pygame as an example.
Leave SympleSynth running while you run Python scripts.
Note that main_pygame will work with any sinthesizer, it just need to be running.

3b. Install PyFluidSynth (1.2.5) and patch it, if necessary.
pip3 install pyfluidsynth
copy the patches/fluidsynthpath.py to where it is installed:
/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/fluidsynth.py

4b. (macOS only) Install osascript
This is needed to control output volume in macOS.

5b. Install FluidSynth, see instructions:
https://github.com/frescobaldi/frescobaldi/wiki/MIDI-playback-on-Mac-OS-X
Note that PyFluidSynth does not support FluidSynth as of 4/25/2020:
https://github.com/nwhitehead/pyfluidsynth/issues/19
Instead of 'homebrew install fluid-synth' which installs the latest FS,
you might want to install old FS v1.11.1:
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/34dcd1ff65a56c3191fa57d3dd23e7fffd55fae8/Formula/fluid-synth.rb

Note that the latest FS (v2.1.2 as 5/18/2020) is available for Linux.

6b.
Replace fluidsynth.py in your Python sites library dir with the one provided in patches/osx folder.
Select the version according to your OS.

7b. Download sound fonts in SF2 format.
Sound fonts need to be place in data folder.

8. Install mido library to work with MIDI keyboards
pip install mido
pip install python-rtmidi

9. Install termcolor, num2words


Other resources
---------------
https://musescore.org/en/handbook/soundfonts-and-sfz-files#list
https://sites.google.com/site/soundfonts4u/
