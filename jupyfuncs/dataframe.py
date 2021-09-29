def rm_index(df):
    return df.loc[:, ~df.columns.str.match('Unnamed')]

def shuffle_df(df):
    return df.sample(frac=1).reset_index(drop=True)