import logging
import json
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import sys, getopt

# load objects from libraries
tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
stops = set(stopwords.words("english"))

# create logger
logging.basicConfig()
log = logging.getLogger('inference_topics')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def clean_text(row):
    row = row.lower()
    row = tokenizer.tokenize(row)
    row = [token for token in row if token not in stops]
    row = [token for token in row if not token.isnumeric()]
    row = [token for token in row if len(token) > 1]
    row = [lemmatizer.lemmatize(token) for token in row]
    return row


def handler(event):
    log.info('-------- START --------')
    try:
        event = json.loads(event)
    except Exception as e:
        log.error("try running the scritpt with a valid json string python script.py \"{\"text\": \"some text\"}\"")
        raise e
    try:
        log.info(f'received event: {event}')
        response = event
        file_path = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(file_path, "notebooks/model")
        # load model and dictionary
        log.info(f'loading model under {model_path}')
        lda = LdaModel.load(f'{model_path}/lda_imdb.model')
        log.info(f'loading dictionary under {model_path}')
        dscr_dictionary = Dictionary.load(f'{model_path}/imdb.dictionary')
        text = event['text']
        bow = dscr_dictionary.doc2bow(clean_text(text))
        vector = lda[bow]
        response['output'] = lda.print_topic(max(vector, key=lambda item: item[1])[0])
        response['vector'] = vector
        log.info(f'inferred document topic distribution: "{response["output"]}"e')
    except Exception as e:
        raise e
    log.info(response)
    log.info('-------- END --------')
    return response


if __name__ == "__main__":
    handler(sys.argv[1])
