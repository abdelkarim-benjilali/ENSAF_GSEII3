#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: tp2
# GNU Radio version: v3.8.2.0-57-gd71cd177

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import longueur  # embedded python module

from gnuradio import qtgui

class tp2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "tp2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("tp2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tp2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.gain = gain = 50

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 100, 1, 50, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self.fft_vxx_0 = fft.fft_vfc(longueur.longueur(), True, window.blackmanharris(1024), 1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('F:\\karim\\s5\\traitement de signal de parole\\tp1\\file.wav', False)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, longueur.longueur())
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, longueur.longueur())
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, longueur.longueur(), 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(gain)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'F:\\karim\\s5\\traitement de signal de parole\\tp2\\file2.wav', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(longueur.longueur())



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tp2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)





def main(top_block_cls=tp2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
