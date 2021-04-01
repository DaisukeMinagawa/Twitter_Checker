# USE Twit_checher2 from venv

import tweepy
import sqlite3
import os
import pathlib
import platform
from plyer import notification
import requests
import notify2


# crontab -eで設定する場合、DISPLAY=:0.0 という値を渡す必要がある
# * * * * * DISPLAY=:0.0 python /home/username/Documents/file.py


# Twitter認証キーの設定
consumer_key = \
    "oE4Wh22jT42ujQ0tw4INu1S8H"
consumer_secret = "79nvlGzpudryUUphLqWLvu46CjrptWfNekjEcmFkEF6HXbYGeL"
access_token = "2558440268-S4FGNiERh8VEbmZQslwS6LSLWEZDh85PAtfACA4"
access_token_secret = "1Dn8fcdeWRiIfsUMOJeMV1G5lfhTKDqeUXneYToKHRgnl"


# Twitter OAuth認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# LINE Notify access token
url = "https://notify-api.line.me/api/notify"
access_token = 'fGu3UzaAzyGNuIiUNjUdm2H8x85oFNX7mIxr3FWi4po'
headers = {'Authorization': 'Bearer ' + access_token}


class Database:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.dbpath = os.path.join(BASE_DIR, 'db.sqlite3')
        self.conn = sqlite3.connect(self.dbpath)
        self.c = self.conn.cursor()
        self.c2 = self.conn.cursor()


db = Database()


def output_users_from_db():
    return db.c.execute('select name, comment from display_twitterusers')


def update_comment(name, comment='null'):
    db.c2.execute(
        """update display_twitterusers set comment = ? where name = ?""", (comment, name,))
    db.conn.commit()


def letters_chk(name):
    return db.c2.execute('select comment from display_twitterusers where name = ?', (name,))


def play_sound():
    #current_dir = os.path.abspath("airplane_ping.mp3")
    #print(current_dir)
    #os.system("mpg123  " + str(current_dir) )
    current_dir = pathlib.Path(__file__).resolve().parent
    os.system('mpg123 ' + str(current_dir) + '/airplane_ping.mp3')


def send_message_to_line(name, message, twit_url):
    message = name + '\n' + message + '\n' + twit_url
    payload = {'message': message}
    r = requests.post(url, headers=headers, params=payload, )


def generate_url(screen_name, id_str):
    time_line = api.user_timeline(screen_name=screen_name)
    # https://twitter.com/TwitterJP/status/1216303977995952128
    screen_name = time_line[0].user.screen_name
    id_str = time_line[0].id_str
    return 'https://twitter.com/' + screen_name + '/status/' + id_str


if __name__ == "__main__":
    api = tweepy.API(auth)
    users_info_from_db = output_users_from_db()
    for user_info_on_db in users_info_from_db:
        # user_info_on_db[0] = name, user_info_on_db[0].text = comment
        time_line = api.user_timeline(screen_name=user_info_on_db[0])
        # Get comment form DB and Check the letters from DB
        for comment in letters_chk(user_info_on_db[0]):
            # print(user_info_on_db[0], comment[0])
            if time_line[0].text == comment[0]:
                print('既読')
            else:
                print('新規投稿' + time_line[0].text)
                update_comment(user_info_on_db[0], time_line[0].text)
                currnet_dir = pathlib.Path(__file__).resolve().parent
                if platform.system() == 'Windows':
                    notification.notify(
                        title=user_info_on_db[0],
                        message=time_line[0].text,
                        app_name='Twit_checker',
                        app_icon=str(currnet_dir) + '/twitter.ico'
                    )
                    send_message_to_line(time_line[0].user.name, time_line[0].text,
                                         generate_url(time_line[0].user.screen_name, time_line[0].id_str))
                # notify2はLinux環境でないと、読み込ませるだけでdbusが無いとエラーが出されてしまう。
                elif platform.system() == 'Linux':
                    notify2.init(u"Twitter_checker")
                    currnet_dir = pathlib.Path(__file__).resolve().parent
                    n = notify2.Notification(user_info_on_db[0], time_line[0].text, str(currnet_dir) + '/twitter.ico')
                    n.show()
                    play_sound()
                    send_message_to_line(time_line[0].user.name, time_line[0].text,
                                                         generate_url(time_line[0].user.screen_name, time_line[0].id_str))
                elif platform.system() == 'Darwin':
                    os.system(
                        "osascript -e \'display notification \"{}\" with title \"{}\" subtitle "
                        "\"{}\" sound name \"Frog\"\'".format(time_line[0].text, user_info_on_db[0], "新規投稿"))
                    send_message_to_line(time_line[0].user.name, time_line[0].text,
                                         generate_url(time_line[0].user.screen_name, time_line[0].id_str))



