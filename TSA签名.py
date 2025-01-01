import os,hashlib,requests,shutil,time
from datetime import datetime

def get_file_tsq(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    hash_bytes = sha256_hash.digest()

    tsq = [
        0x30, 0x39, 0x02, 0x01, 0x01, 0x30, 0x31, 0x30, 0x0D, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x65,
        0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x01, 0xFF 
    ]

    for i, byte in enumerate(hash_bytes):
        tsq[24 + i] = byte

    return bytes(tsq)

def enum_md_files(directory):
    md_files = []
    for f in os.listdir(directory):
        if(os.path.isfile(os.path.join(directory, f)) and f.endswith('.md')):
            md_files.append(f)
            
    return md_files

sign_directory = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
os.makedirs(sign_directory, exist_ok=True)
for md_file in enum_md_files("../source/_posts/"):
    print(md_file,end="   ")
    shutil.copy(os.path.join("../source/_posts/", md_file), sign_directory)

    response = requests.post("http://rfc3161timestamp.globalsign.com/advanced", headers={"Content-Type":"application/timestamp-query"}, data=get_file_tsq(os.path.join("../source/_posts/", md_file)), timeout=5)
    response.raise_for_status()

    if "The request could not be parsed." in response.content.decode('utf-8', errors='ignore'):
        print("TSA请求失败")
    else:
        with open(f"{sign_directory}/{md_file}.tsr", "wb") as f:
            f.write(response.content)
        print("成功")

    time.sleep(5)
