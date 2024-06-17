import unittest
from unittest.mock import patch, MagicMock
from app import app, minioClient

class TestMusicPlayer(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.minioClient')
    def test_index(self, mock_minioClient):
        # Mock the list_objects method
        mock_objects = [
            MagicMock(object_name='song1.mp3'),
            MagicMock(object_name='song2.mp3')
        ]
        mock_minioClient.list_objects.return_value = mock_objects

        # Mock the presigned_get_object method
        mock_minioClient.presigned_get_object.side_effect = [
            'http://mockedurl.com/song1.mp3',
            'http://mockedurl.com/song2.mp3'
        ]

        # Send a request to the index route
        response = self.app.get('/')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'song1.mp3', response.data)
        self.assertIn(b'song2.mp3', response.data)
        self.assertIn(b'http://mockedurl.com/song1.mp3', response.data)
        self.assertIn(b'http://mockedurl.com/song2.mp3', response.data)

    @patch('app.minioClient')
    def test_index_with_error(self, mock_minioClient):
        # Mock the list_objects method to raise an S3Error
        mock_minioClient.list_objects.side_effect = S3Error("Mocked S3 error")

        # Send a request to the index route
        response = self.app.get('/')

        # Verify the response
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error in fetching music files', response.data)

if __name__ == '__main__':
    unittest.main()
