# -*- coding: UTF-8_general_ci -*-
#上傳個股資料到個股資料表
import pandas as pd


def monthly_report(year, month):
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911

    # 下載該年月的網站，並用pandas轉換成 dataframe
    html_df = pd.read_html('http://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year) + '_' + str(month) + '_0.html')

    # 處理一下資料
    df = html_df[0].copy()
    df = df[list(range(0, 10))]
    column_index = df.index[(df[0] == u'公司代號')][0]
    df.columns = df.iloc[column_index]
    df[u'當月營收'] = pd.to_numeric(df[u'當月營收'], 'coerce')
    df = df[~df[u'當月營收'].isnull()]
    df = df[df[u'公司代號'] != u'合計']
    df = df.reset_index()
    del df['index']
    return df
if __name__ == "__main__":
    print monthly_report(102,1)
