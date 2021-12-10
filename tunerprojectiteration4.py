'''
Ruairidh McNeil
Guitar Tuner
12/8/2021

Guitar tuner using the Fast Fourier Transform algorithm 
to determine frequency from a signal. Using the frequency
obtained by our FFT algorithm, we can convert it to a pitch,
which we can match with a set dictionary of pitches to check
if the open string is in tune or not.

https://newt.phys.unsw.edu.au/jw/notes.html
https://support.ircam.fr/docs/AudioSculpt/3.0/co/FFT%20Size.html
https://en.wikipedia.org/wiki/Fast_Fourier_transform
https://people.csail.mit.edu/hubert/pyaudio/docs/
https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
'''

import numpy as np
import pyaudio

p = pyaudio.PyAudio()

'''
To use the FFT algorithm,
we need to set some constants for the FFT and with pyaudio.
'''
#  FFT Constants
SAMPLE_FREQUENCY = 22050
SAMPLES_PER_FRAME = 2048
FFT_AVERAGE_FRAME = 16
#  FREQUENCY Constants
MIDI_MIN = 40
MIDI_MAX = 64
#  PyAudio Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
PERIOD = 3

SAMPLES_PER_FFT = SAMPLES_PER_FRAME*FFT_AVERAGE_FRAME
FREQUENCY_STEP_SIZE = float(SAMPLE_FREQUENCY)/SAMPLES_PER_FFT

NOTE_NAMES = 'C','C#','D','D#','E','F','F#','G','G#','A','A#','B'
STANDARD_TUNING = 'E2', 'A', 'D', 'G', 'B', 'E4'


def frequency_to_midi_from_reference(f):
    midi_number = 12 * np.log2 (f / 440) + 69
    return midi_number


def note_name(n):
    return NOTE_NAMES[n % 12]


#  Interval between samples in our frequency domain
def fftbin_size(n):
    return frequency_to_midi_from_reference(n)/FREQUENCY_STEP_SIZE


#  Function that takes user input for standard tuning and converts it to MIDI number
def selection_to_freq(i):
    if i == 'E2':
        return 82.41
    if i == 'A':
        return 110
    if i == 'D':
        return 146.8
    if i == 'G':
        return 196
    if i == 'B':
        return 246.9
    if i == 'E4':
        return 329.6
    else:
        print('You have entered an incorrect value for standard tuning. Please try again.')
        return False


def freq_check(v, user_low, user_high):
    if user_low <= v <= user_high:
        return True
    else:
        return False


def main():

    #  Identify sound devices connected to computer
    #  https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio
    numdevices = p.get_host_api_info_by_index(0).get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    #  User asked to specify which sound device they'd like to use.
    while True:
        try:
            device_selection = int(input('Select your recording device, make sure to check you are not muted. (1/2/3...)'))
            break
        except ValueError:
            print('Value Error, please enter the integer ID of your sound device.')
        
    print(STANDARD_TUNING)

    #  User asked to specify which note they want to tune to.
    while True:
        try:
            user_input = str(input('What note would you like to tune to?'))
            user_freq_choice  = selection_to_freq(user_input)
            break
        except ValueError:
            print('Value Error, please specify what note from the list above.')


    #  Open sound device stream, input=True to enable recording.
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_FREQUENCY,
                    input=True,
                    frames_per_buffer=SAMPLES_PER_FRAME,
                    input_device_index = device_selection)

    #  Begin recording
    stream.start_stream()

    #  Hanning approximation of fft
    window = np.hanning(SAMPLES_PER_FRAME)

    try:
        while stream.is_active():
            #  Read stream signal, specify buffer and apply FFT to signal.
            signal = stream.read(SAMPLES_PER_FRAME)
            data = np.frombuffer(signal, dtype=np.int16)
            windowed = window * data

            fft = np.fft.rfft(windowed/(len(data)/4))
            freq = np.fft.fftfreq(SAMPLES_PER_FRAME, d=1 / SAMPLE_FREQUENCY)
            freq = fft[1:].argmax() + 174.6

            note_absolute = frequency_to_midi_from_reference(freq)
            nearest_note = int(round(note_absolute))
            nearest_note = note_name(nearest_note)

            print(nearest_note, freq)

            accepted_range_low = int(round(user_freq_choice - 4))
            accepted_range_high = int(round(user_freq_choice + 4))
            value_check = freq_check(freq, accepted_range_low, accepted_range_high)

            if value_check == True:
                print('You are in tune!')
                stream.close()
    except OSError:
        print('Your audio device has been closed.')


if __name__ == '__main__':
    main()
