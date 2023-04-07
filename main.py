import menus
import functions
import prawcore.exceptions

# START APPLICATION WITH REDDIT AUTH
reddit = functions.reddit_auth()

def get_subreddit():
    try:
        # GET SUBREDDIT
        u_sub = input("Enter subreddit to view: ")
        try:
            subreddit = reddit.subreddit(u_sub)
            print(f'\nSubreddit: {subreddit}')
            return subreddit
        except prawcore.exceptions.NotFound:
            print("Error: subreddit not found.\n"
                "Please enter a valid subreddit.")
            return None
    except ValueError:
        print("Invalid input.")

# # # # # MAIN PROGRAM STARTS HERE # # # # #
specified_subreddit = get_subreddit()

while True:
    # DISPLAY MAIN MENU
    menus.main_menu()
    # GET USER INPUT
    user_input = input("Enter: ")

    # INPUT VALIDATION
    if user_input == '1':  # VIEW POST BY INDEX
        if specified_subreddit:
            functions.view_all(specified_subreddit)
    elif user_input == '2':  # SAVE ALL POSTS IN SUBREDDIT
        if specified_subreddit:
            functions.save_all_posts(specified_subreddit)
    elif user_input.lower() == 'b':  # GO BACK
        specified_subreddit = get_subreddit()
    elif user_input.lower() == 'q':  # QUIT PROGRAM
        break
    else:
        print("Invalid option.")