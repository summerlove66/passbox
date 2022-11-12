
import json
from ast import arg
import base64,os,sys,subprocess
from art import *
from aes_util import AESCrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

SETTING_FILE = "settings.json"
PASS_REPO_PATH ="pass_repo"
RSA_PAIR_PATH = "key_pair"
PRIVATE_KEY = 'rsa_private_key.pem'
PUBLIC_KEY = 'rsa_public_key.pem'
RSA_PRIVATE_KEY_FILE = os.path.join(RSA_PAIR_PATH,PRIVATE_KEY)
RSA_PUBLIC_KEY_FILE = os.path.join(RSA_PAIR_PATH,PUBLIC_KEY)
RSA_BEGIN_SYMBOL ="-----BEGIN RSA PRIVATE KEY-----\n"
RSA_END_SYMBOL = "\n-----END RSA PRIVATE KEY-----"


with open(SETTING_FILE) as f:
    SETTING_ITEM  = json.load(f)

#initlize rsa key pair
def initlizer():
    key = RSA.generate(2048)
    f = open(RSA_PRIVATE_KEY_FILE, "wb")
    f.write(key.exportKey('PEM'))
    f.close()

    pubkey = key.publickey()
    f = open(RSA_PUBLIC_KEY_FILE, "wb")
    f.write(pubkey.exportKey('OpenSSH'))
    f.close()

    os.mkdir(RSA_PAIR_PATH)
    os.mkdir(PASS_REPO_PATH)

def get_file(key_file):
    with open(key_file) as f:
        return f.read()

def get_private_key_content():
    return get_file(RSA_PRIVATE_KEY_FILE).replace(RSA_BEGIN_SYMBOL,"").replace(RSA_END_SYMBOL,"")        
   
def generate_private_key(aes_encrypted_content):
    with open(RSA_PRIVATE_KEY_FILE, "w") as f:
        f.write(RSA_BEGIN_SYMBOL+ aes_encrypted_content + RSA_END_SYMBOL)

def pushes(fold_path,comment_info ,repo_name, branch_name):
    os.chdir(fold_path)
    subprocess.run("git add  .")
    #git.stdin.write("programming\n")
    subprocess.run("git commit -m " + comment_info )
    git = subprocess.Popen("git push -f  {}  {}".format(repo_name,branch_name),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                            universal_newlines=True,
                            bufsize=0,)
    # print("=====",git.stdout.read())
    # print("=====", git.stdin.read())
    # print("=====", git.stderr.read())
    out ,err = git.communicate()
    print("+=====",out,err,)
    os.chdir("..")

def pulls():
   
    subprocess.run("git clone -b {} {} {}".format(SETTING_ITEM["rsa"]["git"]["branch"], SETTING_ITEM["rsa"]["git"]["remote"],RSA_PAIR_PATH))
    
    #subprocess.run("git clone -b {} {} {}".format(SETTING_ITEM["pass"]["git"]["branch"] ,SETTING_ITEM["pass"]["git"]["remote"],PASS_REPO_PATH))
# get the original private key 
def get_rsa_private_key_from_aes_key(aes_key):
    if aes_key != "-":
        aesCryptor = AESCrypt(aes_key)
        cipher_text = get_private_key_content()
        return RSA_BEGIN_SYMBOL  + aesCryptor.aes_decrypt(cipher_text) + RSA_END_SYMBOL
    return get_file(RSA_PRIVATE_KEY_FILE)

# reset aes key  for private key  
def reset_rsa_private_aes_key(old_key,new_key):
    private_key_text =  get_private_key_content()
    if old_key != "-":       
        private_key_text= AESCrypt(old_key).aes_decrypt(private_key_text)
    if new_key != "-":
            private_key_text = AESCrypt(new_key).aes_encrypt(private_key_text)
    else:
         if "y" != input("will expose your private key ,are u sure(y|n)\n"):
            exit
    generate_private_key(private_key_text)
    pushes("key_pair","rsa","rsa",SETTING_ITEM["rsa"]["git"]["branch"])
 
    print("reset sucessful! ")

def encrypt_data(msg):
    public_key = RSA.import_key(get_file(RSA_PUBLIC_KEY_FILE ))
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_msg ,aes_key):
    private_key = RSA.import_key(get_rsa_private_key_from_aes_key(aes_key=aes_key))
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def encrypt_pass(domain,msg):
    cipher_text =encrypt_data(msg)
    os.chdir(PASS_REPO_PATH)
    with open(domain ,mode="w") as f:
        f.write(cipher_text)
    pushes(".", domain, "pass", SETTING_ITEM["pass"]["git"]["branch"])   

def decrypt_pass(domain,aes_key):
    domains = os.listdir(PASS_REPO_PATH)
    target_domains =[ e for e in domains if domain  in e]
    domain_count = len(target_domains)
    if domain_count ==0:
        print("domain not found!")
        return
    elif len(target_domains)>1:
       target_domain = input( "\n".join(target_domains)+"\nchoose one form above :")
    else:
        target_domain =target_domains[0]
    print("domain : ", target_domain)    
    with open(os.path.join(PASS_REPO_PATH,target_domain)) as f:
        text = f.read()
        print(decrypt_data(text,aes_key))



if __name__ == '__main__':
    print(text2art("PassBox"))
    funcs= {"dec" :decrypt_pass ,"enc":encrypt_pass,"reset" :reset_rsa_private_aes_key ,"pull" :pulls,"init" :initlizer}
    funcs[sys.argv[1]](*sys.argv[2:])
 
