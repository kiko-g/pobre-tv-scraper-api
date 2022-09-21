import config
from flask_cors import CORS
from flask import Flask, request, jsonify
from scraper import scrape_tv_show

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    res = {
        'message': 'Hello from PobreTV API',
    }

    return jsonify(res)


@app.route('/show', methods=["POST"])
def demo():
    """
        NOTE: The route receives an input in a non-JSON format (XML-URL-Encoded format)
    """
    show_url = request.values['url']
    result = scrape_tv_show(show_url)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host=str(config.HOST), port=int(config.PORT), debug=config.get_mode(config.ENVIRONMENT))
