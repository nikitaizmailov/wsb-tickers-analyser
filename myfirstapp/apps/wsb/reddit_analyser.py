from datetime import datetime, date, time
import re

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

# this one is imported in order to display the plot in html template
import matplotlib
matplotlib.use('Agg')

import io, base64


import json
import praw
#import requests

#import jupyter

from praw.models import MoreComments

# Reading JSON file with credentials to access Reddit API Wrapper
creds = 'myfirstapp/apps/wsb/client_secrets.json'

with open(creds) as f:
    data_creds = json.load(f)

# Creating an instance from Reddit class to interact with Reddit API

reddit = praw.Reddit(
    client_id=data_creds['client_id'],
    client_secret=data_creds['client_secret'],
    user_agent=data_creds['user_agent'],
    username=data_creds['username'],
    password=data_creds['password'],
    #redirect_uri=data_creds['redirect_uri'],
    #refresh_token=data_creds['refresh_token'],
    check_for_async=False
)

##  Function to extract comments from a submission and store it in the dictionary
def comments_to_submission_id_(sub_id):
    # Local Dictionary
    dict_subm = {}
    # Accessing the submission via reddit.submission method
    example_submission = reddit.submission(id=sub_id)
    # Sorting all comments in the submission by newest first
    example_submission.comment_sort = 'new'

    # Flattening the forrest comment to same level (No more top level and replies level comments)
    # Also Replacing More Comments objects with Comments objects themselves.
    example_submission.comments.replace_more(limit=None)

    all_comments = example_submission.comments.list()

    # Check uniqueness of each comment
    comment_done = set()

    # In the Praw docs it states that these MoreComments objects are a representation 
    # of the load more comments and continue this thread links encountered on Reddit.
    # To solve this issue so it loads all the comments and don't get stuck on MoreComments object
    for comment in all_comments:
        if isinstance(comment, MoreComments):
            # This should not be executed as we have converted all more comments to comments above
            continue
        if '**User Report**' in comment.body:
            continue
        if len(comment.body) > 2 and comment.id not in comment_done:
            if sub_id not in dict_subm:
                #print(comment.body)
                comment_done.add(comment.id)
                dict_subm[sub_id] = [comment.body]
            else:
                #print(comment.body)
                dict_subm[sub_id].append(comment.body)
    
    return dict_subm

# Get comments from subreddit regardless of the submission. I.e. anywhere on the subreddit. All the newest ones
# equivalent of https://www.reddit.com/r/VIAC/comments/

def last_comments(regex_pat, subred):
    # Storage for all comments from the whole subreddit where regex pattern match.
    regex_comments_storage = {}
    more_comments_obj = {}
    total_storage_of_all_comments = {}

    # Creating a regex pattern object from string
    pattern2 = regex_pat

    reg_exp2 = re.compile(pattern2)

    # Use subreddit.stream.comments() to get comments in real time.
    all_recent_comments = subred.comments(limit=1000)

    for num,comment in enumerate(all_recent_comments):
        if num == 1000:
            break
        if len(comment.body) > 4000:
            pass
        if isinstance(comment, MoreComments):
            # This should not be executed as we have converted all more comments to comments above
            print('MORE COMMENTS OBJECT!!!')
            more_comments_obj[comment.id] = comment.body
            break
        if '**User Report**' in comment.body:
            continue
        # Searching for regex pattern
        if reg_exp2.search(comment.body):
            if comment.id not in regex_comments_storage:
                print('\n {0}: {1}'.format(num,comment.body))
                regex_comments_storage[comment.id] = comment.body
            else:
                continue
        if comment.id in total_storage_of_all_comments:
            print('%d PASS. Comment already in the Dictionary' % (num))
        else:
            total_storage_of_all_comments[comment.id] = comment.body
        print('%d, %s' % (num, comment.body))
        
    return [regex_comments_storage, total_storage_of_all_comments]
        
        
## Widgets Final Build

# Functions
def subreddit_generator(val):
    subr1 = reddit.subreddit(val)
    return subr1

