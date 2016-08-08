#!/usr/bin/python
import os
import sys
import getopt

def myhelp():
 print "Usage: "
 print "%s [options]... [file]..." % sys.argv[0]
 print "Options: "
 print "-c,--bytes: print the byte counts."
 print "-l,--lines: print the newline counts."
 print "-w,--words: print the word counts."
 print "-m,--chars: print the character counts."
 print "--files0-from=F: read input from the files specified by NUL-terminated names in file F; If F is - then read names from standard input"
 print "--help: print this help and exits."
 print "--version: output version information and exit."
 exit(0) 

def version():
 print "wc.py (Herrada coreutils) 1.0"
 exit(0)

def sort_opts(opt):
# The counts are printed in this order: newlines, words, characters, bytes
 opt_order={'-l':1,'-w':2,'-m':3,'-c':4}
 return (opt_order[opt],opt)

#Do counting using standard input as a data source
def count_words_lines_bytes_stdin(filename,opts):
 wordcount=0
 countlines=0
 charcount=0

 for line in filename:
  charcount+=len(line) 
  line=line.split()
  wordcount+=len(line)
  countlines+=1  
 countbytes=charcount
 
 x=[] 
 filename=''
 if opts:
  results={'-c':countbytes,'-l':countlines,'-w':wordcount,'-m':charcount}
  x = [str(results[i]) for i in opts]  
  x.append(filename) 
 else:
   for i in [countlines,wordcount,countbytes,filename]:
    x.append(str(i)) 
 return x


#Doing couting using regular files as data source
def count_words_lines_bytes(filename,opts):

 if len(opts)==0:
  opts=['-l','-w','-m']

 #TEsting if is a regular file
 if os.path.isfile(filename):
  countbytes=os.stat(filename).st_size
  try:
   myfile=open(filename)
  except Exception as e:
   print e
   return 0
 #Checking if it is directory
 elif os.path.isdir(filename):
  print "%s: Is a directory" % filename
  p=[str(0) for i in opts]
  p.append(filename)
  return p
 else:
  #If file does not exist, show error and continue executing script
  print "%s: No such file or directory" % filename 
  return 0

 #The count of bytes and count of characters are calculated in the same way
 #which is by calling the system call stat. There is no need to scan through the file 
 #to find out those values. 
 
 if len(opts) == 1 and opts[0]=='-c': return [str(countbytes),filename]
 if len(opts) == 1 and opts[0]=='-m': return [str(countbytes),filename]
 if len(opts) == 2 and opts[0]=='-m' and opts[1]=='-c':
  return [str(countbytes),str(countbytes),filename]

 wordcount=0
 countlines=0
# charcount=0
# Counting lines and words by scanning through the file.
# Then spliting each lines using space separator as delimiter.
# This is the expensive part of the code. C/C++ counterpart is far more efficient.

 for line in myfile:
  #charcount+=len(line) 
  line=line.split()
  wordcount+=len(line)
  countlines+=1  

 #Building return value as a list of counters plus the filename. 
 #The order of the counters returned is always as follow: line,words,characters and bytes
 x=[] 

 #Observation:
 #Couting of bytes (option -c) and characters (option -m) is performed in the very same way which
 #is by applying stat system call to the filename. The C implementation in GNU core does the same.

 results={'-c':countbytes,'-l':countlines,'-w':wordcount,'-m':countbytes}
 x = [str(results[i]) for i in opts]  
 x.append(filename) 
 return x

#Function to format output in columns with the proper right and left justification
def report(results,n):
 if n==0: n=3
 justification=[] 

 for i in range(n+1):
  p=[j[i] for j in results]
  q=max([len(k) for k in p])
  justification.append(q) 
 
 rj=justification.pop() 
 #Right justification for the numbers
 myformat=' '.join([ '{'+str(k)+':>'+str(v)+'}' for (k,v) in enumerate(justification)]) 
 
 #Left Justification for the filename
 myformat+=' {'+str(n) + ':<' + str(rj)+'}'

 for i in results:
  print myformat.format(*i) 

#Function that add the total line to the results when there is more than one filename in the arguments 
def total(results,n):
 if n==0: n=3
 total=[]
 for i in range(n):
  total.append(str(sum([ int(k[i]) for k in results])))

 total.append('total')   
 results.append(total)
 return results

#Implementation of the option --files0_from
def files0_from(datain,args):
 #Not allowing filenames in the command line when this option is used
 if args: 
  print "extra operand %s" % args[0]
  print "file operands cannot be combined with --files0-from"
  exit(1)

 if datain == '-':
   #Waiting data from stdin 
  input1=sys.stdin
 else:
  if os.access(datain,os.R_OK):
   input1=open(datain)
  else:
   print "cannot open %s for reading: No such file or directory" % datain
   
  # Filenames contained in input1 MUST BE NULL separated. If so, each filename is stored in
  # list args  
 args=[]
 for i in input1:  
  i=i.strip()
  for j in i.split('\0'):
   args.append(j) 
 args.pop() 
 return args 
  
if __name__ == '__main__' :

 #Using getopt module for handling command line options
 try:
  opts,args=getopt.getopt(sys.argv[1:],'cwlm',['bytes','words','lines','chars','version','help','files0-from='])
 except getopt.GetoptError as e:
  print "Bad arguments. Check help below." 
  myhelp()

 newopts={}
 results=[]
 opts=dict(opts)
 for o in opts:
  if o in ('-c','--bytes'): newopts.setdefault('-c')
  elif o in ('-w','--words'): newopts.setdefault('-w')
  elif o in ('-l','--lines'): newopts.setdefault('-l')
  elif o in ('-m','--chars'): newopts.setdefault('-m')
  elif o in ('--files0-from'): args=files0_from(opts['--files0-from'],args) 
  elif o in ('--help'): myhelp()
  elif o in ('--version'): version()
  
 #No filenames provided which means waiting data from standard input
 if len(args) == 0:
  results=[count_words_lines_bytes_stdin(sys.stdin,sorted(newopts,key=sort_opts))]
 else:
  for arg in args:
   x=count_words_lines_bytes(arg,sorted(newopts,key=sort_opts))
   if x == 0: 
   #Just pass when one of the filenames does not exist but display error.
    pass
   else:
    results.append(x)

 #If more than one filename was provided, add the total line
 if len(args)>1: total(results,len(newopts))
 
 #Present output in nice format
 if results:
  report(results,len(newopts))
