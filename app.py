from flask import Flask, request, jsonify
from flask_cors import cross_origin
import treetaggerwrapper as ttw
import pickle

import syuzhet
from path_problem_resolver import get_absolute_path
from configuration_manager import ConfigurationManager

cmgr = ConfigurationManager("config.json")
cmgr.load_config()

language = cmgr.get_default_language()
emotions_array_length = cmgr.get_emotion_array_length()
emotion_names = cmgr.get_emotion_names()

data_dir = cmgr.get_data_dir()
emolex_filename = cmgr.get_emolex_filename(language)

emolex_abs_path = get_absolute_path('syuzhet/'
                                    + data_dir + '/' + emolex_filename)

with open(emolex_abs_path, 'rb') as f:
    emolex = pickle.load(f)


# Main application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_readme():
    """Show the help readme."""
    return app.send_static_file('Readme.html')


@app.route('/gui-test', methods=['GET'])
@cross_origin()
def send_gui_test():
    """Sent the static index page."""
    return app.send_static_file('index.html')


@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_text():
    """Analyze a text and send response."""
    req_contents = request.get_json()

    if req_contents:
        try:
            text_to_analyze = req_contents['content']
        except KeyError:
            response_dict = make_error_response("Malformed input JSON." +
                                                " Missing 'content' field.")
            return jsonify(response_dict)

        tagger = ttw.TreeTagger(TAGLANG=language.lower()[0:2],
                                TAGDIR=cmgr.get_treetagger_path())

        analyzer = syuzhet.SyuzhetWithFilter(language, tagger,
                                             emotions_array_length, emolex)
        analysis_result = analyzer.analyze_text(text_to_analyze)

        analyzer = None
        tagger = None

        result_dict = make_result_dict(analysis_result,
                                       emo_names=emotion_names)
        response_json = jsonify(result_dict)
        return response_json
    else:
        raise Exception("Empty input JSON")


def make_result_dict(data, request_id=None, corpus=None,
                     document=None, emo_names=None):
    """Create a JSON with the results and all other fields."""
    if data is None or data == []:
        res = make_error_response("Empty analysis result.")
        return res

    res = {}

    keys = [('id', request_id), ('corpus', corpus), ('document', document),
            ('emotion_names', emo_names), ('result', data)]

    for key, val in keys:
        if val is not None:
            res[key] = val

    return res


def make_error_response(msg="Couldn't satisfy request."):
    """Return a dictionary for an error response.
    Used to return an informative error message as JSON
    for a failed request."""
    return {'error': msg}


if __name__ == "__main__":
    app.run()
