import service
import json
import unittest
import urllib

class ServiceTestCase(unittest.TestCase):
    root_url = '/createCsr'
    encrypted = '-----BEGIN PGP MESSAGE-----\nVersion: GnuPG v1\n\njA0EAwMCfq/WT2Po8I1gyVVNDJLvVoLteW1fZ/NvCPt39ieT/ZqfSpAas2KyK2tK\nuAf7cMtNynrbwR7K6gHD82GrfIHxKqKQX/+E1Q+UHU+WIdU1KdL3Xe4Uxb2sMVeE\nRD+VSmRs\n=FaJd\n-----END PGP MESSAGE-----\n'

    def setUp(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()

    def send_get(self, message, passphrase):
        return self.app.get(self.root_url+'?Message='+message+'&PassPhrase='+passphrase)

    def send_post(self, data):
        return self.app.post(self.root_url, data=json.dumps(data), 
                content_type='application/json')

    def test_send_get_no_message(self):
        rv = self.app.get(self.root_url+'?PassPhrase=123')
        assert 'Error' in rv.data

    def test_send_get_no_passphrase(self):
        rv = self.app.get(self.root_url+'?Message=text')
        assert 'Error' in rv.data

    def test_send_get_wrong_passphrase(self):
        rv = self.send_get(urllib.quote(self.encrypted), '123')
        assert 'Error' in rv.data

    def test_send_get_correct_params(self):
        rv = self.send_get(urllib.quote(self.encrypted), 'asdf')
        assert 'DecryptedMessage' in rv.data
        assert 'Flask is a micro webdevelopment framework' in rv.data

    def test_send_post_no_message(self):
        rv = self.send_post(dict(
            PassPhrase='123',
        ))
        assert 'Error' in rv.data

    def test_send_post_no_passphrase(self):
        rv = self.send_post(dict(
            Message='text',
        ))
        assert 'Error' in rv.data

    def test_send_post_wrong_passphrase(self):
        rv = self.send_post(dict(
            Message=self.encrypted,
            PassPhrase='123',
        ))
        assert 'Error' in rv.data

    def test_send_post_correct_params(self):
        rv = self.send_post(dict(
            Message=self.encrypted, 
            PassPhrase='asdf'
        ))
        assert 'DecryptedMessage' in rv.data
        assert 'Flask is a micro webdevelopment framework' in rv.data

if __name__ == '__main__':
    unittest.main()