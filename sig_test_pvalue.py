import numpy as np
from scipy import stats

class sig_test_pvalue():

    def __init__(self):
        return
    
    def __err_detecting(self, bmean, bvar, bcnt, tmean, tvar, tcnt, test_type):
        err_message = ''
        #错误情况判断
        #如果count不为正数
        if bcnt <= 0 or tcnt <= 0:
            err_message = 'ERROR! Input count is invalid'
        #如果输入方差小于0
        elif tvar < 0 or bvar < 0:
            err_message = 'ERROR! Input variance is invalid'

        #只有ttest会出问题，chisq无置信区间
        if test_type == 'ttest':
            if bmean == 0:
                err_message = 'ERROR! base mean is 0, thus no Y/X confidence interval'
            elif tvar == 0 or bvar == 0:
                err_message = 'ERROR! Input variance is invalid'
        #chisq bmean和tmean应该小于1
        if test_type == 'chisq' and (bmean > 1 or tmean > 1):
            err_message = 'ERROR! 01 response should have mean < 1'
        return err_message


    def __conf_interval(self, bmean, bvar, bcnt, tmean, tvar, tcnt, significance_value = 0.95):
        _interval = 0
        Z_value = 1.96
        #其他显著性需求
        if significance_value != 0.95:
            tmp = significance_value + (1 - significance_value)/2
            #percentile function
            Z_value = round(stats.norm.ppf(tmp), 2)
        
        #错误情况判断
        if self.__err_detecting(bmean, bvar, bcnt, tmean, tvar, tcnt, 'ttest') == '':
            _interval = abs(Z_value/bmean) * np.sqrt(tvar/tcnt + (bvar/bcnt)*pow(tmean,2)/pow(bmean,2))
        return _interval
 

    def t_test(self, bmean = 0, bvar = 0, bcnt = 0, tmean = 0, tvar = 0, tcnt = 0):

        _interval = self.__conf_interval(bmean, bvar, bcnt, tmean, tvar, tcnt)
        err_message = self.__err_detecting(bmean, bvar, bcnt, tmean, tvar, tcnt, 'ttest')
        err_message1 = self.__err_detecting(bmean, bvar, bcnt, tmean, tvar, tcnt, 'other')

        if err_message1 == '':
            t = np.abs(round((bmean - tmean) / np.sqrt(bvar/bcnt + tvar/tcnt), 2))
            df = round(pow((bvar/bcnt+tvar/tcnt), 2) /
            (pow((bvar/bcnt), 2)/(bcnt-1)+pow((tvar/tcnt), 2)/(tcnt-1)))
            pval = round(stats.t.sf(t, df)*2, 2)  # two-sided pvalue = Prob(abs(t)>tt)

            if err_message == '':
                low_interval = round(tmean / bmean - 1 - _interval, 4)
                upper_interval = round(tmean / bmean - 1 + _interval, 4)
            if err_message != '':
                low_interval = 0
                upper_interval = 0
        else:
            t = 0
            pval = 0
            low_interval = 0
            upper_interval = 0
        
        return [t, pval, low_interval, upper_interval, err_message]
    

    def chisq(self, bmean = 0, bvar = 0, bcnt = 0, tmean = 0, tvar = 0, tcnt = 0):
        _interval = self.__conf_interval(bmean, bvar, bcnt, tmean, tvar, tcnt)
        err_message = self.__err_detecting(bmean, bvar, bcnt, tmean, tvar, tcnt, 'chisq')
        observ0 = np.array([[bmean*bcnt, bcnt - bmean*bcnt], [tmean*tcnt, tcnt - tcnt*tmean]])
        low_interval = 0
        upper_interval = 0

        try:
            chi, pval, dof, expected = stats.chi2_contingency(observ0)

        except:
            chi = 0
            pval = 0
            if err_message == '':
                err_message = 'ERROR! Other error occur'
        
        return [chi, pval, low_interval, upper_interval, err_message]



