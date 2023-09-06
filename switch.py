import os
import winreg
import subprocess
import shutil


def check_and_clean_php_in_path():
    php_loc_arr = []
    
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        with winreg.OpenKey(hkey, r'Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path = winreg.QueryValueEx(key, 'Path')[0]
            # split the PATH and convert all entries to lowercase for case-insensitive comparison
            path_entries = current_path.split(';')

            # Identify and collect entries containing '/php' or '\php'
            for entry in path_entries:
                if '/php' in entry.lower() or '\\php' in entry.lower():
                    php_loc_arr.append(entry)

            # If we found any PHP entries, remove them
            if php_loc_arr:
                try:
                    new_path = ';'.join(path_entry for path_entry in path_entries if path_entry not in php_loc_arr)
                    winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                except Exception as e:
                    print(f"Error updating PATH: {e}")
                    return None

            return php_loc_arr

    return None

def modify_user_path_with_php_folder(php_dir):  
    check_and_clean_php_in_path()
    # Get the list of PHP versions
    php_versions = os.listdir(php_dir)

    # Display the list of PHP versions with their indices
    print("Available PHP versions:")
    for i, version in enumerate(php_versions):
        print(f"{i+1}. {version}")

    # Select the PHP version using the index
    selected_index = int(input("Enter the index of the PHP version to add to the user PATH variable: "))
    if selected_index < 1 or selected_index > len(php_versions):
        print("Invalid index. Exiting...")
        exit()

    selected_version = php_versions[selected_index - 1]
    selected_folder = os.path.join(php_dir, selected_version)            


    # Append the PHP folder to the user PATH variable in the Windows registry
    user_reg_path = r'Environment'
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        with winreg.OpenKey(hkey, user_reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path = winreg.QueryValueEx(key, 'Path')[0]
            new_path = f"{current_path}{os.pathsep}{selected_folder}"
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)

    # Wait for the exit signal
    print(f"PHP folder '{selected_folder}' added to the user PATH variable. Waiting for exit signal...")

    exit_signal = input("Press Enter to remove the PHP folder from the user PATH variable and exit.")
    check_and_clean_php_in_path()
    # Refresh environment variables
    subprocess.call(["refreshenv"], shell=True)

    print(f"PHP folder '{selected_folder}' removed from the user PATH variable. Exiting...")


if __name__ == '__main__':   
    print("*"*80)
    print("Welcome to PHP switcher", end='\n\n')
    print("This script will help you to add the PHP folder to the user PATH variable.", end='\n\n')    
    print("Author: Johnson | Email: andprogrammer007[@t]gm@ail.com ", end='\n\n')
    print("*"*80)
    php_dir = r'C:\laragon\bin\php' # default PHP folder location    
    if not os.path.exists(php_dir):        
        if os.path.exists(r'c:/php_loc.txt'):
            tmp_path = open(r'c:/php_loc.txt', 'r').read()
        if tmp_path != '':
            php_dir = tmp_path
        else:
            php_dir = input("Enter the path to the PHP folder: ")
            # save the php folder location to c:/php_loc.txt if the input is not empty and the file does not exist
            if php_dir != '' and not os.path.exists(r'c:/php_loc.txt'):
                open(r'c:/php_loc.txt', 'w').write(php_dir)    
    modify_user_path_with_php_folder(php_dir)
