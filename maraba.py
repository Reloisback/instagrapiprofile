from instagrapi import Client
import os
import random
import imaplib
import email
import re
from instagrapi.mixins.challenge import ChallengeChoice
import requests
import time
import json
import email
import os
import glob



# Hello, I need to write an explanation here
#This file was shared on 29.03.2024 by Reloisback. 
#I created this using instagrapi and made it completely by myself.
#It's open for improvement and yes there might be some bugs

#In the meantime, I sell 1600 instagram accounts suitable for the API system, all of the accounts I sell are private accounts, all of them were used without any problems in the infrastructure you see.
#You can contact me to buy
#Telegram: Reloisback


def set_working_directory():
    # Target directory's full path
    target_directory = os.path.join(os.getcwd(), "doc")

    # Check if directory exists
    if not os.path.exists(target_directory):
        # If not, create it
        os.makedirs(target_directory)

    # Change the working directory
    os.chdir(target_directory)

    # List of files to be created
    files_to_create = ["bio.txt", "change_log.txt", "error.txt", "name.txt", "newusername.txt", "user_credentials.txt", "newinfo.txt", "desc.txt", "how_to_use.txt"]

    # List of directories to be created
    dirs_to_create = ["photo", "video", "profilephoto"]

    # Create files if they do not exist
    for file in files_to_create:
        if not os.path.exists(file):
            open(file, 'w').close()

    # Create directories if they do not exist
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.makedirs(dir)

    # Create setting.txt with default settings if it does not exist
    if not os.path.exists("setting.txt"):
        settings = {
            "update_credentials_with_email": False,
            "share_random_videos": False,
            "change_profile_photo": False,
            "delete_all_posts": False,
            "set_account_private": False,
            "set_account_public": False,
            "share_random_photos": False,
            "delete_external_links": False,
            "change_external_url": False,
            "change_bio": False,
            "change_name": False,
            "change_username": False,
            "external_link": "https://biolink",
            "num_photos": 5,
            "num_videos": 1,
            "use_description": False
        }
        with open("setting.txt", 'w') as f:
            json.dump(settings, f, indent=4)

    # Create how_to_use.txt with default instructions if it does not exist
    if not os.path.exists("how_to_use.txt"):
        instructions = """
        This is a Python script that performs various actions on an Instagram account.

        To use this script, you need to:

        1. Install the required Python libraries with pip:
        pip install -r requirements.txt

        2. Run the script with Python:
        python maraba.py

        3. The script will prompt you for your Instagram username and password. Enter them when prompted.

        4. The script will read the settings from the setting.txt file in the doc directory and perform the actions specified in the settings.

        Here's what each setting does:

        - "update_credentials_with_email": If true, the script will update the account credentials with the email.
        - "share_random_videos": If true, the script will share random videos.
        - "change_profile_photo": If true, the script will change the profile photo.
        - "delete_all_posts": If true, the script will delete all posts.
        - "set_account_private": If true, the script will set the account to private.
        - "set_account_public": If true, the script will set the account to public.
        - "share_random_photos": If true, the script will share random photos.
        - "delete_external_links": If true, the script will delete external links.
        - "change_external_url": If true, the script will change the external URL.
        - "change_bio": If true, the script will change the bio.
        - "change_name": If true, the script will change the name.
        - "change_username": If true, the script will change the username.
        - "external_link": The new external link to set if "change_external_url" is true.
        - "num_photos": The number of photos to share if "share_random_photos" is true.
        - "num_videos": The number of videos to share if "share_random_videos" is true.
        - "use_description": If true, the script will use the description.

        You can modify the setting.txt file to change the settings.
        """
        with open("how_to_use.txt", 'w') as f:
            f.write(instructions)

    print(f"Working directory set to: {target_directory}")





allmail_file_path = "allmail.txt"

def update_credentials_with_email(cl, credentials, allmail_file_path):
    updated_credentials = []
    with open(allmail_file_path, 'r') as allmail_file:
        allmails = {line.strip().split(' ', 1)[0]: line.strip().split(' ', 1)[1] for line in allmail_file.readlines() if ' ' in line}
    for username, password, email, email_password in credentials:
        if email in allmails:
            email_password = allmails[email]
        updated_credentials.append((username, password, email, email_password))
    return updated_credentials


def change_password_handler(username):
    chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
    password = "".join(random.sample(chars, 10))
    return password