def submissions_generator(subreddit1):
    subms = subreddit1.hot(limit=25)
    sub_storage = []
    
    # Dictionary storage of submission_id and submission_title
    subm_id_dict = {}
    
    for sub in subms:
        sub_storage.append(sub.title)
        subm_id_dict[sub.title] = sub.id
        
    return sub_storage, subm_id_dict
        

def generate_subreddit(input_val):
    val = input_val
    try:
        subr11 = subreddit_generator(val)
        print("Successfully located subreddit: {}".format(subr11.title))
        subms = submissions_generator(subr11)[0]
        sub_titles_ids = submissions_generator(subr11)[1]
        return [subr11, subms, sub_titles_ids]
        #submission_title.options = subms
    except ValueError:
        print("Subreddit name cannot be empty! Please try again")
    except Exception as e:
        print("Please provide a real subreddit")

def _generate_comments(regex_pat, subr_object, subms, sub_titles_ids, submission_title_selected):
#     subm_label = submission_title
#     # display title of the selected submmission
#     subm_label = subm_label.label
    
#     subr_name = subreddit_input.value
#     subr_object = subreddit_generator(subr_name)
#     subms_id_storage = submissions_generator(subr_object)[1]
    
#     # get the subm id for the selected subm title
#     sub_id = subms_id_storage[subm_label]
    
    # submission_title_selected is the one that user selected in the form.
    sub_id = sub_titles_ids[submission_title_selected]
    
    # get the actual subreddit object itself.
    submission_object = reddit.submission(id=sub_id)
    
    # Get the submission object and from it you get a dictionary of comments.
    dictionary_comments_storage = comments_to_submission_id_(sub_id)
    
    # Creating a dataframe with comments to analyse further
    df_comments = pd.DataFrame(data=dictionary_comments_storage)
    df_comments.columns = ['Comments']
    df_comments = df_comments['Comments'].astype(str)
    # Converting a Series back to DataFrame
    df_comments = df_comments.to_frame()
    
    # Testing each comment with regex whether it contains the pattern searched
    df_test1 = df_comments.copy(deep=True)

    # The pattern is correct. The warning appearing at the bottom is misleading.
    #pattern2 = r'($)?[vV][iI][aA][cC](om|omCBS|CBS)?'
    #pattern3 = r'[Aa][Mm][Cc]'

    regex_pat = str(regex_pat)
    
    check_t_df = df_test1.loc[df_test1['Comments'].str.contains(pat=regex_pat, regex=True, case=False)].reset_index(drop=True)
    check_t_df = check_t_df['Comments'].to_list()

    return check_t_df, df_comments, dictionary_comments_storage, sub_id, submission_object, submission_title_selected
        
