import json
import click
import base64
import os
import subprocess
from aes_util import AESCrypt
from Crypto.PublicKey import RSA
from binaryornot.check import is_binary
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


VERSION = "0.10"
LOGO =f"""
 ____                    ____
|  _ \   __ _  ___  ___ | __ )   ___  __  __
| |_) | / _` |/ __|/ __||  _ \  / _ \ \ \/ /
|  __/ | (_| |\__ \\__ \| |_) || (_) | >  <
|_|     \__,_||___/|___/|____/  \___/ /_/\_\\
    
    
version:{VERSION} author:summerlove66  since:2023.12 
"""

DEFAULT_SETTINGS ={
    "onlyLocal": True,
    "pass": {
        "git": {
            "remote": "git@github.com:user/xxxx.git",
            "branch": "master",
            "localBranch": "master"
        }
    },
    "rsa": {
        "git": {
            "remote": "git@github.com:user/xxxxxxx.git",
            "branch": "master",
            "localBranch": "master"
        }
    }
}
CONFIG_ABS_PATH = os.path.join(os.path.expanduser("~") ,".passbox")
SETTING_FILE = "settings.json"
PASS_REPO_PATH = "pass_repo"
RSA_PAIR_PATH = "key_pair"
PRIVATE_KEY = 'rsa_private_key.pem'
PUBLIC_KEY = 'rsa_public_key.pem'
RSA_PRIVATE_KEY_FILE = os.path.join(RSA_PAIR_PATH, PRIVATE_KEY)
RSA_PUBLIC_KEY_FILE = os.path.join(RSA_PAIR_PATH, PUBLIC_KEY)
RSA_BEGIN_SYMBOL = "-----BEGIN RSA PRIVATE KEY-----\n"
RSA_END_SYMBOL = "\n-----END RSA PRIVATE KEY-----"
FILE_MARK = "file-passbox-"
ENCRYPTED_FILE_MARK = "file-enc-passbox-"

os.makedirs(CONFIG_ABS_PATH,exist_ok=True)
os.chdir(CONFIG_ABS_PATH)

if not os.path.exists(SETTING_FILE):
    with open(SETTING_FILE,"w", encoding="utf8") as f:
        json.dump(DEFAULT_SETTINGS,f)
        
with open(SETTING_FILE) as f:
    SETTING_ITEM = json.load(f)


@click.group()
@click.version_option(message=LOGO)
def cli():
    pass

def get_file(key_file):
    with open(key_file) as f:
        return f.read()


def get_private_key_content():
    return get_file(RSA_PRIVATE_KEY_FILE).replace(RSA_BEGIN_SYMBOL, "").replace(RSA_END_SYMBOL, "")


def generate_private_key(aes_encrypted_content):
    with open(RSA_PRIVATE_KEY_FILE, "w") as f:
        f.write(RSA_BEGIN_SYMBOL + aes_encrypted_content + RSA_END_SYMBOL)


def pushes(fold_path, comment_info, local_branch_name, remote_branch_name):
    if not SETTING_ITEM["onlyLocal"]:
        os.chdir(fold_path)
        subprocess.run("git add  .")
        # git.stdin.write("programming\n")
        subprocess.run("git commit -m " + comment_info)
        git = subprocess.Popen("git push -f  origin {}:{}".format(local_branch_name, remote_branch_name),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0,)
        out, err = git.communicate()
        click.echo(f"+===== {out} {err}")
        os.chdir("..")

# get the original private key
def get_rsa_private_key_from_aes_key(aes_key):
    if aes_key != "-":
        aesCryptor = AESCrypt(aes_key)
        cipher_text = get_private_key_content()
        return RSA_BEGIN_SYMBOL + aesCryptor.aes_decrypt(cipher_text) + RSA_END_SYMBOL
    return get_file(RSA_PRIVATE_KEY_FILE)


def encrypt_text(msg):
    return encrypt_bytes(bytes(msg.encode("utf8")))


def encrypt_bytes(data):
    res = bytearray()
    public_key = RSA.import_key(get_file(RSA_PUBLIC_KEY_FILE))
    cipher = PKCS1_cipher.new(public_key)
    for i in range(0, len(data), 200):
        res += cipher.encrypt(data[i:i + 200])

    return base64.b64encode(res).decode('utf-8')


def decrypt_text(encrypt_msg, aes_key):

    return decrypt_bytes(encrypt_msg, aes_key).decode('utf-8')


def decrypt_bytes(data, aes_key):
    res = bytearray()
    private_key = RSA.import_key(
        get_rsa_private_key_from_aes_key(aes_key=aes_key))
    cipher = PKCS1_cipher.new(private_key)
    data = base64.b64decode(data)
    for i in range(0, len(data), 256):
        res += cipher.decrypt(data[i:i+256], 0)
    return res