def change_profile_photo(cl):
    photo_folder = "profilephoto"
    photo_list = os.listdir(photo_folder)
    selected_photo = random.choice(photo_list)
    cl.account_change_picture(photo_folder + '/' + selected_photo)
    print(f"Profile photo changed successfully: {selected_photo}")
    save_change_log(cl.username, "Profile photo changed")  # Log kaydını burada oluşturuyoruz

def delete_all_posts(cl):
    user_id = cl.user_id
    media_list = cl.user_medias(user_id)
    for idx, media in enumerate(media_list, start=1):
        try:
            print(f"{idx}. post is being deleted...")
            cl.media_delete(media.id)
            print(f"{idx}. post has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting post {idx}: {e}")
    print("All posts have been deleted successfully.")
    save_change_log(cl.username, "All posts deleted")  # Log kaydını burada oluşturuyoruz


def delete_fifth_post(cl):
    user_id = cl.user_id
    media_list = cl.user_medias(user_id)

    if len(media_list) >= 5:  # Check if there are at least 5 posts
        fifth_post = media_list[4]  # Get the 5th post (indexing starts from 0)
        try:
            print("5th post is being deleted...")
            cl.media_delete(fifth_post.id)
            print("5th post has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting 5th post: {e}")
    else:
        print("There are less than 5 posts. No posts were deleted.")

    save_change_log(cl.username, "5th post deleted")

def delete_old_posts(cl, max_posts=4):
    user_id = cl.user_id
    media_list = cl.user_medias(user_id)

    if len(media_list) > max_posts:
        # Reverse the list and then slice it
        reversed_list = list(reversed(media_list))
        # If there are more than max_posts, delete the older ones
        for idx, media in enumerate(reversed_list[max_posts:], start=1):
            try:
                print(f"{idx}. post is being deleted...")
                cl.media_delete(media.id)
                print(f"{idx}. post has been deleted successfully.")
            except Exception as e:
                print(f"Error deleting post {idx}: {e}")

        print("All posts have been deleted successfully.")
        save_change_log(cl.username, "All posts deleted")

def delete_all_reels(cl):
    user_id = cl.user_id
    media_list = cl.user_medias(user_id)
    reel_list = [media for media in media_list if media.media_type == 2]  # filter out the reels
    for idx, reel in enumerate(reel_list, start=1):
        try:
            print(f"{idx}. reel is being deleted...")
            cl.delete_media(reel.id)
            print(f"{idx}. reel has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting reel {idx}: {e}")
    print("All reels have been deleted successfully.")
    save_change_log(cl.username, "All reels deleted")  # Log the change here

def share_random_photos(cl):
    # Load the settings from the settings.txt file
    with open('setting.txt', 'r') as f:
        settings = json.load(f)
    
    num_photos = settings.get('num_photos', 3)
    use_description = settings.get('use_description', False)

    descriptions = {}
    if use_description:
        with open('desc.txt', 'r', encoding='utf-8') as f:
            desc_lines = f.readlines()
        current_key = None
        for line in desc_lines:
            line = line.strip()
            if line.endswith('Decs'):
                # Extract the number from the ordinal string
                current_key = int(''.join(filter(str.isdigit, line.split(' ')[0])))
                descriptions[current_key] = ''
            elif line.endswith('Decs End'):
                current_key = None
            elif current_key is not None:
                descriptions[current_key] += line + '\n'

    photo_folder = "photo"
    photo_list = os.listdir(photo_folder)

    # Load the shared photos from the shared_photos.txt file
    shared_photos = {}
    try:
        with open('shared_photos.txt', 'r') as f:
            for line in f:
                username, *photos = line.strip().split(':')
                shared_photos[username] = photos
    except FileNotFoundError:
        pass

    # Get the shared photos for the current user
    user_shared_photos = shared_photos.get(cl.username, [])

    # Exclude the shared photos from the selection
    photo_list = [photo for photo in photo_list if photo not in user_shared_photos]

    if photo_list:
        selected_photos = random.sample(photo_list, min(num_photos, len(photo_list)))
    else:
        print("No photos available to share.")
        return
    for idx, photo in enumerate(selected_photos, start=1):
        photo_path = photo_folder + '/' + photo
        print(f"{idx}. photo shared...")
        # Get the photo number from the photo name
        photo_number = int(os.path.splitext(photo)[0])
        # Get the corresponding description
        caption = descriptions.get(photo_number, "") if use_description else ""
        cl.photo_upload(photo_path, caption=caption.strip())
        # Add the shared photo to the user_shared_photos list
        user_shared_photos.append(photo)

    # Update the shared_photos dictionary
    shared_photos[cl.username] = user_shared_photos

    # Save the updated shared_photos dictionary to the shared_photos.txt file
    with open('shared_photos.txt', 'w') as f:
        for username, photos in shared_photos.items():
            f.write(f"{username}:{':'.join(photos)}\n")

    print(f"{len(selected_photos)} random photos were shared successfully.")
    save_change_log(cl.username, f"{len(selected_photos)} new posts shared") # Log kaydını burada oluşturuyoruz



