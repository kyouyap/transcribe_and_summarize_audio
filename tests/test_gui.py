import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from src.gui import App
import time

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        del cls.app

    def setUp(self):
        self.ex = App()


    def test_set_openai_api_key(self):
        test_key = "test_key"
        self.ex.env_var_input.setText(test_key)
        self.ex.set_openai_api_key()
        self.assertEqual(os.environ["OPENAI_API_KEY"], test_key)

    @patch("src.gui.Recorder")
    def test_record(self, mock_recorder):
        self.ex.record_btn.click()
        self.assertTrue(self.ex.stop_btn.isEnabled())
        self.assertFalse(self.ex.record_btn.isEnabled())
        mock_recorder.return_value.start_recording.assert_called_once()

    @patch("src.gui.Recorder")
    def test_stop_recording(self, mock_recorder):
        instance = mock_recorder.return_value
        instance.is_recording = True
        self.ex.recorder = instance

        with patch("src.gui.transcribe") as mock_transcribe, \
                patch("src.gui.summary") as mock_summary, \
                patch("PyQt6.QtWidgets.QMessageBox.about") as mock_about:
            assert self.ex.stop_btn.isEnabled() 
            self.ex.stop_btn.click()
            QTest.qWait(100)
            instance.stop_recording.assert_called_once()
            instance.save_recording.assert_called_once()
            mock_transcribe.assert_called_once()
            mock_summary.assert_called_once()
            mock_about.assert_called_once()

            self.assertTrue(self.ex.record_btn.isEnabled())
            self.assertFalse(self.ex.stop_btn.isEnabled())

    @patch("PyQt6.QtWidgets.QFileDialog.getOpenFileName")
    @patch("src.gui.AudioSegment.from_file")
    @patch("src.gui.transcribe")
    @patch("src.gui.summary")
    @patch("PyQt6.QtWidgets.QMessageBox.about")
    def test_extract_audio_from_video(self, mock_about, mock_summary, mock_transcribe, mock_from_file, mock_get_open_file_name):
        video_file = "test_video.mp4"
        audio_file = "test_video.mp3"
        mock_get_open_file_name.return_value = (video_file, None)

        self.ex.extract_audio_btn.click()

        mock_get_open_file_name.assert_called_once()
        mock_from_file.assert_called_once_with(video_file, format="mp4")
        mock_from_file.return_value.export.assert_called_once_with(audio_file, format="mp3")
        mock_transcribe.assert_called_once_with(audio_file)
        mock_summary.assert_called_once_with(mock_transcribe.return_value)
        mock_about.assert_called_once_with(self.ex, "Summary", mock_summary.return_value)


if __name__ == "__main__":
    unittest.main()
