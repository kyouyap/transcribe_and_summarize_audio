
import unittest
import os
import time
from src.record import Recorder

class TestRecorder(unittest.TestCase):

    def test_recorder_initialization(self):
        recorder = Recorder()
        self.assertIsNotNone(recorder)
        self.assertFalse(recorder.is_recording)

    def test_start_stop_recording(self):
        recorder = Recorder()
        recorder.start_recording()
        self.assertTrue(recorder.is_recording)
        time.sleep(2)  # Record for 2 seconds
        recorder.stop_recording()
        self.assertFalse(recorder.is_recording)

    def test_save_recording(self):
        output_file = "./test_output/test_audio.wav"
        recorder = Recorder(output_file=output_file)
        recorder.start_recording()
        time.sleep(2)  # Record for 2 seconds
        recorder.stop_recording()
        recorder.save_recording()
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)  # Clean up the test file

if __name__ == "__main__":
    unittest.main()
