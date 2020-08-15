# https://github.com/realsirjoe/instagram-scraper

from igramscraper.instagram import Instagram
import csv
import os

# manual setting
my_username = ''
my_password = ''
max_followers = 10000

# authentication supported
instagram = Instagram()
instagram.with_credentials(my_username, my_password)
instagram.login(two_step_verificator=True)
account = instagram.get_account(my_username)

# see who doesn't follow back
# Get 'max_followers' followers of the user, 100 a time with random delay between requests
followers = instagram.get_followers(account.identifier, max_followers, 100, delayed=True) 
following = instagram.get_following(account.identifier, max_followers, 100, delayed=True) 

followers_name = [ [follower.username, follower.full_name] for follower in followers['accounts'] ]    # a list of list
following_name = [ [following_user.username, following_user.full_name] for following_user in following['accounts'] ]

if not os.path.exists(r'./output/' + my_username):
    os.makedirs(r'./output/' + my_username)

with open(r'./output/' + my_username + r'/not_follow_back.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in following_name:
        if x not in followers_name:
            try:
                writer.writerow([x[0], x[1]])
            except:
                writer.writerow([x[0]])


# check lost followers
if not os.path.exists(r'./output/' + my_username + r'/my_followers.csv'):
    with open(r'./output/' + my_username + r'/my_followers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for x in followers_name:
            writer.writerow([x[0]])
else:
    followers_username = [ follower.username for follower in followers['accounts'] ]
    with open(r'./output/' + my_username + r'/my_followers.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        with open(r'./output/' + my_username + r'/lost_followers.csv', 'a', newline='') as csvfile_w:
            writer = csv.writer(csvfile_w)
            for row in rows:
                if row[0] not in followers_username:
                    writer.writerow([row[0]])

    with open(r'./output/' + my_username + r'/my_followers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for x in followers_name:
            writer.writerow([x[0]])
