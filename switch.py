import os
import winreg
import subprocess


def modify_user_path_with_php_folder(php_dir):
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

    # Refresh environment variables
    subprocess.call(["refreshenv"], shell=True)

    # Wait for the exit signal
    print(f"PHP folder '{selected_folder}' added to the user PATH variable. Waiting for exit signal...")

    exit_signal = input("Press Enter to remove the PHP folder from the user PATH variable and exit.")

    # Remove the PHP folder from the user PATH variable in the Windows registry
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        with winreg.OpenKey(hkey, user_reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path = winreg.QueryValueEx(key, 'Path')[0]
            new_path = ';'.join(entry for entry in current_path.split(';') if entry.lower() != selected_folder.lower())
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)

    # Refresh environment variables
    subprocess.call(["refreshenv"], shell=True)

    print(f"PHP folder '{selected_folder}' removed from the user PATH variable. Exiting...")


if __name__ == '__main__':
    php_dir = r'C:\laragon\bin\php'
    modify_user_path_with_php_folder(php_dir)
