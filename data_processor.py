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