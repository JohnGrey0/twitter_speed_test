import configparser
import speedtest
import tweepy

def get_speed():
    st = speedtest.Speedtest()
    return st.download()/1000/1000, st.upload()/1000/1000

def get_config():
    config = configparser.ConfigParser()
    config.read('twitter_api.config')
    return config

def send_tweet(body):
    config = get_config()
    api_key = config.get('TWITTER', 'api_key')
    api_secret = config.get('TWITTER', 'api_secret')
    access_key = config.get('TWITTER', 'access_key')
    access_secret = config.get('TWITTER', 'access_secret')
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    api.update_status(body)
    
def speed_test():
    variables = {'pay_down': 1000,
                 'pay_up': 40,
                 'min_down': 750,
                 'internet_prov': 'Comcast',
                 'loc': 'Someplace'}
    variables['down'], variables['up'] = get_speed()
    
    body = r"""Hey @{internet_prov} why is my internet speed {down} Mbps DOWN / {up} Mbps UP when I pay for {pay_down} Mbps DOWN / {pay_up} Mbps UP in {loc}? @ComcastCares @xfinity #comcast #speedtest""".format(**variables)
    
    if variables['down'] <= variables['min_down']:
        send_tweet(body)
        
if __name__ == '__main__':
    speed_test()