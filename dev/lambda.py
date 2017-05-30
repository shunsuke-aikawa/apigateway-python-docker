# -*- coding: utf-8 -*-


def handler(event, context):

    res = {}
    res['method'] = vent['context']['http-method']
    res['url'] = event['params']['path']
    res['query-string'] = event['params']['querystring']
    res['json-body'] = event['body-json']

    return res