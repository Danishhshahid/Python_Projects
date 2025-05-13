from fileinput import fileno
import streamlit as st
import pandas as pd
from io import BytesIO


st.set_page_config(page_title="File Converter", page_icon="📂", layout="wide")
st.title("file converter & cleaner")
st.write("upload CVS or Excel file,Clean and convert it to different format")

files = st.file_uploader("Upload your file", type=['csv', 'xlsx'],accept_multiple_files=True)
if files :
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        st.subheader(f"{file.name} -Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name} "):
            df = df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())

            if st.checkbox (f"file Missing value - {file.name}"):
                df = df.fillna(df.select_dtypes(include=['number']).mean())
                st.success("File missing value with mean")
                st.dataframe(df.head())

            selected_columns = st.multiselect(f"Select columns to keep - {file.name}",df.columns,default = df.columns)
            df = df[selected_columns]
            st.dataframe(df.head())

            if st.checkbox(f"show Chart - {file.name}"):
                if not df.select_dtypes(include='number').empty:
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
                    st.success("Chart displayed")
                else:
                    st.warning("No numeric columns to plot!")

            format_choise=st.radio(f"Convert {file.name} to:",["csv","xlsx"],key=file.name)

            if st.button (f"{file.name} as {format_choise}"):
                output =BytesIO()
                if format_choise == "csv":
                    df.to_csv(output,index=False)
                    mine = "text/csv"
                    new_name = file.name.replace(ext,"csv")

                else:
                    df.to_excel(output,index=False,engine='openpyxl')
                    mine = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext,"xlsx")

                output.seek(0)
                st.download_button("Download File", file_name=new_name,data=output,mime=mine)
                st.success("processing Completed !")


