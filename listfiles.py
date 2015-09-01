# python 3
# List files, set options at the top

# Name of file to write to, relative or absolute
fname = 'output.txt'
# Path to folder to scan
drpath = '/path/to/folder'

##################################################

from os import walk

str(drpath)
f = []
for (dirpath, dirnames, filenames) in walk(drpath):
  
        
    f.extend(dirnames)
    b = open( fname, 'a' )
    b.write("\n".join(f))
    b.close()
    
    break
