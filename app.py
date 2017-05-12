from flask import Flask, request, jsonify
import treetaggerwrapper as ttw
import pickle
import pudb

import syuzhet
from path_problem_resolver import get_absolute_path
from configuration_manager import ConfigurationManager

cmgr = ConfigurationManager("config.json")
cmgr.load_config()

language = cmgr.get_default_language()
emotions_array_length = cmgr.get_emotion_array_length()
data_dir = cmgr.get_data_dir()
emolex_filename = cmgr.get_emolex_filename(language)

# pudb.set_trace()
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


@app.route('/test/tokenization', methods=['POST'])
def test_json_tokenization():
    json_contents = request.get_json()

    pudb.set_trace()
    if json_contents:
        try:
            sentences = json_contents['contents']  # list of lists of str
            from syuzhet.lemmatization import lemmatize
            lemmatized_text = [lemmatize(s, tagger) for s in sentences]
            result = {'lemmatized_sentences': lemmatized_text}
            return jsonify(result)
        except KeyError as e:
            raise e

    else:
        raise Exception("No contents in the JSON!")


if __name__ == "__main__":
    app.run()
