# -*- coding: utf-8 -*-


def handler(event, context):

    method = event['context']['http-method']

    res = {}
    if method == 'GET':

        res['params'] = event['params']['querystring']

    else:

        res['params'] = event['body-json']


    return res