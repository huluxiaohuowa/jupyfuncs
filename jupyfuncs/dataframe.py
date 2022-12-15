def rm_index(df):
    return df.loc[:, ~df.columns.str.match('Unnamed')]


def rm_col(df, col_name):
    return df.loc[:, ~df.columns.str.match(col_name)]


def shuffle_df(df):
    return df.sample(frac=1).reset_index(drop=True)
