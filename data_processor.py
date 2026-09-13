import pandas as pd
import os

class UnsupportedFileType(Exception):
    pass
def read_file(file):
    file_name=file.filename
    file_type=os.path.splitext(file_name)[1].lower()
    if file_type=='.csv':
        data=pd.read_csv(file)
    elif file_type=='.xlsx':
        data=pd.read_excel(file)
    else:
        raise UnsupportedFileType
    return data

def clean_data(data):

    new_data=data.drop_duplicates()

    num_data=new_data.select_dtypes(include='number')
    num_data=num_data.fillna(num_data.median())
    text_data=new_data.select_dtypes(include='str').fillna("Unknown")

    new_data[new_data.select_dtypes(include='number').columns]=num_data
    new_data[new_data.select_dtypes(include='str').columns]=text_data

    return new_data

def calculate_statistics(data):
    num_data=data.select_dtypes(include='number')

    mean=num_data.mean().to_dict()
    median=num_data.median().to_dict()
    corr=num_data.corr().to_dict()

    return {"mean": mean, "median": median, "correlation": corr}