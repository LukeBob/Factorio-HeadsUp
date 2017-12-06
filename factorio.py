#!/usr/bin/python3
import argparse
import requests
import tarfile
import json
import re
import os

Author = "LukeBob"

## Colours
class Color():
    @staticmethod
    def red(str):
        return "\033[91m" + str + "\033[0m"

    @staticmethod
    def green(str):
        return "\033[92m" + str + "\033[0m"

    @staticmethod
    def yellow(str):
        return "\033[93m" + str + "\033[0m"

    @staticmethod
    def blue(str):
        return "\033[94m" + str + "\033[0m"


## Banner
banner = (Color.green(
    """
 _____         _             _         _   _                _     _   _
|  ___|       | |           (_)       | | | |              | |   | | | |
| |_ __ _  ___| |_ ___  _ __ _  ___   | |_| | ___  __ _  __| |___| | | |_ __
|  _/ _` |/ __| __/ _ \| '__| |/ _ \  |  _  |/ _ \/ _` |/ _` / __| | | | '_ '
| || (_| | (__| || (_) | |  | | (_) | | | | |  __/ (_| | (_| \__ \ |_| | |_) |
\_| \__,_|\___|\__\___/|_|  |_|\___/  \_| |_/\___|\__,_|\__,_|___/\___/| .__/
                                                                       | |
                                                                       |_|
Author: {0}
    """).format(Color.blue(Author)))




## Factorio Main Class Example, app = Factorio('Stable').RequestVersion() <== Gets you Latest Version From https://factorio.com/
class Factorio():
    def __init__(self, version):
        self.version      = version
        self.url          = 'https://www.factorio.com'
        self.experimental = '/download-headless/experimental'
        self.stable       = '/download-headless/stable'

## Gets Latest Version
    def RequestVersion(self):
        try:
            r=requests.get(self.url)

            s = re.findall("Stable: (\d{0,3}.\d{0,3}.\d{0,3})", r.text)
            e = re.findall("Experimental: (\d{0,3}.\d{0,3}.\d{0,3})", r.text)

            if self.version == 'stable':
                i = s[0]
                return(i)

            elif self.version == 'experimental':
                i = e [0]
                return(i)
        except:
            print(Color.red("\n[Error]:")+"Could not find the latest version from: https://www.factorio.com")
            exit(0)


