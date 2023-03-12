import menus
import functions
import prawcore.exceptions

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
