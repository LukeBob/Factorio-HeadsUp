import argparse
import requests
import tarfile
import json
import re, os, sys

Author = "LukeBob"
## Coulors
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

## Bruce Banner
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


## Factorio Main CLass Example, app = Factorio('Stable').RequestVersion() <== Gets you Latest Version From https://factorio.com/
class Factorio():
    def __init__(self, version):
        self.version      = version
        self.url          = 'https://www.factorio.com'
        self.experimental = '/download-headless/experimental'
        self.stable       = '/download-headless/stable'

## Gets Latest Version
    def RequestVersion(self):
        try:
            url_list = []
            if(self.version == None):
                return(None)
            r=requests.get("{0}".format(self.url))

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
def Download(version, link):
    url = "{0}/get-download/{1}/headless/linux64".format(link, version)
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
    except:
        raise

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

    elif type == "experimental":
        try:
            write_json(sta_cur, version)
        except:
            raise
            return(None)

        print(Color.green("\n===>")+" Updated Json Config")

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

## Main Stuff
def main(args, parser):

    if args.stable and args.check:
        app = Factorio('stable')
        site_version = app.RequestVersion()
        (sta_cur, exp_cur) = parse_config()

        if site_version != sta_cur:
            print("""
----------------
Your version:   ({0})
----------------
Latest Version: ({1})
----------------
            """.format(Color.red(sta_cur), Color.green(site_version)))
            print(Color.green("\n\n===>")+" New Update Available -- Version ({0}), Update with, \"python3 factorio.py --stable --download\"\n".format(Color.blue(site_version)))
            exit(0)

        elif site_version == sta_cur:
            print("""
----------------
Your version:   ({0})
----------------
Latest Version: ({1})
----------------
            """.format(Color.green(sta_cur), Color.green(site_version)))
            print(Color.green("\n\n===>")+" Up to date with the latest binary -- Version ({0})\n".format(Color.blue(site_version)))
            exit(0)


    elif args.stable and args.download:
        app = Factorio('stable')
        site_version = app.RequestVersion()
        (sta_cur, exp_cur) = parse_config()

        if site_version == sta_cur:
            print(Color.red("\nERROR: ")+"Version ({0}) already up to date, Force download by changing Config.json values back to (0) and running again.\n".format(sta_cur))
            exit(0)
        elif site_version != sta_cur:
            Download(site_version, app.url)
            Remove_junk(site_version)
            update_config('stable', site_version)


    elif args.experimental and args.check:
        app = Factorio('experimental')
        site_version = app.RequestVersion()
        (sta_cur, exp_cur) = parse_config()


        if site_version != exp_cur:
            print("""
----------------
Your version:   ({0})
----------------
Latest Version: ({1})
----------------
            """.format(Color.red(exp_cur), Color.green(site_version)))
            print(Color.green("\n\n===>")+" New Update Available -- Version ({0}), Update with, \"python3 factorio.py --experimental --download\"\n".format(Color.blue(site_version)))
            exit(0)

    elif args.experimental and args.download:
        app = Factorio('stable')
        site_version = app.RequestVersion()
        (sta_cur, exp_cur) = parse_config()

        if site_version == exp_cur:
            print(Color.red("\n[+] ERROR: ")+"Version ({0}) already up to date, Force download by changing Config.json values back to (0) and running again.\n".format(exp_cur))
            exit(0)

        elif site_version != exp_cur:
            Download(site_version, app.url)
            Remove_junk(site_version)
            update_config('experimental', site_version)
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