def share_random_videos(cl):
    # Load the settings from the settings.txt file
    with open('setting.txt', 'r') as f:
        settings = json.load(f)
    
    # Get the number of videos to be shared from the settings
    num_videos = settings.get('num_videos', 1)

    video_folder = "video"
    video_list = [file for file in os.listdir(video_folder) if file.endswith('.mp4')]
    selected_videos = random.sample(video_list, num_videos)
    for idx, video in enumerate(selected_videos, start=1):
        video_path = video_folder + '/' + video
        print(f"{idx}. video shared...")
        cl.video_upload(video_path, caption="")
    print(f"{num_videos} random videos were shared successfully.")
    save_change_log(cl.username, f"{num_videos} new videos shared")

def save_change_log(username, action):
    with open('change_log.txt', 'a') as log_file:
        log_file.write(f"{action}: {username}\n")



def share_random_reels(self):
    # Load the settings from the settings.txt file
    with open('setting.txt', 'r') as f:
        settings = json.load(f)

    # Get the number of reels to be shared from the settings
    num_reels = settings.get('num_reels', 1)
    use_reel_desc = settings.get('reel_desc', False)

    caption = ""
    if use_reel_desc:
        # Load the descriptions from the reeldesc.txt file
        with open('reeldesc.txt', 'r', encoding='utf-8') as f:
            caption = "\n".join(line.strip() for line in f.readlines())

    reel_folder = "reel"
    reel_list = [file for file in os.listdir(reel_folder) if file.endswith('.mp4')]

    # Load previously shared reels
    with open('shared_reel.txt', 'r') as f:
        shared_reels = f.read().splitlines()

    # Filter out the reels that have already been shared
    reel_list = [reel for reel in reel_list if reel not in shared_reels]

    selected_reels = random.sample(reel_list, min(num_reels, len(reel_list)))
    for idx, reel in enumerate(selected_reels, start=1):
        reel_path = reel_folder + '/' + reel
        print(f"{idx}. reel shared...")
        self.clip_upload(reel_path, caption=caption)

        # Save the shared reel to the shared_reel.txt file
        with open('shared_reel.txt', 'a') as f:
            f.write(f"{self.username}: {reel}\n")

    print(f"{len(selected_reels)} random reels were shared successfully.")
    save_change_log(self.username, f"{len(selected_reels)} new reels shared")

def save_change_log(username, action):
    with open('change_log.txt', 'a') as log_file:
        log_file.write(f"{action}: {username}\n")

def delete_external_links(api):
    result = api.private_request("accounts/current_user/?edit=true")
    time.sleep(5)

    for link in result.get('user', {}).get('bio_links', []):
        print("DELETING BIO LINK")

        signed_body = f"signed_body=SIGNATURE.%7B%22_uid%22%3A%22{api.user_id}%22%2C%22_uuid%22%3A%22{api.uuid}%22%2C%22link_ids%22%3A%22%5B%5C%22{link.get('link_id', '')}%5C%22%5D%22%7D"

        response = api.private_request("accounts/remove_bio_links/", data=signed_body, with_signature=False)
        time.sleep(4)
        save_bio_link_change(api.username, "BioLink Cleared")  # Log kaydını burada oluşturuyoruz



def change_external_url(cl, external_url):
    cl.set_external_url(external_url=external_url)
    print(f"Bio link has been successfully changed: {external_url}")
    save_bio_link_change(cl.username, "BioLink Changed")  # Log kaydını burada oluşturuyoruz

def save_bio_link_change(username, action):
    with open('change_log.txt', 'a') as log_file:
        log_file.write(f"{action}: {username}\n")


