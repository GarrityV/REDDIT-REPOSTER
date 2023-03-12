import menus
import functions
import prawcore.exceptions

# THINGS TO DO
# [X] ADD ABILITY TO SAVE MORE THAN 1 ACCOUNT
# [X] FIX ISSUE IF USER HAS INSUFFICIENT POSTING PERMISSION
# [X] REMEMBER & STORE LOGIN WITH JSON FILE
# [X] REMOVE SAVED ACCOUNTS
# [X] FIX BUG LOADING JSON WHEN DOESNT EXIST
# [X] IF NO LOGINS IN JSON FILE, PROMPT FOR LOGIN
# [] IMPLEMENT GO BACK OPTION
# [X] VIEW SUBREDDIT POSTS
# [X] SPECIFY POST TO VIEW DESC
# [X] MENU
# [X] SAVE POSTS (IMG & MD)
# [X] FIX REPOST BEFORE ASKING BUG
# [X] REPOST POSTS WITH TEXT
# [X] REPOST POSTS WITH URL
# [X] REPOST POSTS WITH IMAGES
# [] REPOST WITH UPDATED DATES (PERSONAL)
# [] FIX HTTP 400 ERROR WITH BAD REDIRECTS

# START APPLICATION WITH REDDIT AUTH
reddit = functions.reddit_auth()

# GET SUBREDDIT
u_sub = input("Enter subreddit: ")
try:
    subreddit = reddit.subreddit(u_sub)
except prawcore.exceptions.NotFound:
    print("Error: subreddit not found.\n"
          "Please enter a valid subreddit.")

# # # # # MAIN PROGRAM STARTS HERE # # # # #
invalid = False
while not invalid:
    # DISPLAY MAIN MENU
    menus.main_menu()
    # GET USER INPUT
    user_input = input("Enter: ")

    # INPUT VALIDATION
    if user_input == '1':
        functions.view_all(subreddit)
        invalid = True
    elif user_input == '2':
        print()
    elif user_input == '3':
        print()
    elif user_input.lower() == 'q':
        break
    else:
        print("Invalid option.")
