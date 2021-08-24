import configparser
import speedtest
import tweepy

def get_speed():
    st = speedtest.Speedtest()
    return st.download()/1000/1000, st.upload()/1000/1000

def get_config():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('twitter_api.config')
    return config

def send_tweet(body, variables):
    auth = tweepy.OAuthHandler(variables['api_key'], variables['api_secret'])
    auth.set_access_token(variables['access_key'], variables['access_secret'])
    api = tweepy.API(auth)
    api.update_status(body)
    
def speed_test():
    config = get_config()
    variables = {'api_key': config.get('TWITTER', 'api_key'),
                 'api_secret': config.get('TWITTER', 'api_secret'),
                 'access_key': config.get('TWITTER', 'access_key'),
                 'access_secret': config.get('TWITTER', 'access_secret'),
                 'pay_down': float(config.get('TWITTER', 'pay_down')),
                 'pay_up': float(config.get('TWITTER', 'pay_up')),
                 'min_down': float(config.get('TWITTER', 'min_down')),
                 'isp_handle': config.get('TWITTER', 'isp_handle'),
                 'location': config.get('TWITTER', 'location'),
                 'additional_message': config.get('TWITTER', 'additional_message')}
    variables['down'], variables['up'] = get_speed()
    
    body = r"""Hey {isp_handle} why is my internet speed {down} Mbps DOWN / {up} Mbps UP when I pay for {pay_down} Mbps DOWN / {pay_up} Mbps UP in {location}? {additional_message}""".format(**variables)
    
    if variables['down'] <= variables['min_down']:
        send_tweet(body, variables)
        
if __name__ == '__main__':
    speed_test()