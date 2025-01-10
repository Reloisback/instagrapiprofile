If it works for you and you remember me if you become very rich one day, I'll leave a small address here for you to donate 
<a href="https://www.buymeacoffee.com/reloisback" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# Instagram Bulk Profile Editing Script

Hello! I'm sharing the Instagram bulk profile editing script that I created over months to meet my own needs. This tool utilizes the **Instagrapi** infrastructure and will not function without it.  

---

## ✨ **Requirements**

1. Install the latest version of [Instagrapi](https://github.com/subzeroid/instagrapi/tree/master).
2. Place `maraba.py` in the main folder.
3. Transfer the `doc` folder into the main folder.

---

## 🚀 **Getting Started**

1. In the `doc/user_credentials.txt`, add your Instagram account credentials in the format:  
   ```
   username:pass:mail:mailpass
   ```
2. Configure the proxy:  
   Edit line 640 in `maraba.py`:
   ```python
   cl = Client(proxy="TYPE PROXY HERE")
   ```
   Replace `"TYPE PROXY HERE"` with your proxy details.  

3. Ensure your Instagram-linked email addresses are IMAP-compliant. The script will automatically retrieve email confirmation codes if configured correctly.

---

## 🔧 **Features**

### Use the `doc/setting.txt` file to configure the following options:

- `Share_random_videos` - Share random videos from the `doc/video` folder. Specify the number of videos with `num_videos`.
- `Change_profile_photo` - Randomly change the profile photo using images from the `doc/profilephoto` folder. If there is only one image, all accounts will use the same profile photo.
- `delete_all_post` - Delete all shared posts.
- `set_account_private` - Make the account private.
- `set_account_public` - Make the account public.  
- `Share_random_reels` - Share random reels from the videos in the `doc/reel` folder. Use `num_reels` to specify the number of reels.
- `share_random_photos` - Share random posts from photos in the `doc/photo` folder. Use `num_photos` to specify the number of photos.
- `delete_external_link` - Remove the website link (External_link) from the current bio.
- `change_external_url` - Replace the current link with a new one. Specify the new link using `external_link`.
- `Change_bio` - Change the biography. Ensure `bio.txt` and `bio1.txt` exist in the `doc` folder. To use random biographies, create files named `bio1.txt`, `bio2.txt`, etc., each with different content. The script will randomly select one.
- `Change_name` - Change the account name. Add names to `name.txt`. Repeating names will increase their selection probability.
- `Change_username` - Change the username. Add usernames to `newusername.txt`, each on a new line. The script will randomly select one.
- `change_password` - Update the account password to the value specified in `new_password`.

### Experimental Settings
Other settings in `setting.txt` are experimental and may not work reliably. It is recommended to stick to the features listed above.

---

## 🚜 **Contact**

- **Telegram**: [@reloisback](https://t.me/reloisback)

---

## 📡 **Support**

<a href="https://www.buymeacoffee.com/reloisback" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
I'm happy if it worked for you, the codes I shared are completely free. 
If you want to support me you can use Buy me a Coffe.
Thanks a lot
