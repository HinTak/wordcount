This script is my own implementation of Linux command wc.

Side Notes about wc.py

### Performance:
As file size increases, the execution time of GNU wc version becomes remarkable better that my wc python version.
However, for sizes less than 100 MB the execution time is comparable.
 
|Filesize|C GNU(sec)|python (sec)|
--------- ---------  ------------
|104 MB|1.064|1.70|
|196MB|2.17|3.19|
|588MB|6.413|9.69|  
 
Conclusion: It is difficult to beat compiled code over interpreted one.
 
### Options: 
All of the command options were implemented except one. 
The handling of command line options is managed by module getopt.

I decided to skip option 'L' since I could not figure out and efficient
way to calculate maximum line length. 
I could have used brute force (max function or comparison of subsequent values)
but that is computationally expensive.
 
### Data Source:
    I considered the 3 posible data sources:
    1. several filenames from command line
    2. Standard input
    3. The --files0-from=file option
 
### Format of the output:
       I used right justification for the numbers and left justification for filename.
       The presentation of the data differs from the wc GNU but it is still nice.
 
### Error Handling:
      I properly handle errors for the following situations:
      a.- Invalid option in command line
      b.- Non-existent file provided as argument.
          Script display error message for non-existent files 
          and correct output for the existing ones.
      c.- File is not readable or file type is a directory.
      d.- Option --files0_from used along with filenames as arguments.
 
### Comment on line counting:
      wc GNU implementation count new lines based on the number of character '\n' that
      it detects. So a "line" terminated with a null string (\0) is not counted. This occurs at the 
      end of file.
      For example generate a null terminated line:
      #find . -name '*' -print0 >nullterminated.txt
       Then do the line counting:
      #wc nullterminated.txt 
       0   1 269 nullterminated.txt
  
      Line counting is zero. 
      My script does count this null-terminated line 
      

 
Luis
