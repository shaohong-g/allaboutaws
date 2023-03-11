import sys, os
from flask import Flask, jsonify
from flask_cors import CORS
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)
cors = CORS(app)
# app.config['SECRET_KEY'] = config.SECRET_KEY


# import all blueprints
from flask_blueprints.public import public


# register all blueprints
app.register_blueprint(public, url_prefix='/api/0')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=8000, debug=True, host='0.0.0.0')

