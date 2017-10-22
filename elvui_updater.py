from lxml import html
import os, requests, re, zipfile

# TODO: Logging
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

def local_version(wow_dir):
    ''' Return version of local ELVUI install '''
    toc_loc = wow_dir + '\\interface\\addons\\ElvUI\\ElvUI.toc'

    # Read addon TOC file
    try:
        toc = open(toc_loc, 'r')
        toc_lines = toc.readlines()
        toc.close()
    except FileNotFoundError:
        return 'Not Installed'

    # Parse version string
    version = VERSION_RE.search(toc_lines[2])
    return version.group()

def update(version, wow_dir):
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
    elvui_zip.extractall(path='{:s}{:s}'.format(wow_dir, '\\interface\\addons\\'))

    # Cleanup
    elvui_zip.close()
    os.remove(local_filename)

def main():
    ''' Update if version mismatch '''
    # Identify local install
    try:
        settings = open('settings', 'r')
        wow_dir = settings.readline()
        settings.close()

    except FileNotFoundError:
        invalid = True

        # Configure WoW Dir
        while invalid:
            install_dir = input('Provide full URL for WoW Install Directory: ')
            if os.path.exists(install_dir):
                invalid = False
                wow_dir = install_dir

        # Write install dir to settings
        settings = open('settings', 'w')
        settings.write(install_dir)
        settings.close()

    # Get local and prod versions
    local = local_version(wow_dir)
    prod = prod_version()

    print('Installed Version: {:s}'.format(local))
    print('Live Version: {:s}'.format(prod))

    if local != prod:
        print('Updating...')
        update(prod, wow_dir)
        print('Update Complete')

if __name__ == '__main__':
    main()
