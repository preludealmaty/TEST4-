# coding: utf-8
# ����������� ��������� UTF-8.
from __future__ import unicode_literals

# ����������� ������ ��� ������ � JSON � ������.
import json
import logging

# ����������� ��������� Flask ��� ������� ���-�������.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# ��������� ������ � �������.
sessionStorage = {}

# ������ ��������� ���������� Flask.
@app.route("/", methods=['POST'])

def main():
# ������� �������� ���� ������� � ���������� �����.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# ������� ��� ���������������� ��������� �������.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # ��� ����� ������������.
        # �������������� ������ � �������������� ���.

        sessionStorage[user_id] = {
            'suggests': [
                "�� ����.",
                "�� ����.",
                "�������!",
            ]
        }

        res['response']['text'] = '������! ���� �����!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # ������������ ����� ������������.
    if req['request']['original_utterance'].lower() in [
        '�����',
        '�����',
        '�������',
        '������',
    ]:
        # ������������ ����������, ���������.
        res['response']['text'] = '����� ����� ����� �� ������.�������!'
        return

    # ���� ���, �� �������� ��� ������ �����!
    res['response']['text'] = '��� ������� "%s", � �� ���� �����!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# ������� ���������� ��� ��������� ��� ������.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # �������� ��� ������ ��������� �� �������.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # ������� ������ ���������, ����� ��������� �������� ������ ���.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # ���� �������� ������ ���� ���������, ���������� ���������
    # �� ������� �� ������.������.
    if len(suggests) < 2:
        suggests.append({
            "title": "�����",
            "url": "https://market.yandex.ru/search?text=����",
            "hide": True
        })

    return suggests