def post_encrypted(domain, cipher_text, will_upload):
    os.chdir(PASS_REPO_PATH)
    with open(domain, mode="w") as f:
        f.write(cipher_text)
    if will_upload:
        pushes(".", domain, SETTING_ITEM["rsa"]["git"]
               ["localBranch"], SETTING_ITEM["rsa"]["git"]["branch"])
    click.echo("encrypt sucessful! ")

# initlize rsa key pair
@cli.command(name="init")
def initlizer():
    os.mkdir(RSA_PAIR_PATH)
    key = RSA.generate(2048)
    f = open(RSA_PRIVATE_KEY_FILE, "wb")
    f.write(key.exportKey('PEM'))
    f.close()

    pubkey = key.publickey()
    f = open(RSA_PUBLIC_KEY_FILE, "wb")
    f.write(pubkey.exportKey('OpenSSH'))
    f.close()

    os.mkdir(PASS_REPO_PATH)


@cli.command(name="pull")
def pulls():
    if os.path.exists(PASS_REPO_PATH) or os.path.exists(RSA_PAIR_PATH):
        print("Warning: {} or {} dirctory is exists, please remove(backup if u need) it  then try again!".format(
            PASS_REPO_PATH, RSA_PAIR_PATH))
        exit()
    subprocess.run("git clone -b {} {} {}".format(
        SETTING_ITEM["rsa"]["git"]["branch"], SETTING_ITEM["rsa"]["git"]["remote"], RSA_PAIR_PATH))
    subprocess.run("git clone -b {} {} {}".format(
        SETTING_ITEM["pass"]["git"]["branch"], SETTING_ITEM["pass"]["git"]["remote"], PASS_REPO_PATH))


# reset aes key  for private key
@cli.command(name="reset")
@click.argument("old_key")
@click.argument("new_key")
def reset_rsa_private_aes_key(old_key, new_key):
    private_key_text = get_private_key_content()
    if old_key != "-":
        private_key_text = AESCrypt(old_key).aes_decrypt(private_key_text)
    if new_key != "-":
        private_key_text = AESCrypt(new_key).aes_encrypt(private_key_text)
    else:
        if "y" != input("will expose your private key ,are u sure(y|n)\n"):
            exit
    generate_private_key(private_key_text)
    pushes("key_pair", "rsa", SETTING_ITEM["rsa"]["git"]
           ["localBranch"], SETTING_ITEM["rsa"]["git"]["branch"])
    click.echo("reset sucessful! ")


@cli.command(name="enc")
@click.argument("domain")
@click.argument("msg")
@click.option("--upload", default=True, type=bool, help="will upload?(true/false)")
def encrypt_text_handler(domain, msg, upload):
    post_encrypted(domain, encrypt_text(msg), upload)


@cli.command(name="encfile")
@click.argument("file_path")
@click.option("--upload", default=True, type=bool, help="will upload?(true/false)")
def encrypt_file_handler(file_path, upload):
    if is_binary(file_path):
        with open(file_path, "rb") as f:
            cipher_text = encrypt_bytes(f.read())
    else:

        with open(file_path, encoding="utf8") as f:
            cipher_text = encrypt_text(f.read())

    filename = FILE_MARK + os.path.basename(file_path)

    post_encrypted(filename, cipher_text, upload)


@cli.command(name="dec")
@click.argument("domain")
@click.argument("aes_key")
@click.option("--filename", default="", type=str, help="if it generate a file ,what's the filename?")
def decrypt_handler(domain, aes_key, filename):
    domains = os.listdir(PASS_REPO_PATH)
    target_domains = [e for e in domains if domain in e]
    domain_count = len(target_domains)
    if domain_count == 0:
        click.echo("domain not found!")
        return
    elif len(target_domains) > 1:
        target_domain = input("\n".join(target_domains) +
                              "\nchoose one form above :")
    else:
        target_domain = target_domains[0]
    click.echo("domain : " + target_domain)
    with open(os.path.join(PASS_REPO_PATH, target_domain)) as f:
        content = f.read()
        if target_domain.startswith("file-pass"):
            if filename == "":
                filename = target_domain.replace(FILE_MARK, "")
            with open(filename, "wb") as g:
                g.write(decrypt_bytes(content, aes_key))
            print("Congratulations, decrypted sucessful")
        else:
            print(decrypt_text(content, aes_key))


# if __name__ == '__main__':
#     print(text2art("PassBox"))
#     # print(sys.argv)
#     # funcs = {"dec": decrypt, "enc": encrypt_text, "encfile" :encrypt_file,
#     #          "reset": reset_rsa_private_aes_key, "pull": pulls, "init": initlizer}
#     # funcs[sys.argv[1]](*sys.argv[2:])
#     cli()
