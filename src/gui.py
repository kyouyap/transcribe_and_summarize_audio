from pydub import AudioSegment
from .transcribe import transcribe
from .summary import summary
from .record import Recorder
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QFileDialog,
    QCheckBox,
    QComboBox,
)
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Your App Name")
        self.setGeometry(300, 300, 300, 200)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()

        # Create form to enter environment variable "OPENAI_API_KEY"
        env_var_label = QLabel("OPENAI_API_KEY:", self)
        layout.addWidget(env_var_label)

        self.env_var_input = QLineEdit(self)
        layout.addWidget(self.env_var_input)

        set_env_var_button = QPushButton("Set OPENAI_API_KEY", self)
        set_env_var_button.clicked.connect(self.set_openai_api_key)
        layout.addWidget(set_env_var_button)

        # Record button
        self.record_btn = QPushButton("Record", self)
        self.record_btn.clicked.connect(self.record)
        layout.addWidget(self.record_btn)

        # Stop button
        self.stop_btn = QPushButton("Stop Recording", self)
        self.stop_btn.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_btn)

        self.extract_audio_btn = QPushButton("Extract Audio from Video", self)
        self.extract_audio_btn.clicked.connect(self.extract_audio_from_video)
        layout.addWidget(self.extract_audio_btn)

        # is_local_whisper checkbox
        self.is_local_whisper_checkbox = QCheckBox("Use Local Whisper", self)
        layout.addWidget(self.is_local_whisper_checkbox)

        # Model name combobox
        self.model_name_combobox = QComboBox(self)
        self.model_name_combobox.addItem("gpt-3.5-turbo")
        self.model_name_combobox.addItem("gpt4")
        layout.addWidget(self.model_name_combobox)

        widget.setLayout(layout)

        self.update_buttons_status()

    def update_buttons_status(self):
        is_recording = hasattr(self, 'recorder') and self.recorder.is_recording
        self.record_btn.setEnabled(not is_recording)
        self.stop_btn.setEnabled(is_recording)

    def set_openai_api_key(self):
        os.environ["OPENAI_API_KEY"] = self.env_var_input.text()

    def record(self):
        self.recorder = Recorder()
        self.recorder.start_recording()
        print("Recording started. Press 'Stop Recording' button to stop recording.")
        self.update_buttons_status()

    def stop_recording(self):
        self.recorder.stop_recording()
        self.recorder.save_recording()
        print("Recording stopped and saved.")
        self.update_buttons_status()
        transcription = transcribe(
            self.recorder.output_file,
            is_local_whisper=self.is_local_whisper_checkbox.isChecked()
        )

        text_summary = summary(
            transcription, model_name=self.model_name_combobox.currentText())

        QMessageBox.about(self, "Summary", text_summary)

    def extract_audio_from_video(self):
        video_file, _ = QFileDialog.getOpenFileName(self, "Select Video File")
        if not video_file:
            return

        audio_file = os.path.splitext(video_file)[0] + ".mp3"
        video = AudioSegment.from_file(
            video_file, format=video_file.split(".")[-1])
        video.export(audio_file, format="mp3")

        transcription = transcribe(
            audio_file,
            model_name=self.model_name_combobox.currentText(),
            is_local_whisper=self.is_local_whisper_checkbox.isChecked()
        )

        text_summary = summary(
            transcription, model_name=self.model_name_combobox.currentText())

        QMessageBox.about(self, "Summary", text_summary)
