from lxml import html
import requests
import re
import zipfile

# TODO: Load dir from config file or create upon first use
WOW_DIR = "C:\\Program Files (x86)\\World of Warcraft"

''' Scrape ELVUI Downloads Page '''
ELVUI = requests.get('https://www.tukui.org/download.php?ui=elvui')
ELVUI_TREE = html.fromstring(ELVUI.content)
VERSION_RE = re.compile('[0-9]+\\.[0-9]+')

def prod_version():
    ''' Return current live version of ELVUI '''
    # Parse version string from ELVUI webpage
    version_str = ELVUI_TREE.get_element_by_id('version').text_content()

    # Parse version
    return VERSION_RE.search(version_str).group()

def local_version():
    ''' Return version of local ELVUI install '''
    toc_loc = WOW_DIR + '\\interface\\addons\\ElvUI\\ElvUI.toc'

    # Read addon TOC file
    toc = open(toc_loc, 'r')
    toc_lines = toc.readlines()
    toc.close()

    # Parse version string
    version = VERSION_RE.search(toc_lines[2])
    return version.group()

def update(version):
    ''' Download and install newest ELVUI '''
    # Download zip
    local_filename = 'elvui_{:s}.zip'.format(version)
    req = requests.get('https://www.tukui.org/downloads/elvui-{:s}.zip'.format(version), \
                        stream=True)

    with open(local_filename, 'wb') as download:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                download.write(chunk)

    # Unzip
    elvui_zip = zipfile.ZipFile(local_filename, 'r')

    # Extract to addons folder
    elvui_zip.extractall(path='{:s}{:s}'.format(WOW_DIR, '\\interface\\addons\\'))


def main():
    ''' Update if version mismatch '''
    local = local_version()
    prod = prod_version()

    print('Installed Version: {:s}'.format(local))
    print('Live Version: {:s}'.format(prod))

    if local != prod:
        print('Updating...')
        update(prod)
        print('Update Complete')

if __name__ == '__main__':
    main()
