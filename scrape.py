from bs4 import BeautifulSoup
import requests
import random
import boto3
import botocore
import os.path
import os

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
url = 'https://www.honolulupd.org/information/arrest-logs/'

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}
response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.text, features="html.parser")

bucket_name = "honolulupd-arrest-logs"
s3 = boto3.resource('s3')

def exists(key):
    try:
        s3.Object(bucket_name, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
    else:
        return True

def is_current(date):
    if not os.path.isfile('current.txt'):
        return False
    f = open('current.txt')
    if f.read() == date:
        return True
    return False

def upload(url):
    bucket = s3.Bucket(bucket_name)

    r = requests.get(url, allow_redirects=True, headers=headers)
    key = url.split('/')[::-1][0]

    if not exists(key):
        date = ('-'.join(key.split('-')[0:3]))
        if not is_current(date):
            open('current.pdf', 'wb').write(r.content)
            open('current.txt', 'w').write(date)
            os.system('python3 text.py')
        bucket.put_object(Key=key, Body=r.content)

for link in soup.find_all('a'):
    current_link = link.get('href')
    if current_link.endswith('pdf') and "Arrest_Log" in current_link:
        upload(current_link)
