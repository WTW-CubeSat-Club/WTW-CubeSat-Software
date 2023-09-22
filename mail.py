import imaplib
import urllib.request
import env_vars

script_dir = env_vars.script_dir


def fetch(username, password):
    mailbox = imaplib.IMAP4_SSL('outlook.office365.com')
    mailbox.login(env_vars.mail_user, env_vars.mail_passwd)
    mailbox.select("INBOX")
    _, nums = mailbox.search(None, "UNSEEN")
    while str(nums) == "[b'']":
        _, nums = mailbox.search(None, "UNSEEN")

    print(nums)
    for num in nums[0].split():
        _, email_raw = mailbox.fetch(num, "(RFC822)")
        #remove most of email
        email_raw = str(email_raw)[-249:]
        print(email_raw)
        link = email_raw[71:-71]
        print(link) 
        print("\n"+str(len(email_raw)))
    
    return link

#downloads data in csv format
def download(link, norad_id):
    #path to cache will change depending on which folder you run the script in in vscode
    with urllib.request.urlopen(link) as csvfile, open(f'{script_dir}csv_cache/{norad_id}data.csv', 'w') as f:
        f.write(csvfile.read().decode())



