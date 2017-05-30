# -*- coding: utf-8 -*-
import subprocess
import json
import ast
import re
import traceback
import sys


LAMBDA_METHOD = 'handler'
LAMBDA_DIR = '/home/lambda/dev'
LAMBDA_FILE = 'lambda.py'
LAMBDA_PARAMS = {
    "context": {
        "stage": "local",
        "http-method": "",
        "resource-path": "",
        "source-ip": "localhost"
    },
    "body-json": {},
    "params": {
        "path": {},
        "querystring": {},
        "header": {
            "Accept": "*/*",
            "User-Agent": "Local",
            "Host": "localhost"
        }
    },
    "base64-body": "",
    "stage-variables": {}
}



def application(env, start_response):
    try:

        req = Request(env)
        lam = Lambda()


        lam.set_params(req)


        try:


            status_code, ret = lam.execute_lambda()


            start_response(status_code, [('Content-Type','application/json')])
            return [ json.dumps(ret).encode("utf-8") ]


        except Exception:
            start_response('500', [('Content-Type','application/json')])
            return [ json.dumps({'stackTrace': lam.stack_trace}).encode("utf-8") ]



    except Exception as e:

        start_response('500', [('Content-Type','application/json')])
        return [ json.dumps({'stackTrace': traceback.format_exc()}).encode("utf-8") ]





class Request(object):

    def __init__(self, env):
        self.method = env['REQUEST_METHOD']
        self.query_string = self._get_query_string(env['QUERY_STRING'])
        self.path = add_slash(env['PATH_INFO'])
        self.body = self._get_body(env)
        self.path_params = env['PATH_INFO']

    def _get_query_string(self, query_string):
        return_dict = {}
        for val in query_string.split('&'):
            if val is '':
                continue
            v = val.split('=')
            return_dict[v[0]] = v[1]
        return return_dict

    def _get_body(self, env):
        length = env['CONTENT_LENGTH']
        if length is "" or length is 0 or length is '0':
            return {}

        body = env['wsgi.input'].read(int(length))
        return json.loads(body)



class Lambda(object):


    def set_params(self, req_obj):
        LAMBDA_PARAMS['context']['http-method'] = req_obj.method
        LAMBDA_PARAMS['params']['path'] = req_obj.path_params
        LAMBDA_PARAMS['params']['querystring'] = req_obj.query_string
        LAMBDA_PARAMS['body-json'] = req_obj.body

        params_file = "{}/params.json".format(LAMBDA_DIR)

        with open(params_file, mode='w') as f:
            f.write(json.dumps(LAMBDA_PARAMS))

    def execute_lambda(self):

        process = subprocess.run(self._lambda_command().split(" "),
                                    stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        stdout_data = process.stdout.decode('utf-8')


        self._write_log(stdout_data)
        self._check_exception(stdout_data)
        stdout_data = self._extract_result(stdout_data)
        status_code = self._check_status_code(stdout_data)


        return status_code, stdout_data


    def _write_log(self, ret):
        params_file = "{}/log/debug.log".format(LAMBDA_DIR)

        with open(params_file, mode='a') as f:
            f.write(ret)


    def _lambda_command(self):
        return "python-lambda-local -f {} -t 30 {}/{} {}/params.json".format(LAMBDA_METHOD, LAMBDA_DIR, LAMBDA_FILE, LAMBDA_DIR)


    def _extract_result(self, ret):
        ret = ret.split("RESULT:\n")[1].split("\n[")[0]
        return ast.literal_eval(ret)


    def _check_status_code(self, ret):

        error_key = 'Traceback'
        if error_key in ret:
            return '500'

        return '200'


    def _check_exception(self, ret):
        res = ret.split("Process Process-1:")

        if (len(res) is 2):
            self.stack_trace = res[1].split('\n')
            raise Exception("Lambda Error")




def add_slash(val):
    val = convert_str(val)

    if val[-1] != '/':
        return val + '/'

    return val


def convert_str(val):
    if type(val) is not str:
        return str(val)

    return val
