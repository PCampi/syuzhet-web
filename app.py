from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import treetaggerwrapper as ttw
import pickle
import numpy as np
# import pudb

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
CORS(app)


@app.route('/', methods=['GET'])
def show_readme():
    """Show the help readme."""
    return app.send_static_file('Readme.html')


@app.route('/gui-test', methods=['GET'])
def send_gui_test():
    """Sent the static index page."""
    result = render_template("index.html")
    return result


@app.route('/analyze', methods=['POST'])
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

        analysis_result = _analyze(text_to_analyze, output_format='list')

        # pudb.set_trace()
        result = {'aggregate': analysis_result['aggregate'],
                  'emotions': _make_sent_result(analysis_result['sentences'])}

        result_dict = make_result_dict(result, emo_names=emotion_names)
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

    tpls = [('id', request_id), ('corpus', corpus), ('document', document),
            ('emotion_names', emo_names), ('result', data)]

    res = {k: v for k, v in tpls if v is not None}

    return res


def make_error_response(msg="Couldn't satisfy request."):
    """Return a dictionary for an error response.
    Used to return an informative error message as JSON
    for a failed request."""
    return {'error': msg}


def _make_sent_result(sentences):
    """Vertically stack the ndarrays and make them list.

    Parameters
    ----------
    sentences: List[np.ndarray]
        list of array, each representing the emotions in a sentence

    Returns
    -------
    each_emo: dict[str: List[int]]
        dictionary whose keys are the emotion names, and values the value
        of the emotion for each sentence
    """
    if sentences is None or sentences == []:
        return None

    tmp = np.stack(sentences)
    result = {emotion_names[i]: tmp[:, i].tolist()
              for i in range(len(emotion_names))}

    return result


def _analyze(text, output_format='list', also_get_sents=False):
    """Analyze a text using Syuzhet and TreeTagger."""
    tagger = ttw.TreeTagger(TAGLANG=language.lower()[0:2],
                            TAGDIR=cmgr.get_treetagger_path())

    analyzer = syuzhet.SyuzhetWithFilter(language, tagger,
                                         emotions_array_length, emolex)
    analysis_result = analyzer.analyze_text(text,
                                            get_sentences=also_get_sents)
    # pudb.set_trace()

    analyzer = None
    tagger = None

    if output_format == 'np.ndarray':
        result = {'aggregate': analysis_result['aggregate'],
                  'sentences': analysis_result['sentences']}
    elif output_format == 'list':
        result = {'aggregate': analysis_result['aggregate'].tolist(),
                  'sentences': [x.tolist()
                                for x in analysis_result['sentences']]}
    else:
        raise ValueError("Invalid argument output_format: {}"
                         .format(output_format))

    if also_get_sents:
        result['sentence_list'] = analysis_result['sentence_list']

    return result


if __name__ == "__main__":
    app.run()
