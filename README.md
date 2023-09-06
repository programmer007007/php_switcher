# PHP Version Switcher

Easily switch between different PHP versions on Windows using Python.

## Installation:

### 1. Clone the Project
First, clone the project to your desired location.

### 2. Save the Script
Save the `switch.py` file in your Python's library directory. For instance, if you have Python 3.9 installed, place it in:
```
C:/python39/Lib
```
> **Note**: Replace the path with your actual Python installation directory.

### 3. Configure PHP Location
Create a file named `php_loc.txt` in your C: drive. Inside this file, specify the root directory of your PHP installations. 

For example:
```
c:/php/
```
In this example, the `c:/php/` directory contains multiple subdirectories, each representing a different version of PHP.

### 4. Execute the Script
To switch between PHP versions, run the following command:
```
python -m switch
```

---
