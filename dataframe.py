def rm_index(df):
    return df.loc[:, ~df.columns.str.match('Unnamed')]