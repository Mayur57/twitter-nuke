![header-image](https://i.ibb.co/6Pdkwm1/twitter-nuke-01-min.png)

# Twitter Nuke
Quickly and efficiently delete your entire tweet history with the help of your Twitter archive without worrying about the puny and pointless 3200 tweet limit imposed by Twitter.

### About
The script uses multithreading to speed up the deletion process by simultaneously running multiple instances of the Twitter API. By utilising this modification the speed can be improved upto **~50-60 times** the single threaded performance (~1 tweet per sec).

### Features
- Set the number of likes and retweets as threshold above which the tweets will not be deleted.
- Set the batch size for threads
- Your deleted tweets and skipped tweets will be outputted in corresponding files.

### Usage
- Download your Twitter data by following [these steps](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive). 
- Edit the script with your Twitter API tokens and your preferences.
- Run it in your terminal using `python3 deleter-script.py`

(**Note:** Post September 2020, due to the high-profile Twitter attack of July 2020, the Twitter data might take anywhere from 24 hours to 4 days to be generated. Keep this in mind.)

### Caution
This script will delete **all** of your tweets and the action cannot be reversed. The script **DOES NOT** ask for your confirmation before executing the delete command. Run this script only if you are absolutely sure about it. The creator is not responsible for any loss in data and all the liabilities are held by the person running this script.

### Donate
Donate to the creator here -> [Buy Me a Coffee](https://buymeacoffee.com/mayurbhoi)

### Other Credits 
Photo by [Brett Jordan](https://unsplash.com/@brett_jordan?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/twitter?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
  
