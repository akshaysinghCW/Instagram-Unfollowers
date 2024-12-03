# unfollowers
A Python application deployed using Flask to compare followers.html and following.html files, and figure out the list of people who have unfollowed you. 

How do I use this?

Step-1
Go to your profile, click the 3 lines at the top right corner of your screen. 
Tap on 'Your Activity' option. Hint - It has a clock as an icon.
Now scroll down and tap on the 'Download your information' button and request download.
It will authenticate you, confirm your email address and send you the data in about 4-6 hours.

Step-2
Go to your email, you would have received a new email from IG with subject as 'Your Instagram Information'.
Download the attached file, and extract it.
It will create a folder with this format 'yourusername_date'. 
Open it, open a subfolder named 'followers_and_following'.
You will find a file named followers.html and a file named following.html, these two are important for us. 

Step-3 
Go to https://akshaysinngh.com/unfollowers/ 
Upload followers.html, and then following.html and press the submit button.

## run local

1. create python venv
2. `pip install -r requirements`
3. python3 app.py