import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

Path=st.sidebar.file_uploader('Excel')
if Path is not None:
    Data=pd.ExcelFile(Path)
    Sheet_names=Data.sheet_names
    Drop=st.sidebar.checkbox("Drop NH4",value=False)

    #フルスペクトル
    fig,ax=plt.subplots()
    Sheet_name=Sheet_names[0]
    df_full=pd.read_excel(Path,sheet_name=Sheet_name)
    
    if Drop==True:
        df_full=df_full.drop(df_full.loc[df_full["H or NH4"]=="NH4"].index)

    df_full=df_full.groupby("C").sum()
    ax=df_full.plot.bar(legend=False)
    ax.set_ylabel("Absolute Intensity")
    st.pyplot()

    #CIDスペクトル
    Sheet_name=Sheet_names[1]
    fig,ax=plt.subplots()
    df_cid=pd.read_excel(Path,sheet_name=Sheet_name)
    df_cid=df_cid.groupby("C").sum()
    
    #倍率の計算
    df_full["cid"]=df_cid.sum(axis=1)
    df_full["rate"]=df_full[df_full.columns[0]]/df_full["cid"]
    
    df=df_cid.mul(df_full["rate"],axis=0)
    ax=df.plot.bar(stacked=True)
    ax.set_ylabel("Absolute Intensity")
    st.pyplot()
    
    #規格化した表の表示
    df=df.fillna(0)
    df=df/sum(df.sum(axis=1))
    st.dataframe(df)
    
    #クリップボードにコピー
    if st.button("copy"):
        df.to_clipboard()