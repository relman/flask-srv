import gnupg
import urllib
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/decryptMessage', methods=['GET'])
def decrypt_message_get():
    message = urllib.unquote(request.args.get('Message') or '')
    passphrase = urllib.unquote(request.args.get('Passphrase') or '')
    return decrypt(message, passphrase)


@app.route('/decryptMessage', methods=['POST'])
def decrypt_message_post():
    message = request.json.get('Message', None)
    passphrase = request.json.get('Passphrase', None)
    return decrypt(message, passphrase)


def decrypt(message, passphrase):
    if not passphrase or not message:
        return jsonify({'Error': 'Passphrase and Message are required'}), 400
    gpg = gnupg.GPG()
    result = gpg.decrypt(message, passphrase=passphrase)
    if not result.ok:
        return jsonify({'Error': 'Unable to decrypt message'}), 400
    return jsonify({'DecryptedMessage': str(result)})


if __name__ == '__main__':
    app.run()
