import gnupg
import json
import urllib
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/createCsr', methods=['GET'])
def create_csr_get():
    message = urllib.unquote(request.args.get('Message') or '')
    passphrase = urllib.unquote(request.args.get('PassPhrase') or '')
    return decrypt(message, passphrase)

@app.route('/createCsr', methods=['POST'])
def create_csr_post():
    message = request.json.get('Message', None)
    passphrase = request.json.get('PassPhrase', None)
    return decrypt(message, passphrase)
    
def decrypt(message, passphrase):
    if not passphrase or not message:
        return jsonify({'Error': 'PassPhrase and Message are required'})
    gpg = gnupg.GPG()
    result = gpg.decrypt(message, passphrase=passphrase)
    if not result.ok:
        return jsonify({'Error': 'Unable to decrypt message'})
    return jsonify({'DecryptedMessage': str(result)})

if __name__ == '__main__':
    app.run()
