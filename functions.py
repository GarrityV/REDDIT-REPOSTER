import base64
import praw
import praw.exceptions
import prawcore.exceptions
from datetime import date
from PIL import Image
import requests
import mimetypes
import json
import menus


def view_post(p):  # FUNCTION PART OF view_all()
    file_path = None

    # DOWNLOAD AND DISPLAY IMAGE IF POST IS IMAGE
    if p['url'].endswith(('jpg', 'jpeg', 'png', 'gif')):
        # DOWNLOAD IMAGE
        response = requests.get(p['url'])
        mime_type = response.headers['content-type']
        file_extension = mimetypes.guess_extension(mime_type)
        image_data = response.content
        file_path = 'image' + file_extension
        with open(file_path, 'wb') as image_file:
            image_file.write(image_data)

        # DISPLAY IMAGE
        img = Image.open('image' + file_extension)
        img.show()
        print(p['url'])

    # DISPLAY POST CONTENTS
    if file_path:
        print(f'{p["url"]}')
    elif p['desc']:
        print(p['desc'])
    else:
        print(p['url'])


def save_login(user, passwd):
    # CREATE DICT FOR LOGIN INFO
    login_info = {
        user: {
            "username": user,
            "password": passwd
        }
    }

    # ENCODE DICT AS JSON OBJECT
    login_json = json.dumps(login_info, indent=4)

    # WRITE JSON OBJECT TO FILE
    with open('login_info.json', 'w') as f:
        f.write(login_json)
        print("Login saved successfully.")


def load_login():
    try:
        # READ JSON FROM FILE
        with open('login_info.json', 'r') as f:
            accounts = json.load(f)
    except FileNotFoundError:
        # CREATE NEW JSON FILE
        print('File login_info.json not found.\n'
              'Creating new file login_info.json')

        with open('login_info.json', 'w') as f:
            accounts = {}
    except json.decoder.JSONDecodeError:
        # FILE IS EMPTY
        accounts = {}

    # DECODE JSON AND EXTRACT LOGIN INFO
    #login_info = json.loads(login_json)
    #accounts = []
    #for username, account in login_info.items():
    #    password = account['password']
    #    accounts.append({'username': username, 'password': password})

    account_list = []
    for username, account in accounts.items():
        account_list.append(account)

    return account_list


def reddit_auth():  # LOGIN AUTHENTICATION
    global reddit
    access = False
    while not access:
        # DISPLAY LOGIN MENU
        menus.login_menu()
        menu_choice = input("Enter: ")

        # MENU CHOICE 1
        if menu_choice == '1':
            # GET LOGIN FROM USER
            username = input("Enter username: ")
            password = input("Enter password: ")

            # ATTEMPT TO AUTHENTICATE
            try:
                reddit = praw.Reddit(client_id='REPLACE',
                                     client_secret='REPLACE',
                                     username=username,  # base64.b64decode(username)
                                     password=password,  # base64.b64decode(password)
                                     user_agent='REPLACE')

                user = reddit.user.me()
                if user is not None:
                    access = True
                    print(f'Logged in as {user}')

                    # CHECK IF LOGIN IS SAVED
                    accounts = load_login()
                    login_saved = False
                    if username in accounts:
                        login_saved = True

                    # ASK TO SAVE LOGIN IF NOT SAVED
                    if not login_saved:
                        save_login_info = input("Save login info? [Y]es/[N]o\n")
                        if save_login_info.lower() == 'y':
                            save_login(username, password)
                else:
                    print('Invalid login.\n'
                          'Restarting...')
            except prawcore.exceptions.OAuthException:
                access = False
                print('Error occurred while trying to login.\n'
                      'Have you created a Reddit developer app?')

        # MENU CHOICE 2
        elif menu_choice == '2':
            try:
                # READ JSON FILE
                accounts = load_login()
            # IF JSON FILE NOT FOUND
            except FileNotFoundError:
                print('File login_info.json not found.\n'
                      'Creating new file login_info.json')

                with open('login_info.json', 'w') as f:
                    accounts = {}

            # CHECK IF ACCOUNTS IS EMPTY
            if not accounts:
                print('No saved accounts found.\n'
                      'Enter login information.')
            else:
                # DISPLAY SAVED ACCOUNTS
                print("--- SAVED ACCOUNTS ---")
                for i, account in enumerate(accounts):
                    print(f'[{i + 1}] {account["username"]}')

                # SELECT ACCOUNT
                select_account = input("Enter account index: ")
                try:
                    select_account = int(select_account)
                    if (select_account > 0) and (select_account <= len(accounts)):
                        account = accounts[select_account - 1]
                        username = account['username']
                        password = account['password']
                except ValueError:
                    print("Invalid input.\n"
                          "Please enter account index.")
                    continue

                # TRY TO AUTHENTICATE
                try:
                    reddit = praw.Reddit(client_id='REPLACE',  # ENTER CLIENT ID
                                         client_secret='REPLACE',  # ENTER CLIENT SECRET
                                         username=username,  # base64.b64decode(username)
                                         password=password,  # base64.b64decode(password)
                                         user_agent='REPLACE')  # ENTER NAME OF APP

                    user = reddit.user.me()
                    if user is not None:
                        access = True
                        print(f'Logged in as {user}')

                        # CHECK IF LOGIN IS SAVED
                        login_saved = False
                        for account in accounts:
                            if account['username'] == username and account['password'] == password:
                                login_saved = True
                                break

                        # ASK TO SAVE LOGIN IF NOT SAVED
                        if not login_saved:
                            save_login_info = input("Save login info? [Y]es/[N]o\n")
                            if save_login_info.lower() == 'y':
                                save_login(username, password)

                    else:
                        print('Invalid login.\n'
                              'Restarting...')
                except prawcore.exceptions.OAuthException:
                    access = False
                    print('Error occurred while trying to login.\n'
                          'Have you created a Reddit developer app?')
        else:
            print("Invalid choice. Try again.")
            continue

    # return reddit object
    return reddit