def change_bio(client):
    try:
        bio_files = glob.glob('bio*.txt')  # All bio files
        if not bio_files:
            print("No bio files found. Biography could not be changed.")
            return

        bio_file = random.choice(bio_files)  # Select a random bio file
        with open(bio_file, 'r', encoding='utf-8') as f:
            new_bio = f.read().strip()
            client.account_edit(biography=new_bio)
            print(f"Biography successfully changed: {new_bio}")
            save_bio_change(client.username, success=True)  # Log kaydını burada oluşturuyoruz
    except FileNotFoundError:
        print(f"The {bio_file} file was not found. Biography could not be changed.")

def save_bio_change(username, success=False):
    with open('change_log.txt', 'a') as log_file:
        status = "Success" if success else "Failure"
        log_file.write(f"{status}: Bio Changed: {username}\n")


def change_name(cl):
    try:
        with open('name.txt', 'r', encoding='utf-8') as name_file:
            names = name_file.readlines()
            random.shuffle(names)
            for new_name in names:
                new_name = new_name.strip()
                try:
                    cl.account_edit(full_name=new_name)
                    time.sleep(1)
                    success = True
                    print(f"Name changed successfully: {new_name}")
                except Exception as name_error:
                    success = False
                    print(f"Name change error: {name_error}. A different name will be tried.")
                if success:
                    break
    except FileNotFoundError:
        print("The file name.txt was not found. The name could not be changed.")

        
def change_username(cl, username, password, email, email_password):
    try:
        with open('newusername.txt', 'r') as username_file:
            usernames = username_file.readlines()
        random.shuffle(usernames)
        for new_username in usernames:
            new_username = new_username.strip()
            try:
                cl.account_edit(username=new_username)
                success = True
                print(f"Username changed successfully: {new_username}")
            except Exception as username_error:
                    if "challenge_required" in str(username_error):
                        success = False
                        print(f"Challenge required for username: {new_username}. Trying the next username.")
                    else:
                        success = False
                        print(f"Username change error for {new_username}: {username_error}. Trying the next username.")
    except FileNotFoundError:
        print("The file newusername.txt was not found. The username could not be changed.")


    def change_password(self, old_password: str, new_password: str, new_username: str = None) -> bool:
        # Load settings from setting.txt
        with open('setting.txt', 'r') as f:
            settings = json.load(f)

        # Check if the change_password setting is true
        if settings['change_password']:
            try:
                enc_old_password = self.password_encrypt(old_password)
                enc_new_password = self.password_encrypt(new_password)
                data = {
                    "enc_old_password": enc_old_password,
                    "enc_new_password1": enc_new_password,
                    "enc_new_password2": enc_new_password,
                }
                self.with_action_data(
                    {
                        "_uid": self.user_id,
                        "_uuid": self.uuid,
                        "_csrftoken": self.token,
                    }
                )
                result = self.private_request("accounts/change_password/", data=data)
                if result:
                    print("Password changed successfully.")
                    # Log the change
                    with open('changepass.txt', 'a') as log_file:
                        username = new_username if new_username else self.username
                        if self.email and self.email_password:
                            log_file.write(f"{username}:{new_password}:{self.email}:{self.email_password}\n")
                        else:
                            log_file.write(f"{username}:{new_password}\n")
                else:
                    print("Failed to change password.")
                return result
            except Exception as e:
                print(f"Error changing password: {e}")
                return False
        else:
            print("Password change is not enabled in the settings.")
            return False


    def account_set_private(self) -> bool:
        assert self.user_id, "Login required"
        user_id = str(self.user_id)
        data = self.with_action_data({"_uid": user_id, "_uuid": self.uuid})
        result = self.private_request("accounts/set_private/", data)
        if result["status"] == "ok":
            print(f"Account set to private")
        return result["status"] == "ok"

