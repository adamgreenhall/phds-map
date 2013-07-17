import pandas as pd
import pandasjson, simplejson

def to_jsonblob(df, reset=False): 
    if reset:
        return simplejson.loads(df.reset_index().to_json(orient='records'))
    else:
        return simplejson.loads(df.to_json(orient='records'))
pd.DataFrame.to_jsonblob = to_jsonblob


def set_index_name(df, nm): 
    df.index.name = nm
    return df
pd.DataFrame.set_index_name = set_index_name