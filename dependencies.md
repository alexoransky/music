The project depends on Python and the following Python libs:

- Python 3
  
        tested Python 3.8.6

- termcolor

        tested termcolor 1.1.0

- num2words

        tested num2words 0.5.10

- pyfluidsynth

    pyfluidsynth depends on fluidsynth Linux package
  
        tested fluidsynth 2.1.5-2
  
        tested pyfluidsynth 1.3.0
        it installed numpy 1.19.4

- mido

        tested mido 1.2.9

- python-rtmidi 
  
    python-rtmidi requires gcc, pkgconf etc. i.e. base-devel
    python-rtmidi requires cython

        tested cython 0.29.21
  
        tested python-rtmidi 1.4.6
        python-rtmidi generated an error:
        FileNotFoundError: [Errno 2] No such file or directory: 'pkg-config'

