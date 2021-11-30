# this module will be imported in the into your flowgraph
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
def longueur():
	
	data_dir = pjoin(dirname(scipy.io.__file__), 'F:', '/karim/s5/traitement de signal de parole/tp1')
	wav_fname = pjoin(data_dir, 'file.wav')

	samplerate, data = wavfile.read(wav_fname)
	#print("number of channels = {data.shape[1]}")
	#print(data.shape)
	length = data.shape[0] / samplerate
	#print("length")
	#print(length)
	#print(samplerate)
	#length = 0.01s
	return samplerate 