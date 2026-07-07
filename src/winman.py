# Author: @xchgll

import requests
import argparse
import zipfile
import json
import os
from fnmatch import fnmatch

CONFIG_DIR = ""
CONFIG_FILE = ""

WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"

if os.name == "nt":
    CONFIG_DIR = os.path.join(os.environ.get("USERPROFILE"),".winman")
else:
    CONFIG_DIR = os.path.join(os.environ.get("HOME"),".winman")

CONFIG_FILE = os.path.join(CONFIG_DIR,"config.json")
DOCN_DIR = os.path.join(CONFIG_DIR,"docn")

REPO_BASE = "https://raw.githubusercontent.com/xchgll/winman/refs/heads/master/"
REPO_CONFIG = REPO_BASE + "config.json"
REPO_DOCN = REPO_BASE + "winapi_docs_json.zip"

def update_docn():
    
    if not os.path.exists(DOCN_DIR):
        os.makedirs(DOCN_DIR,exist_ok=True)
    
    print("[#] Please Wait...")

    download = requests.get(REPO_DOCN)

    with open("download_temp.zip","wb") as f:
        f.write(download.content)
    
    print("[#] Extracting Data")

    with zipfile.ZipFile("download_temp.zip") as zf:
        for member in zf.infolist():
            print(member.filename) 
            if member.is_dir():
                continue
            filename = os.path.basename(member.filename)
            if not filename:
                continue
            target = os.path.join(DOCN_DIR, filename)
            with zf.open(member) as src, open(target, "wb") as dst:
                dst.write(src.read())
    
    config_resp = requests.get(REPO_CONFIG)

    with open(CONFIG_FILE,"w") as conf:
            conf.write(config_resp.text)

    os.remove("download_temp.zip")

    print("[+] Done")

def check_version():
    try:
        resp = requests.get(REPO_CONFIG)

        repo_version = resp.json()

        if resp.status_code in (400,403,404):
            print("[!] Error fetching repositry: ",resp.status_code)
            return
    except:
        print("[!] Cannot Check Version... Skipping")
    
    try:
        with open(CONFIG_FILE,"r") as f:
            current_version = json.load(f)

    # first time update
    except FileNotFoundError:
        print(BOLD + WHITE + "[?] Seems first time use winman\nDownload Documentation ? (y/n)" + RESET)
        value = input().lower()

        if value[0] == "n":
            return
        
        # to force update
        current_version = {"version": 0}


    # compare
    try:
        if repo_version["version"] > current_version["version"]:
            print(BOLD + WHITE + "[+] New Update: %s" % repo_version.get("note",""))

            print(
                ("Version: %d\nDownload Size: %s\nDisk Size: %s" + RESET) % (
                    repo_version["version"],
                    repo_version["zip_size"],
                    repo_version["disk_size"],
                )
            )


            print("Wanna Update ? (y/n)")

            value = input().lower()
            if value[0] == "n":
                return
            else:
                update_docn()
                return

        else:
            print("[+] Up to Date")
    except Exception as e:
        print("[!] Error while checking version " + str(e))


def dump_entry(entry):
    def h(title):
        print(f"{BOLD}{WHITE}{title}{RESET}")

    h(entry["name"])

    if entry.get("title"):
        print(f"  {entry['title']}")

    print()

    h("SYNOPSIS")

    if entry.get("header"):
        print(f"  Header : {entry['header']}")

    if entry.get("dll"):
        print(f"  DLL    : {entry['dll']}")

    if entry.get("lib"):
        print(f"  LIB    : {entry['lib']}")

    if entry.get("api_names"):
        print(f"  API    : {', '.join(entry['api_names'])}")

    print()

    if entry.get("description"):
        h("DESCRIPTION")
        print(f"  {entry['description']}")
        print()

    params = entry.get("parameters", [])
    if params:
        h("PARAMETERS")

        for p in params:
            print(f"  {BOLD}{p['name']}{RESET}")

            if p.get("direction"):
                print(f"      Direction : {p['direction']}")

            if p.get("description"):
                print(f"      {p['description']}")

            print()

    if entry.get("return_value"):
        h("RETURN VALUE")
        print(f"  {entry['return_value']}")
        print()

    if entry.get("remarks"):
        h("REMARKS")
        print(entry["remarks"])
        print()

    if entry.get("min_supported_client") or entry.get("min_supported_server"):
        h("REQUIREMENTS")

        if entry.get("min_supported_client"):
            print(f"  Client : {entry['min_supported_client']}")

        if entry.get("min_supported_server"):
            print(f"  Server : {entry['min_supported_server']}")

        print()

    if entry.get("unicode_ansi"):
        h("CHARACTER SET")
        print(f"  {entry['unicode_ansi']}")
        print()

    see_also = entry.get("see_also", [])

    if see_also:
        h("SEE ALSO")

        for item in see_also:
            print(f"  {BOLD + WHITE + item.get("text","") + RESET}\thttps://learn.microsoft.com/en-us{item.get("url","")}")

        print()

    if entry.get("source_file"):
        h("SOURCE")
        print(f"  {entry['source_file']}")
    
    h(f"\n{"="*20}\n")

def query_function(func: str):

    search_c = func.lower()[0]

    if search_c.isalpha():
        search_c = search_c
    else:
        search_c = "_misc"

    try:

        with open(os.path.join(DOCN_DIR,search_c+".json"),"r",encoding="utf-8") as df:
            data = json.load(df)
            for winfunc in data:
                if fnmatch(winfunc["name"],func):
                    dump_entry(winfunc)

    except FileNotFoundError:
        print("[#] Database not found... please try run winman -u to update")


def main():

    parser = argparse.ArgumentParser(
        prog="WinMan",
        description="Offline documentation browser for Windows and NT APIs"
    )

    parser.add_argument(
            "-q", "--query",
            required=False,
            help="API name or pattern to search for"
    )

    parser.add_argument(
            "-u", "--update",
            required=False,
            action="store_true",
            help="Update Check"
    )


    args = parser.parse_args()

    if args.update:
        check_version()

    query = args.query

    if not query:
        exit(0)


    query_function(query)

if __name__ == "__main__":
    main()