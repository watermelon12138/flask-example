# coding:utf-8
import operator
import json
from flask import render_template, request, Blueprint, jsonify
from flask_example.worker import conn
from rq import Queue
from rq.job import Job
from .models import Result


word_count = Blueprint('word_count', __name__)
# initialized a queue based on that connection.
q = Queue(connection=conn)

@word_count.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@word_count.route('/start', methods=['POST'])
def get_counts():
    # this import solves a rq bug which currently exists
    from flask_example.help_func import count_and_save_words
    # Deserialize a JSON document to a Python object.
    data = json.loads(request.data.decode())
    # print('data: \n', data)
    # get url
    url = data["url"]
    if not url[:8].startswith(('https://', 'http://')):
        url = 'http://' + url
    # count word and save result to database
    result_id = count_and_save_words(url)
    return result_id


@word_count.route("/results/<result_id>", methods=['GET'])
def get_results(result_id):

    if result_id.isdigit():
        result = Result.query.filter_by(id=int(result_id)).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        # print(jsonify(results))
        return jsonify(results)

    else:
        return "Nay!", 202

# @word_count.route('/start', methods=['POST'])
# def get_counts():
#     # this import solves a rq bug which currently exists
#     from flask_example.help_func import count_and_save_words
#     # Deserialize a JSON document to a Python object.
#     data = json.loads(request.data.decode())
#     print('data: \n', data)
#     # get url
#     url = data["url"]
#     if not url[:8].startswith(('https://', 'http://')):
#         url = 'http://' + url
#     # start job
#     job = q.enqueue_call(
#         func=count_and_save_words, args=(url,), result_ttl=5000
#     )
#     # return created job id
#     return job.get_id()
#
# @word_count.route("/results/<job_key>", methods=['GET'])
# def get_results(job_key):
#     # Fetches a persisted job from its corresponding Redis key and instantiates it.
#     job = Job.fetch(job_key, connection=conn)
#
#     if job.is_finished:
#         result = Result.query.filter_by(id=job.result).first()
#         results = sorted(
#             result.result_no_stop_words.items(),
#             key=operator.itemgetter(1),
#             reverse=True
#         )[:10]
#         return jsonify(results)
#     else:
#         return "Nay!", 202