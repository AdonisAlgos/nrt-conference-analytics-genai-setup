import unittest
from transcribe import Transcriber

class TestTranscriberIntegration(unittest.TestCase):
    def test_transcribe_real(self):
        transcriber = Transcriber()
        transcript_text = transcriber.transcribe("test_audio.m4a")
        diarised_transcript = transcriber.correct_transcript(transcript_text)

        print(transcript_text)
        print(diarised_transcript)

        self.assertIsInstance(transcript_text, str)
        self.assertIsInstance(diarised_transcript, str)

if __name__ == '__main__':
    unittest.main()
