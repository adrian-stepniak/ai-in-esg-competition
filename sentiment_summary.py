import pandas as pd


def get_sentiment_label(row):
    labels = {
        'negative': row.negative_score,
        'neutral': row.neutral_score,
        'positive': row.positive_score
    }

    return max(labels, key=labels.get)


def summarize_sentiment(esg_component):
    df1 = pd.read_csv(f'sentiment_{esg_components}_guardian_df(1).csv', sep=';', index_col=0)
    df2 = pd.read_csv(f'sentiment_{esg_components}_df.csv', sep=';', index_col=0)

    df1 = df1[['companyName', 'versionCreated', 'negative_score', 'neutral_score', 'positive_score']]
    df2 = df2[['companyCode', 'versionCreated', 'negative_score', 'neutral_score', 'positive_score']]

    df1.columns = df2.columns
    df = pd.concat([df1, df2], ignore_index=True)

    df.columns = ['company', 'date', 'negative_score', 'neutral_score', 'positive_score']

    df['year'] = df['date'].apply(lambda date_str: date_str.split('-')[0])
    df['month'] = df['date'].apply(lambda date_str: date_str.split('-')[1])
    df = df[df['year'].isin(['2020', '2021'])]
    df['period'] = df.apply(lambda row: f'{row.year}-{row.month}', axis=1)

    df['label'] = df.apply(get_sentiment_label, axis=1)

    grouping_df = df[['company', 'period', 'label']].value_counts()
    grouping_df = grouping_df.unstack(2)

    grouping_df = grouping_df.fillna(0)
    grouping_df['pos_perc'] = grouping_df.apply(lambda row: row.positive / sum(row), axis=1)
    grouping_df['neg_perc'] = grouping_df.apply(lambda row: row.negative / sum(row), axis=1)

    grouping_df.to_excel(f'news_sentiment_{esg_components}.xlsx')


esg_components = ['ceo', 'gov', 'cyb', 'env']

for esg_component in esg_components:
    summarize_sentiment(esg_components)
