# coding:utf-8
import requests
import nltk
import re
from bs4 import BeautifulSoup
from collections import Counter
from .stop_words import stops
from .word_count.models import Result
from .data import db


def count_and_save_words(url):
    errors = []
    try:
        r = requests.get(url)
        # print('r.text: \n', r.text)
    except:
        errors.append("Unable to get URL. Please make sure it's valid and try again.")
        return {'error': errors}

    # html text processing
    # 使用beautifulsoup通过删除从URL返回的HTML标签来清理文本。
    raw = BeautifulSoup(r.text, 'html.parser').get_text()
    # print('raw: \n', raw)
    nltk.data.path.append('F:\\GitHubRepository\\flask-example\\flask_example\\nltk_data')
    # 以列表的形式返回raw中的所有token，nltk.word_tokenize可以读取字符制作token
    tokens = nltk.word_tokenize(raw)
    # print('tokens: \n', tokens)
    # 将tokens转换成nltk text object
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('[A-Za-z]')
    raw_words = [w for w in text if nonPunct.match(w)]
    # print('raw_words: \n', raw_words)
    raw_word_count = Counter(raw_words)
    # print('raw_word_count: \n', raw_word_count)
    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    # save the results
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return str(result.id)
    except:
        errors.append("Unable to add item to database.")
        return {'error': errors}