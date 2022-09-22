import json
import config
from flask_cors import CORS
from flask import Flask, request, jsonify
from scraper import scrape_tv_show

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    res = {
        'message': 'Hello from the PobreTV-Local API!',
    }

    return jsonify(res)


@app.route('/show', methods=["POST"])
async def show():
    """
        NOTE: The route receives an input in a non-JSON format (XML-URL-Encoded format)
    """
    show_url = request.values['url']
    seriesName, seasons = await scrape_tv_show(show_url)

    return jsonify({
        'title': seriesName,
        'seasons': []
    })


if __name__ == "__main__":
    app.run(host=str(config.HOST), port=int(config.PORT),
            debug=config.get_mode(config.ENVIRONMENT))
