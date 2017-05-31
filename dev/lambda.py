# -*- coding: utf-8 -*-


def handler(event, context):

    res = {}
    res['method'] = event['context']['http-method']
    res['url'] = event['params']['path']
    res['query-string'] = event['params']['querystring']
    res['json-body'] = event['body-json']

    return res