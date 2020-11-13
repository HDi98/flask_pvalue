#coding=utf-8

from flask import Flask, render_template, request, url_for, redirect, jsonify
from scipy import stats
from sig_test_pvalue import sig_test_pvalue
import numpy as np
import json

app = Flask(__name__)


@app.route("/pvalue", methods = ["POST", "GET"])
def test1():
    if request.method == 'GET':
        return render_template('input_outfit.html')
    if request.method == "POST":
        try:
            test_type = request.values.get("test_type")
            base_mean = float(request.form.get("base_mean"))
            base_var = float(request.form.get("base_var"))
            base_cnt = float(request.form.get("base_cnt"))
            test_mean = float(request.form.get("test_mean"))
            test_var = float(request.form.get("test_var"))
            test_cnt = float(request.form.get("test_cnt"))
        except:
            return '''<h1>ERROR</h1>'''

        if test_type == 'ttest':
            out = sig_test_pvalue().t_test(base_mean, base_var, base_cnt, test_mean, test_var, test_cnt)
            return render_template("show_pvalue.html", test_stat = out[0], P_value = out[1], message = out[4], lower_interval = out[2], upper_interval = out[3])
        elif test_type == 'chisq':
            out = sig_test_pvalue().chisq(base_mean, base_var, base_cnt, test_mean, test_var, test_cnt)
            return render_template("show_pvalue.html", test_stat = out[0], P_value = out[1], message = out[4], lower_interval = out[2], upper_interval = out[3])


#accept json data
@app.route("/pvalue_api", methods = ["GET", "POST"])
def get_json():
    #if request.method == "POST":
    #dict1 = request.args.get()
    try:
        test_type = request.args.get('test_type')
        base_mean = float(request.args.get("base_mean"))
        base_var = float(request.args.get("base_var"))
        base_cnt = float(request.args.get("base_cnt"))
        test_mean = float(request.args.get("test_mean"))
        test_var = float(request.args.get("test_var"))
        test_cnt = float(request.args.get("test_cnt"))
    except:
        out_new = {'message': 'error in input format'}
        return json.dumps(out_new)
    if test_type == 'ttest':
        out = sig_test_pvalue().t_test(base_mean, base_var, base_cnt, test_mean, test_var, test_cnt)
        out_new = {'test_stat':out[0], 'P_value': out[1], 'lower_interval': out[2], 'upper_interval': out[3], 'message': out[4]}
    elif test_type == 'chisq':
        out = sig_test_pvalue().chisq(base_mean, base_var, base_cnt, test_mean, test_var, test_cnt)
        out_new = {'test_stat':out[0], 'P_value': out[1], 'message': out[4]}
    else: 
        out_new = {'message': 'error in input test type'}
    #return '''<h1>The test result is: {}</h1>''' .format(out_new)
    return json.dumps(out_new)
    # else:
    #     return '<h1>只接受post请求</h>'


if __name__ == "__main__":
    app.run(port=8000, debug=True)
    #app.run(host='0.0.0.0', port=8000, debug=True)