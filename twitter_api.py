from time import sleep

import pandas as pd
from searchtweets import collect_results, gen_rule_payload, load_credentials

premium_search_args = load_credentials("./.twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

companies_profiles = ['bp_plc', 'Equinor', 'HPCL', 'BPCLimited', 'dccplc', 'zenergynz', 'MurphyUSA', 'PetronetLNGLtd',
                      'SenexEnergy', 'MahindraRise', 'Honda', 'BMW', 'TataMotors', 'Toyota', 'Nissan',
                      'Faurecia', 'SchaefflerGroup', 'mitsucars', 'MazdaUSA']

companies_hash = ['#PBFEnergy']

env_base_query = '(#greenwashing OR #greenscam OR #environment OR #ecology) @{} lang:en'
social_base_query = 'from:{} lang:en -has:mentions'

env_tweets_df = pd.DataFrame(columns=['text', 'createDate', 'company'])
social_tweets_df = pd.DataFrame(columns=['text', 'createDate', 'company'])


def tweets_df(base, company_name):
    temp_df = pd.DataFrame(columns=['text', 'createDate', 'company'])

    query = base.format(company_name)
    query_cmp = gen_rule_payload(query, from_date="2020-01-01", results_per_call=100)
    tweets = collect_results(query_cmp, max_results=100, result_stream_args=premium_search_args)
    sleep(3)

    temp_df['text'] = [tweet.text for tweet in tweets]
    temp_df['createDate'] = [tweet.created_at_datetime for tweet in tweets]
    temp_df['company'] = company_name

    return temp_df


def tweets_df_hash(base, company_name):
    new_base = base.replace('@', '').replace('from:', '')
    return tweets_df(new_base, company_name)


for company in companies_profiles:
    env_tweets_df = env_tweets_df.append(tweets_df(env_base_query, company))
    env_tweets_df.drop_duplicates().to_csv('env_tweets_df.csv')

    social_tweets_df = social_tweets_df.append(tweets_df(social_base_query, company))
    social_tweets_df.drop_duplicates().to_csv('social_tweets_df.csv')

for company in companies_hash:
    env_tweets_df = env_tweets_df.append(tweets_df_hash(env_base_query, company))
    env_tweets_df.drop_duplicates().to_csv('env_tweets_with_hash_df.csv')

    social_tweets_df = social_tweets_df.append(tweets_df_hash(social_base_query, company))
    social_tweets_df.drop_duplicates().to_csv('social_tweets_with_hash_df.csv')
