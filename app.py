from flask import Flask, request, jsonify
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

tagger = ttw.TreeTagger(TAGLANG=language.lower()[0:2],
                        TAGDIR=cmgr.get_treetagger_path())

analyzer = syuzhet.Syuzhet(language, tagger, emotions_array_length, emolex)


# Main application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_readme():
    """Show the help readme."""
    return app.send_static_file('Readme.html')


# @app.route('/test/tokenization', methods=['POST'])
# def test_json_tokenization():
#     json_contents = request.get_json()
#
#     if json_contents:
#         try:
#             sentences = json_contents['contents']  # list of lists of str
#             from syuzhet.lemmatization import lemmatize
#             lemmatized_text = [lemmatize(s, tagger) for s in sentences]
#             result = {'lemmatized_sentences': lemmatized_text}
#             return jsonify(result)
#         except KeyError as e:
#             raise e
#
#     else:
#         raise Exception("No contents in the JSON!")


@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze a text and send response."""
    req_contents = request.get_json()

    if req_contents:
        text_to_analyze = req_contents['content']
        analysis_result = analyzer.analyze_text(text_to_analyze)

        result_dict = make_result_dict(analysis_result,
                                       emo_names=emotion_names)
        response_json = jsonify(result_dict)

        return response_json
    else:
        raise Exception("Empty input JSON")


def make_result_dict(result, id=None, corpus=None, document=None,
                     emo_names=None):
    """Create a JSON with the results and all other fields."""
    res = dict()

    keys = [('id', id), ('corpus', corpus), ('document', document),
            ('emotion_names', emo_names), ('result', result)]

    for k in keys:
        if k[1] is not None:
            res[k[0]] = k[1]

    return res


if __name__ == "__main__":
    app.run()
