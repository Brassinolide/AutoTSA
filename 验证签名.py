import os,subprocess

def enum_md_files(directory):
    md_files = []
    for f in os.listdir(directory):
        if(os.path.isfile(os.path.join(directory, f)) and f.endswith('.md')):
            md_files.append(f)
            
    return md_files

sign_directory = "2025-01-01 18-12-09"

for md_file in enum_md_files(sign_directory):
    try:
        result = subprocess.run(f"openssl ts -verify -in \"{sign_directory}/{md_file}.tsr\" -data \"{sign_directory}/{md_file}\" -CAfile r6.pem", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"{md_file} 验证成功")
    except subprocess.CalledProcessError as e:
        print(f"{md_file} 验证失败")