def change_email(cl, username, password):
    with open('setting.txt', 'r') as file:
        settings = json.load(file)

    change_password = settings.get("change_password", False)
    new_password = settings.get("new_password", "") if change_password else password

    with open('newmail.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        new_email, new_email_password = line.strip().split(':')
        try:
            cl.send_confirm_email(new_email)
            print(f"Email changed successfully: {new_email}")
            with open('changelog.txt', 'a') as log_file:
                log_file.write(f"{username}:{new_password}:{new_email}:{new_email_password}\n")
        except Exception as email_error:
            print(f"Email change error: {email_error}.")

def save_change(username, password, email, email_password, new_username, success=False):
    if success:
        with open('change_log.txt', 'a') as log_file:
            status = "Success"
            log_file.write(f"{username}  -  {new_username}:{password}:{email}:{email_password}- {status}\n\n")
        with open('newinfo.txt', 'a') as newinfo_file:
            newinfo_file.write(f"{new_username}:{password}:{email}:{email_password}\n")


def delete_phone(client: Client):
        # Get the current account information
    account_info = client.account_info()

        # Check if a phone number is set
    if 'phone_number' in account_info and account_info['phone_number']:
        print(f"Current phone number: {account_info['phone_number']}")

            # Set the phone_number field to an empty string to remove the phone number
        client.account_edit(phone_number="")

            # Get the updated account information
        updated_account_info = client.account_info()

            # Check if the phone number was successfully removed
        if 'phone_number' in updated_account_info and not updated_account_info['phone_number']:
            print("Phone number was successfully removed.")
        else:
            print("Failed to remove phone number.")
    else:
        print("No phone number is set.")

def read_settings(file_path):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        print("Settings file not found.")
        return None

def perform_actions_based_on_settings(cl, settings, username, password, email, email_password):
    if settings:
        if settings.get("change_profile_photo", False):
            change_profile_photo(cl)
        if settings.get("followers_count", False):
            get_followers_count(cl)
        if settings.get("delete_old_posts", False):
            delete_old_posts(cl)
        if settings.get("delete_fifth_post", False):
            delete_fifth_post(cl)
        if settings.get("delete_all_posts", False):
            delete_all_posts(cl)
        if settings.get("delete_all_reels", False):
            delete_all_reels(cl)
        if settings.get("delete_phone", False):
            delete_phone(cl)
        if settings.get("set_account_private", False):
            cl.account_set_private()
        if settings.get("set_account_public", False):
            cl.account_set_public()
        if settings.get("share_random_reels", False):    
            share_random_reels(cl)    
        if settings.get("share_random_photos", False):
            share_random_photos(cl)
        if settings.get("delete_external_links", False):
            delete_external_links(cl)
        if settings.get("share_random_videos", False):
            share_random_videos(cl)
        if settings.get("change_external_url", False):
            external_url = settings.get("external_link", "")
            change_external_url(cl, external_url)
        if settings.get("change_bio", False):
            change_bio(cl)
        if settings.get("change_name", False):
            change_name(cl)
        if settings.get("change_email", False):
            change_email(cl, username, password)
        if settings.get("change_password", False):
            new_password = settings.get("new_password", "")
            old_password = password
            success = cl.change_password(old_password, new_password)
            if success:
                print("Password changed successfully.")
                # Log the change
                with open('changepass.txt', 'a') as log_file:
                    if email and email_password:
                        log_file.write(f"{username}:{new_password}:{email}:{email_password}\n")
                    else:
                        log_file.write(f"{username}:{new_password}\n")
            else:
                print("Failed to change password.")
        if settings.get("change_username", False):
            change_username(cl, username, password, email, email_password)
    else:
        print("An error occurred while loading the settings.")



def read_credentials(file_path):
    credentials = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(':')
            username = parts[0] if len(parts) > 0 else None
            password = parts[1] if len(parts) > 1 else None
            email = parts[2] if len(parts) > 2 else None
            email_password = parts[3] if len(parts) > 3 else None
            CHALLENGE_EMAIL = parts[2] if len(parts) > 2 else None
            CHALLENGE_PASSWORD = parts[3] if len(parts) > 3 else None
            credentials.append((username, password, email, email_password, CHALLENGE_EMAIL, CHALLENGE_PASSWORD))
    return credentials
def main():
    credentials = read_credentials('user_credentials.txt')
    settings = read_settings('setting.txt')

    total_users = len(credentials)

    for idx, (username, password, email, email_password, CHALLENGE_EMAIL, CHALLENGE_PASSWORD) in enumerate(credentials, start=1):
        print(f"\n Hello, I sell 1600 instagram accounts, Telegram: Reloisback")
        print(f"\n These codes are shared completely free of charge")
        print(f"\nProcess {idx}/{total_users} - Logging in: {username}")
        print(f"\n {email} {email_password}")

        try:
            cl = Client(proxy="TYPE PROXY HERE")
            cl.challenge_code_handler = lambda api, choice: challenge_code_handler(username, CHALLENGE_EMAIL, CHALLENGE_PASSWORD, choice)
            cl.change_password_handler = change_password_handler 
            for _ in range(20):  # Retry up to 20 times
                try:
                    print(f"Signing In {username} ")
                    cl.login(username, password)
                    print(f"Successfully logged in {username}")
                    # Write the username and follower count to the text document
                    with open('change_log.txt', 'a') as f:
                        f.write(f'{username}:{password}:{CHALLENGE_EMAIL}:{CHALLENGE_PASSWORD}\n')

                    with open('followers.txt', 'a') as f:
                        followers = cl.user_followers(cl.user_id)
                        print(f"Number of followers: {len(followers.keys())}")
                        f.write(f"{username}: {len(followers.keys())}\n")

                    # Read the text document into a list of tuples
                    with open('followers.txt', 'r') as f:
                        lines = f.readlines()
                        data = [(line.split(':')[0], int(line.split(':')[1])) for line in lines]

                    # Sort the list of tuples based on the follower count
                    data.sort(key=lambda x: x[1], reverse=True)

                    # Write the sorted list back to the text document
                    with open('followers.txt', 'w') as f:
                        for username, follower_count in data:
                            f.write(f"{username}: {follower_count}\n")
                    break  # Break the loop after a successful login
                except Exception as e:  # Catch any exception
                    if f"We couldn't find an account with the username {username}. Check the username you entered and try again." not in str(e):
                        raise  # If the exception is not the expected one, raise it

            with open('fullinfo.txt', 'a') as f:
                f.write(f"{username}:{password}:{CHALLENGE_EMAIL}:{CHALLENGE_PASSWORD}\n")

            cl.challenge_code_handler = lambda _, choice: challenge_code_handler(username, CHALLENGE_EMAIL, CHALLENGE_PASSWORD, choice)

            perform_actions_based_on_settings(cl, settings, username, password, email, email_password)

            # Close the session
            cl.logout()
            print("The session has been closed successfully.")

        except Exception as e:
            print(f"Hata oluştu: {e}")
            with open("error.txt", "a") as error_file:
                error_file.write(f"{username}:{password}:{email}:{email_password}\n")
            continue
def get_imap_server(email):
    if "gmx.net" in email or "gmx.com" in email:
        return "imap.gmx.net"
    elif "hotmail.com" in email or "outlook.com" in email:
        return "imap-mail.outlook.com"
    elif "gmail.com" in email:
        return "imap.gmail.com"
    elif "mail.ru" in email:
        return "imap.mail.ru"
    elif "rambler.ru" in email:
        return "imap.rambler.ru"
    elif "gazeta.pl" in email:
        return "imap.gazeta.pl"
    else:
        return "imap.firstmail.ltd"
    


def get_code_from_email(username, CHALLENGE_EMAIL, CHALLENGE_PASSWORD):
    imap_server = get_imap_server(CHALLENGE_EMAIL)
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
    mail.select("inbox")
    print(f"Checking {CHALLENGE_EMAIL} {CHALLENGE_PASSWORD} for a 6-digit code...")

    # Tüm e-postaları al
    status, email_ids = mail.search(None, "ALL")
    assert status == "OK", "Error during get_code_from_email: %s" % status

    # En son gelen e-postanın ID'sini al
    if email_ids:
        latest_email_id = email_ids[0].split()[-1]
        status, email_data = mail.fetch(latest_email_id, "(RFC822)")
        assert status == "OK", "Error2 during get_code_from_email: %s" % status

        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # E-posta içeriğini al
        payload = msg.get_payload(decode=True)
        if payload is not None and isinstance(payload, bytes):
            body = payload.decode("utf-8")

            # 6 haneli kodu çıkart
            code_pattern = r"\b\d{6}\b"
            match = re.search(code_pattern, body)
            if match:
                code = match.group()
                if code and code not in ['999999', '262626', '363636']:
                    print(f"Found a 6-digit code: {code}")
                    return code

    return False

def get_code_from_sms(username):
    while True:
        code = input(f"Enter code (6 digits) for {username}: ").strip()
        if code and code.isdigit():
            return code
    return None

def challenge_code_handler(username, CHALLENGE_EMAIL, CHALLENGE_PASSWORD, choice):
    if choice == ChallengeChoice.SMS:
        return get_code_from_sms(username)
    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username, CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
    return False

if __name__ == "__main__":
    set_working_directory()
    main()