def plot_graph(regex_pattern, subr_object, subms, sub_titles_ids, submission_title_selected):
    
    # Pattern selected
    pattern3 = regex_pattern
    
    # get subreddit object itself. Not the submission itself
    subreddit = subr_object
    
    # get submission title
    title_submission = _generate_comments(pattern3, subr_object, subms, sub_titles_ids, submission_title_selected)[5]
    
    # Plotting a bar chart graph
    df_data = _generate_comments(pattern3, subr_object, subms, sub_titles_ids, submission_title_selected)[1]
    
    df_mentions_visual = df_data.copy(deep=True)

    # Filtering for the pattern needed
    df_mentions_visual = df_mentions_visual.loc[df_mentions_visual['Comments'].str.contains(pat=pattern3, 
                                                                                            regex=True, case=False)].reset_index(drop=True)
    # Column names for the newly grouped dataframe
    cols = pattern3.split('|')

    def splittingdata(cols):
        df_temp = df_mentions_visual.copy(deep=True)
        for col in cols:
            try:
                df_temp[col] = df_mentions_visual.loc[df_mentions_visual['Comments'].str.contains(pat=col, regex=True, case=False)].reset_index(drop=True)
            except Exception as exc:
                print(exc)
        return df_temp

    df_split = splittingdata(cols)

    # dropping a Comments column as it is no longer needed
    df_split = df_split.drop('Comments', axis=1)

    # Adding a row with total count of Non-NAN rows for each column
    df_split.loc['Total by column'] = df_split.count()

    # Sorting by the highest amount of mentions to lowest amount of mentions
    df_split = df_split.sort_values(df_split.last_valid_index(), axis=1, ascending=False)

    # 
    df_split = df_split.dropna(axis=0, how='all')
    
    
    # Visiualising the dataframe
    df_barchart_mentions = df_split.copy(deep=True)
    df_barchart_mentions = df_barchart_mentions.iloc[-1, 0:]
    # Dictionary with ticker as a key and mentions as a value
    df_barchart_mentions = df_barchart_mentions.to_dict()

    # creating the x and y values
    x1 = df_barchart_mentions.keys()
    y1 = df_barchart_mentions.values()


    
    comms = _generate_comments(pattern3, subr_object, subms, sub_titles_ids, submission_title_selected)[0]
    
    dict_subm = _generate_comments(pattern3, subr_object, subms, sub_titles_ids, submission_title_selected)[2]
    sub_id = _generate_comments(pattern3, subr_object, subms, sub_titles_ids, submission_title_selected)[3]
    
    comms_extracted = len(dict_subm[sub_id])

    # Plotting the graph.
    fig = plt.figure() # creating an empty figure with no Axes
    fig, ax = plt.subplots(figsize=(9,5), dpi=90) # creating a figure with one single Axes(chart)
    ax.bar(x1, y1, width=0.5)
    ax.set_title('Top Stock Mentions in Subreddit: {0}, Submission(Post): {1}'.format((subreddit.title).upper(), title_submission))
    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()


    # print('Extraction Comepleted!')
    # print('Total number of comments extracted: %d' % (len(dict_subm[sub_id])))
    # print("{} times {} was mentioned in the submission \n".format(len(comms), pattern3))
    # print("Below are the comments where the REGEX pattern was mentioned:")
    # for num,comm in enumerate(comms):
    #     print("{}) {}".format(num, comm))

    return b64, comms, comms_extracted, pattern3

# def last_1000_comments():
#     # getting the subreddit object
#     subr = subreddit_generator(subreddit_input.value)
    
#     # Storage for all comments from the whole subreddit where regex pattern match.
#     regex_comments_storage = {}
#     more_comments_obj = {}
#     total_storage_of_all_comments = {}

#     # Creating a regex pattern object from string
#     pattern2 = regex_pattern.value

#     reg_exp2 = re.compile(pattern2)

#     # Use subreddit.stream.comments() to get comments in real time.
#     all_recent_comments = subr.comments(limit=1000)

#     for num,comment in enumerate(all_recent_comments):
#         if num == 1000:
#             break
#         if len(comment.body) > 4000:
#             pass
#         if isinstance(comment, MoreComments):
#             # This should not be executed as we have converted all more comments to comments above
#             print('MORE COMMENTS OBJECT!!!')
#             more_comments_obj[comment.id] = comment.body
#             break
#         if '**User Report**' in comment.body:
#             continue
#         # Searching for regex pattern
#         if reg_exp2.search(comment.body):
#             if comment.id not in regex_comments_storage:
#                 regex_comments_storage[comment.id] = comment.body
#             else:
#                 continue
#         if comment.id in total_storage_of_all_comments:
#             pass
#         else:
#             total_storage_of_all_comments[comment.id] = comment.body
            
#         print("All the captured regex mentions in 1000 comments".center(100, '-'))
#         if not regex_comments_storage:
#             print("REGEX Pattern was not mentioned in these comments")
#         else:
#             for num, key in enumerate(regex_comments_storage):
#                 print("{}) {}".format(num, regex_comments_storage[key]))
        
#         # Added a separator between the two outputs
#         print("\n")
#         print('ALL COMMENTS OUTPUT BELOW'.center(100, '-'))
#         print("\n")
#         for num, key in enumerate(total_storage_of_all_comments):
#             print('%d, %s' % (num, total_storage_of_all_comments[key]))


# The input:
# subr_object, subms, sub_titles_ids = generate_subreddit('wallstreetbets')

# submission_title_selected = 'AMC Yolo 14k'
# regex_pattern = 'AMC'

# plot_graph(regex_pattern, subr_object, subms, sub_titles_ids, submission_title_selected)