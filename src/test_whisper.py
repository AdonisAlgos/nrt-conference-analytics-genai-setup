import unittest
import os
from whisper import Transcription

class TestWhisper(unittest.TestCase):

    def setUp(self) -> None:
        # Create a test audio file
        self.transcriber = Transcription()
        self.audio_file_path = "test_audio.m4a"
        self.assertTrue(os.path.exists(self.audio_file_path), f"{self.audio_file_path} does not exist")


    def test_diarize_audio(self):
        # Test the diarize_audio function

        diarization = self.transcriber.diarize_audio(self.audio_file_path)
        self.assertIsNotNone(diarization)
        self.assertTrue(hasattr(diarization, 'itertracks'), "Diarization result should have 'itertracks' method")
        
        # Assuming the result is a pyannote.core.Annotation object
        speaker_labels = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"Speaker {speaker} from {turn.start:.1f}s to {turn.end:.1f}s")
            speaker_labels.append(speaker)
        
        self.assertTrue(len(speaker_labels) > 0, "No speaker labels found")
        self.assertTrue(all(isinstance(label, int) for label in speaker_labels), "All speaker labels should be integers")

if __name__ == '__main__':
    unittest.main()