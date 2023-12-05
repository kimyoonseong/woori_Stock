import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd

st.title('무슨 주식을 사야 부자가 되려나...')
st.sidebar.title('회사 이름과 기간을 입력하세요')
#st.sidebar.text('회사이름')
# Using object notation
company=st.sidebar.text_input('회사 이름')


#today = datetime.datetime.now()
start_year= datetime.date(2009,1,1)
end_year=datetime.date(2031,12,31)

d = st.sidebar.date_input(
    "시작일-종료일",
    (start_year, datetime.date(2031, 12, 31)),
    start_year,
    end_year,
    format="MM.DD.YYYY",
)
button_result = st.sidebar.button('주가 데이터 확인')

def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    url = "{0}?method={1}".format(base_url, method)   
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    df = df[['회사명','종목코드']]
    print('url: ', url)
    print("df: ", df)
    return df

def get_ticker_symbol(company_name):     
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values    
    ticker_symbol = code[0]
    return ticker_symbol

# 코드 조각 추가
if button_result==True:
    if company != "":
        stock_name=company
        ticker_symbol = get_ticker_symbol(stock_name)
        date_range=d     
        start_p = date_range[0]               
        end_p = date_range[1] + datetime.timedelta(days=1) 
        df = fdr.DataReader(ticker_symbol, start_p, end_p, exchange="KRX")
        df.index = df.index.date
        st.subheader(f"[{stock_name}] 주가 데이터")
        st.dataframe(df.head())
        chart_data=pd.DataFrame(df,columns=["Close"])
        st.line_chart(chart_data)

      
        excel_data = BytesIO()      
        df.to_excel(excel_data)

        st.download_button("엑셀 파일 다운로드", 
        excel_data, file_name='stock_data.xlsx')

        csv_data=BytesIO() 
        df.to_csv(csv_data)
        st.download_button("CSV 파일 다운로드", 
        csv_data, file_name='stock_data.csv')