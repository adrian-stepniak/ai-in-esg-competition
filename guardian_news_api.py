from time import sleep

import pandas as pd
import requests

key = 'API_Key'
show_fields_args = 'bodyText'

company_names = ['"BP"', '"Equinor"', '"Hindustan Petroleum"', '"HPCL"', '"Bharat Petroleum"', '"BPCL"', '"DCC"',
                 '"PBF ENERGY"',
                 '"Z Energy"', '"Murphy USA"', '"MurphyUSA"', '"Petronet LNG"', '"Petronet"', '"Senex Energy"',
                 '"Mahindra"',
                 '"Honda"', '"BMW"', '"Tata Motors"', '"Toyota"', '"Nissan"', '"Faurecia"', '"Schaeffler"',
                 '"Mitsubishi"', '"Mazda"']

gov_query_args = ['"audit inconsistencies"', '"tax fraud"', '"governance controversies"', '"corporate governance"']

cyb_query_args = ['scam', 'hack', 'cybersecurity', '"cyber security"', '"cyber-security"',
                  '"personal data leak"', '"data leak"', 'phishing', 'malware', 'ransomware', '"cyber attack"',
                  'cyberattack',
                  'cyberattack', 'cyberthreat', '"cyber threat"', 'cyber-threat', '"fake call"', 'ddos',
                  '"Social engineering"', 'Backdoor', '"cyber vulnerabilities"', 'cybercriminal']

ceo_query_args = ['CEO', 'CE', '"chief executive officer"', '"chief administrator"', '"chief executive"',
                  '"CEO succesion"',
                  '"CEO controversy"', '"CEO said"', 'director', 'boss', '"CEO respond"', '"CEO scandal"',
                  '"CEO fraud"',
                  '"CEO action"', '"CEO apologizes"', '"CEO crime"', '"CEO retirement"', '"CEO retiring"',
                  '"CEO explains"',
                  '"CEO helps"']

env_query_args = ['"green washing"', 'greenwashing', 'green-washing', '"green sheen"', 'greensheen',
                  '"green marketing"',
                  '"green PR"', 'greenscamming', '"green scamming"', 'green-scamming', 'greenscam', '"green scam"',
                  '"green business"', '"green speak"', 'greenspeak', '"environment protection"', 'ecology',
                  '"radioactive waste"', '"hazardous waste"', '"illegal dumping"', '"fly dumping"',
                  '"taxic waste dumping"',
                  '"electronic waste"', '"toxic waste"', 'environment', 'ecology']


def df_add(df, index, article, company):
    df.at[index, 'text'] = article.get('webTitle')
    df.at[index, 'storyText'] = article.get('fields').get('bodyText')
    df.at[index, 'companyName'] = company_names[company].replace('"', '')
    return index + 1


def read_news(company_names, key, show_fields_args, query_args):
    df = pd.DataFrame()
    for company in range(company_names.__len__()):
        base_url = 'https://content.guardianapis.com/search?'
        api_key = '&api-key={}'.format(key)
        show_fields = '&show-fields={}&page-size=50&lang=en'.format(show_fields_args)
        from_date = '&from-date=2020-01-01'
        query_ask = "("
        current_page = 'page='
        for item in range(query_args.__len__()):
            if item == 0:
                query_ask = query_ask + query_args[item]
            elif item == query_args.__len__() - 1:
                query_ask = query_ask + ' OR ' + query_args[item] + ')'
            else:
                query_ask = query_ask + ' OR ' + query_args[item]
        query = '&q={} AND {}'.format(company_names[company], query_ask)
        whole_query = (base_url + from_date + show_fields + query + api_key).replace(' ', '%20')

        response = requests.get(whole_query)
        sleep(0.25)
        response_dict = response.json().get('response')
        temp_df = pd.DataFrame(columns=['text', 'storyText', 'companyName'])
        if response_dict.get('pages') is not None:
            for page in range(response_dict.get('pages') + 1):
                index = 0
                if page == 0:
                    continue
                elif page == 1:
                    for article in response_dict.get('results'):
                        index = df_add(temp_df, index, article, company)
                else:
                    new_whole_query = (base_url + current_page + str(
                        page) + from_date + show_fields + query + api_key).replace(' ', '%20')
                    new_response = requests.get(new_whole_query)
                    sleep(0.25)
                    for article in new_response.json().get('response').get('results'):
                        index = df_add(temp_df, index, article, company)
            df = df.append(temp_df, ignore_index=True)
    return df


gov_guardian_df = read_news(company_names, key, show_fields_args, gov_query_args)
gov_guardian_df.to_csv('gov_guardian_df.csv')

cyb_guardian_df = read_news(company_names, key, show_fields_args, cyb_query_args)
cyb_guardian_df.to_csv('cyb_guardian_df.csv')

ceo_guardian_df = read_news(company_names, key, show_fields_args, ceo_query_args)
ceo_guardian_df.to_csv('ceo_guardian_df.csv')

env_guardian_df = read_news(company_names, key, show_fields_args, env_query_args)
env_guardian_df.to_csv('env_guardian_df.csv')
