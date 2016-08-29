"""
Finds text and replaces it with other text
Example Usage:
(1) python find_replace.py
(2) python find_replace.py "replaceThis" "withThis"
(3) python find_replace.py "replaceThis" "withThis" "inTheseFiles"
(4) python find_replace.py -f "replaceThis" -r "withThis"
(5) python find_replace.py -f "replaceThis" -r "withThis" --format "inTheseFiles"
*** If you use method (1), all of the defaults must be changed in the script ***
*** If you use method (2) or (4), the default file format must be changed in the script ***
    
Optional Arguments:
  -h, --help            displays help message and exits
  -f FIND               text to find
  -r REPLACE            text to replace
  --format=FILE_FORMAT  search files with this glob.glob format
  -b                    backs up each file as 'each filename'.frtmp
Author's Notes:
(1)
At present, it is easiest to use this script in the same directory as the target files.
Though, this script may be used in other directories if the file format is properly specified.
(2)
You can do this with unix too (src: http://stackoverflow.com/questions/15402770/how-to-grep-and-replace)
find /path/to/files -type f -exec sed -i 's/oldstring/new string/g' {} \;
Polish: 7
"""

import shutil
import sys
import glob
import fileinput
from optparse import OptionParser

####### DEFAULTS (an alternative to supplying these as arguments) #######

# (1,2) Replace Old Text 'default_old' with 'default_new'
default_old = ">snowy</"
default_new = ">Michael Hammer</"

# (3) Search these files (Example formats: "file.txt", "*.txt", "*.py", "*.*")
default_format = "*.html"


def find_replace(old, new, file_format, backup):
    """
    Parameters: old, new, file_format
    (1) Finds all files matching the wildcard 'file_format'
    (2) For each file, replace any occurence of 'old' with 'new'
    Returns: nothing
    """

    filenames = glob.glob(file_format)
    num_files = len(filenames)

    # Backup Files as a precaution
    if backup:
        for fn in filenames:
           shutil.copy(fn, fn + ".frtmp")

    # Count occurences of 'old'
    total_count = 0
    # Print occurences to stdout
    stdout = sys.stdout

    for fn in filenames:
        count = 0
        for line in fileinput.input(fn, inplace = True):
            # Monitor occurences
            if old in line:
                count += 1
                # First count
                if count is 1:
                     stdout.write("Found in %s\n" % fn)
                # Any count
                stdout.write("*** (%d) %s: '%s' ***\n" % (count, fn, line[:-1])) # Trim '\n' from line

            # Replace 'old' with 'new'
            print(line.replace(old, new).rstrip())
        # Check if found
        if count is 0:
            stdout.write("<<< Not found in %s: %s >>>" % (fn, line))
        # Update Total Count
        total_count += count

    if num_files is 0:
        stdout.write("[Error: No file matches the specified file format]\n")
    elif num_files > 1:
        stdout.write("In %d files, there were %d occurences of '%s'\n" % (num_files, total_count, old))



def new_option_parser():
    """ 
    Handles input
    Returns: OptionParser
    """
    parser = OptionParser()
    parser.add_option("-f", 
                      dest="find", default = None,
                      help="text to find")
    parser.add_option("-r", 
                      dest="replace", default = None,
                      help="text to replace")
    parser.add_option("--format", 
                      dest="file_format", default = None,
                      help="search files with this glob.glob format")
    parser.add_option("-b", action="store_true", 
                      dest="backup", default = False,
                      help="backs up each file as 'each filename'.frtmp")
    return parser

######## MAIN ########
if __name__ == '__main__':
    parser = new_option_parser()
    options, args = parser.parse_args()

    ### Future Modification: also handle arguments without optionParser ###

    # Check for supplied arguments
    if options.find is None:
        options.find = default_old

    if options.replace is None:
        options.replace = default_new

    if options.file_format is None:
        options.file_format = default_format

    # Find + Replace
    find_replace(options.find, options.replace, 
                 options.file_format, options.backup)