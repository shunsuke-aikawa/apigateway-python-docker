# -*- coding: utf-8 -*-


def handler(event, context):

    method = event['context']['http-method']

    res = {}
    res['method'] = method
    res['url'] = event['params']['path']
    res['query-string'] = event['params']['querystring']
    res['json-body'] = event['body-json']

    if method == 'GET':
        pass
    else:
        pass

    return res