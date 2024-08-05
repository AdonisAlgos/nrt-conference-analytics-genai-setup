import unittest
from transcribe import Transcriber

class TestTranscriberIntegration(unittest.TestCase):
    def test_transcribe_real(self):
        transcriber = Transcriber()
        result = transcriber.transcribe("test_audio.m4a")
        diarised_result = transcriber.diarise(result.segments)

        self.assertIsInstance(result["text"], str)
        self.assertIsInstance(diarised_result, list)

if __name__ == '__main__':
    unittest.main()
