Guitar tuner using the Fast Fourier Transform algorithm 
to determine frequency from a signal. Using the frequency
obtained by our FFT algorithm, we can convert it to a pitch,
which we can match with a set dictionary of pitches to check
if the open string is in tune or not.


To run my project, you will need two libraries installed: numpy, pyaudio

pip install numpy 
pip install pyaudio


Wolfe, J. (n.d.). Note names, MIDI numbers and frequencies. Retrieved December 10, 2021, from https://newt.phys.unsw.edu.au/jw/notes.html. 


Link to perfect pitch E4 I used to test my program, just hold it up to your sound device with your phone or what not.
https://www.youtube.com/watch?v=F1hgKMmZuDk


https://support.ircam.fr/docs/AudioSculpt/3.0/co/FFT%20Size.html
https://en.wikipedia.org/wiki/Fast_Fourier_transform
https://people.csail.mit.edu/hubert/pyaudio/docs/
https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