## Downloads Latest Version
    @staticmethod
    def Download(version):
        url = "https://www.factorio.com/get-download/{0}/headless/linux64".format(version)
        local_filename = "factorio-headless-{0}.tar.gz".format(version)
        print("\n"+Color.green("===>")+" Latest Version: {0}".format(version))

        try:
            r=requests.get(url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
        except:
            raise
            exit(0)

        print("\n"+Color.green("===>")+" Downloaded File: {0}".format(local_filename))

        try:
            print("\n"+Color.green("===>")+" Extracting ({0}) to (factorio)".format(local_filename))
            tar = tarfile.open(local_filename)
            tar.extractall(path='factorio-new-{0}'.format(version))
            tar.close()
        except tarfile.ReadError:
            print(Color.red("\n[Error]:")+" Tarfile could not open file {0}. Are you using python3 ?. ".format(Color.blue(local_filename)))
            exit(0)


## Gets New Json Data Ready For Writing To New Json File
def write_json(sta_cur, exp_cur):
    data = {}
    data['Stable'] = sta_cur
    data['Experimental'] = exp_cur

    ## Clear Last
    with open("Config.json", 'w') as f:
        json.dump([], f)

    with open("Config.json", 'w') as f:
        json.dump(data, f)


## Writes New Json Config
def update_config(type, version):
    (sta_cur, exp_cur) = parse_config()
    if type == "stable":
        try:
            write_json(version, exp_cur)
        except:
            raise
        print(Color.green("\n===>")+" Updated Json Config")
        print(Color.green("\n===>")+" Finished...\n")

    elif type == "experimental":
        try:
            write_json(sta_cur, version)
        except:
            raise
            return(None)

        print(Color.green("\n===>")+" Updated Json Config")
        print(Color.green("\n===>")+" Finished...\n")



## Removes old factorio.tar.gz
def Remove_junk(version):
    try:
        cmd = "rm -r factorio-headless-{0}.tar.gz".format(version)
        os.system(cmd)
    except:
        raise
    print(Color.green("\n===>")+" Removed Junk Files")



## Parses Current Versions From Json Configs
def parse_config():
    try:
        with open('Config.json', 'r') as f:
            config = json.load(f)
    except:
        raise
        print(Color.red("\n===> Could not find config..."))
        exit(0)

    sta_cur = config["Stable"]
    exp_cur = config["Experimental"]
    return(sta_cur, exp_cur)


def print_versions(our_ver, site_ver):
    print("""
------------------------
Your version:   ({0})
------------------------
Latest Version: ({1})
------------------------
        """.format(Color.red(our_ver), Color.green(site_ver)))

## Main Stuff
def main(args, parser):

## Stable object
    stab_app = Factorio('stable')
## Experimental object
    exp_app  = Factorio('experimental')
## Latest Stable Version
    stab_ver = stab_app.RequestVersion()
## Latest Experimental Version
    exp_ver  = exp_app.RequestVersion()
## Our Versions From Config.json
    (sta_cur, exp_cur) = parse_config()


## stable check
    if args.stable and args.check:
        if stab_ver != sta_cur:
            if stab_ver == 'No':
                print_versions(sta_cur, "None")
                print(Color.red("\n[+] Error: ")+"No Latest \"Stable\" Version Available!\n")
            else:
                print_versions(sta_cur, stab_ver)
                print(Color.green("\n\n===>")+" New Update Available -- Version ({0}), Update with, \"python3 factorio.py --stable --download\"\n".format(Color.blue(stab_ver)))
                exit(0)

        elif stab_ver == sta_cur:
            print_versions(sta_cur, stab_ver)
            print(Color.green("\n\n===>")+" Up to date with the latest binary -- Version ({0})\n".format(Color.blue(stab_ver)))
            exit(0)

## stable download
    elif args.stable and args.download:
        if stab_ver == sta_cur:
            print(Color.red("\n[+] ERROR: ")+"Version ({0}) already up to date, Force download by changing Config.json stable value back to (0) and running again.\n".format(Color.blue(stab_ver)))
            exit(0)

        elif stab_ver != sta_cur:
            if stab_ver == 'No':
                print(Color.red("\n[+] Error: ")+"No Latest \"Stable\" Version Available!\n")
                exit(0)
            else:
                stab_app.Download(stab_ver)
                Remove_junk(stab_ver)
                update_config('stable', stab_ver)


## experimental check
    elif args.experimental and args.check:
        if exp_ver != exp_cur:
            if exp_ver == 'No':
                print_versions(exp_cur, "None")
                print(Color.red("\n[+] Error: ")+"No Latest \"Experimental\" Version Available!\n")
            else:
                print_versions(exp_cur, exp_ver)
                print(Color.green("\n\n===>")+" New Update Available -- Version ({0}), Update with, \"python3 factorio.py --experimental --download\"\n".format(Color.blue(exp_ver)))
                exit(0)

        elif exp_ver == exp_cur:
            print_versions(exp_cur, exp_ver)
            print(Color.green("\n\n===>")+" Up to date with the latest binary -- Version ({0})\n".format(Color.blue(exp_ver)))
            exit(0)

## experimental download
    elif args.experimental and args.download:
        if exp_ver == exp_cur:
            print(Color.red("\n[+] ERROR: ")+"Version ({0}) already up to date, Force download by changing Config.json experimental value back to (0) and running again.\n".format(Color.blue(exp_cur)))
            exit(0)

        elif exp_ver != exp_cur:
            if exp_ver == 'No':
                print(Color.red("\n[+] Error: ")+"No Latest \"Experimental\" Version Available!\n")
                exit(0)
            else:
                exp_app.Download(exp_ver)
                Remove_junk(exp_ver)
                update_config('experimental', exp_ver)
                exit(0)
    else:
        parser.print_help()
        exit(0)

if __name__ == '__main__':
    ## Argparse Stuff
    parser = argparse.ArgumentParser(description="Factorio HeadsUp Linux (v-1.0)", epilog="Author: LukeBob")
    parser.add_argument("--stable", action='store_true', help="Check/Download Stable Version")
    parser.add_argument("--experimental", action='store_true', help="Check/Download Experimental Version")
    parser.add_argument("--check", action='store_true', help='Check your version against the latest.')
    parser.add_argument("--download", action='store_true', help='Download latest Factorio headless binary')
    args = parser.parse_args()
    print(banner)
    main(args, parser)

