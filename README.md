# php_version_switcher
Switching PHP version on Windows Using Python

Create the module and save it in the Lib folder of the python for it to b sued as a module in windows
since windows doesn't has something that can be executed by the global path.

Then we can run the following 


Installation:

just save the code switch.py file inside the C:/python39/Lib [ur python installed location]  folder then create a file in c:/php_loc.txt with the folder location of php[root one] eg: c:/php/ this location basically of mine has many php version folders in them after that run the below command.
if u have largon installed at the default location then it will capture the file path of that , but if not then u got to do this config file creation process.

python -m switch