def view_all(subreddit):
    num_view = int(input("# of posts to view: "))

    try:
        # get posts from subreddit provided
        all_posts = subreddit.hot(limit=num_view)
    except prawcore.exceptions.NotFound:
        print(f'Subreddit r/{subreddit} not found.')
    except ValueError:
        print("Invalid input.")

    posts = {}  # DICTIONARY FOR POST INFORMATION

    for i, post in enumerate(all_posts):
        posts[i+1] = {"index": i+1,
                      "title": post.title,
                      "id": post.id,
                      "desc": post.selftext,
                      "url": post.url}

    #   PRINT POST INDEX, TITLE, ID
        print(f'[{i+1}] {post.title} [ID: {post.id}]')

    print("Enter post index to view that post.")
    index_view = int(input("Index: "))

    selected_post = posts[index_view]
    view_post(selected_post)

    repost = input("Repost post? [Y]es/[N]o\n")
    if repost.lower() == 'y':
        if selected_post['url'].endswith(('jpg', 'jpeg', 'png', 'gif')):
            # DOWNLOAD IMAGE
            response = requests.get(selected_post['url'])
            mime_type = response.headers['content-type']

            # GET FILE EXTENSION
            file_extension = mimetypes.guess_extension(mime_type)
            image_data = response.content

            # GET PATH TO DOWNLOADED IMAGE
            file_path = 'image' + file_extension

            # WRITE IMAGE DATA TO IMAGE FILE FOR REPOST
            with open(file_path, 'wb') as image_file:
                image_file.write(image_data)

            # REPOST IMAGE
            repost_image(reddit, file_path)
        elif selected_post['desc']:
            # REPOST POST
            repost_post(selected_post, reddit)
            # PRINT CONTENTS OF REPOST
            print(selected_post['desc'])
        else:
            # REPOST URL POST
            repost_post(selected_post, reddit)
            # PRINT CONTENTS OF REPOST
            print(selected_post['url'])

    view_another_post = input("View another post? [Y]es/[N]o\n")
    if view_another_post.lower() == 'y':
        view_all(subreddit)


def repost_post(selected_post, r):
    # GET SUBREDDIT TO REPOST TO
    subreddit_name = ''  # input("Enter subreddit to repost to: ")  # ENTER A SUBREDDIT
    subreddit = r.subreddit(subreddit_name)

    # CREATE A MARKDOWN FILE
    filename = selected_post['id'] + ".md"
    with open(filename, "w") as f:
        # WRITE POST TO MD FILE
        f.write(selected_post['title'] + "\n\n")
        f.write(selected_post['desc'] + "\n\n")
        f.write(selected_post['url'] + "\n\n")

    # GET NEW TITLE FOR REPOST
    new_title = input("Enter title for repost: ")

    # REPOST POST
    if selected_post['desc']:
        try:
            submission = subreddit.submit(new_title, selftext=selected_post['desc'])

            if submission is not None:
                print(f'Successfully reposted to r/{subreddit_name} with ID [{submission.id}]')
            else:
                print("Error occurred while trying to repost.")
        except praw.exceptions.RedditAPIException:
            print("Insufficient permissions.")
    elif selected_post['url']:
        try:
            submission = subreddit.submit(new_title, url=selected_post['url'])

            if submission is not None:
                print(f'Successfully reposted to r/{subreddit_name} with ID [{submission.id}]')
            else:
                print("Error occurred while trying to repost.")
        except praw.exceptions.RedditAPIException:
            print("Insufficient permissions.")
    else:
        submission = None


def repost_image(r, image_file_path=None):
    # GET SUBREDDIT TO REPOST TO
    subreddit_name = ''  # input("Enter subreddit to repost to: ")  # ENTER A SUBREDDIT
    subreddit = r.subreddit(subreddit_name)

    # GET NEW TITLE FOR REPOST
    new_title = input("Enter title for repost: ")

    try:
        # REPOST IMAGE
        submission = subreddit.submit_image(new_title, image_file_path)

        if submission is not None:
            print(f'Successfully reposted to r/{subreddit_name} with ID [{submission.id}]')
        else:
            print("Error occurred while trying to repost.")
    except praw.exceptions.RedditAPIException:
        print("Insufficient permissions.")


def get_current_date():
    # get current date
    today = date.today()

    # get abbreviation of month
    month = today.strftime("%b").upper()

    day = today.strftime("%d")
    year = today.strftime("%Y")

    return month, day, year
