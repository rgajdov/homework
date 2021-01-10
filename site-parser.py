import os
import shutil
from bs4 import BeautifulSoup

PATH_TO_ALL_FILES = r"C:\\Users\\admin\\Desktop\\undead_pages"
PATH_TO_SEPARATE_FILES = r"C:\\Users\\admin\\Desktop\\error_files"

result = {
    "ListFilesError": [],
    "CaptchaError": [],
    "UnicodeDecodeError": [],
    "AccountSuspendedError": [],
    "HtmlStructureError": [],
    "SiteNotAvailableError": [],
    "GarbageSiteError": [],
    "SmallHtmlFileError": [],
    "OtherError": [],
}


def parse_files():
    lst = os.listdir(PATH_TO_ALL_FILES)
    for filename in lst:
        with open(PATH_TO_ALL_FILES + '\\' + filename, "r") as fh:
            try:
                contents = fh.read()

                soup = BeautifulSoup(contents, 'html.parser')

                if soup.html is None or soup.head is None or soup.body is None or soup.title is None or not contents.rstrip().endswith("</html>"):
                    result["HtmlStructureError"].append(filename)

                else:
                    title = str(soup.title.text).strip().lower()

                    if "index of" in title:
                        result["ListFilesError"].append(filename)

                    elif "captcha" in title:
                        result["CaptchaError"].append(filename)

                    elif "account suspended" in title:
                        result["AccountSuspendedError"].append(filename)

                    elif "under construction" in title or "domain" in title or "unavailable" in title or "not available" in title:
                        result["SiteNotAvailableError"].append(filename)

                    else:
                        total_tag_count = 0
                        p_tag_count = 0
                        for child in soup.recursiveChildGenerator():
                            if child.name:
                                if child.name == 'p':
                                    p_tag_count += 1
                                else:
                                    total_tag_count += 1

                        if p_tag_count > total_tag_count:
                            result['GarbageSiteError'].append(filename)
                        else:
                            if len(contents) < 500:
                                result['SmallHtmlFileError'].append(filename)
                            else:
                                result['OtherError'].append(filename)

            except UnicodeDecodeError:
                result["UnicodeDecodeError"].append(filename)


if __name__ == '__main__':

    parse_files()

    total_files = [files for files in os.listdir(PATH_TO_ALL_FILES) if files.endswith('.html')]

    print(f'Total pages: {len(total_files)}')

    for item in result:
        print(f'\t{item}: {len(result[item])}')

        for file in result[item]:

            newpath = PATH_TO_SEPARATE_FILES + '\\\\' + item
            if not os.path.exists(newpath):
                os.mkdir(newpath)

            src = PATH_TO_ALL_FILES + '\\\\' + file
            dst = newpath + '\\\\' + file

            shutil.copy(src, dst)
