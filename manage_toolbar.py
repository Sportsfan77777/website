"""
finds a toolbar in a set of globbed html files
and updates it with the current toolbar that is stored in
'*****_toolbar.txt' where '*****' is the name of the toolbar

1st argument is the name of the toolbar (required)
"""

import os
import shutil
import sys
import glob

name = "the name of the toolbar "

if len(sys.argv) <= 1:
    print "   *** Must have the name of the toolbar as the first argument ***"
    exit()
else:
    name = sys.argv[1] # 1st Argument

#### The argument is supplied ####

print "Updating Toolbar named '%s'" % name
toolbar_fn = "%s_toolbar.html" % name

# (1) Get .html files
html_fns = glob.glob("*.html")

# (2) Locate the lines starting and ending the toolbar in each file
target_start = "<!-- start %s toolbar -->" % name
target_end = "<!-- end %s toolbar -->" % name

for html_fn in html_fns:
    # Check if this toolbar is in this file
    if (not target_start in open(html_fn).read()) or (not target_end in open(html_fn).read()):
        # If it is not, skip to next file in the loop
        print "Not present in file '%s'" % html_fn
        continue

    print "<<<< Present in file '%s' >>>>" % html_fn

    toolbar_f = open(toolbar_fn, "r") # will read from toolbar

    tmp_fn = "%s.tmp" % html_fn
    f = open(html_fn, "r") # Read to this file
    tmp_f = open(tmp_fn, "w") # Write to this file (mv it to old file later)

    in_toolbar = False

    # Read line by line
    for line in f:
        if in_toolbar:
            # If in toolbar, do not copy (instead, write from a different file -- see below)
            #pass
            # Check if this is the end of the toolbar
            if target_end in line:
                # Unmark 'in_toolbar'
                in_toolbar = False
                # Write this line
                tmp_f.write(line)
        else:
            # If not in toolbar, copy line to tmp
            tmp_f.write(line)
            # Check if this is the start of the toolbar
            if target_start in line:
                # Mark 'in_toolbar'
                in_toolbar = True
                # Then, copy toolbar from .txt file to .html.tmp file
                for toolbar_line in toolbar_f:
                    tmp_f.write(toolbar_line)

    # Move tmp file to old file name
    shutil.move(tmp_fn, html_fn) # move(src, dst)

    # Close Files
    f.close()
    tmp_f.close()
    toolbar_f.close()



