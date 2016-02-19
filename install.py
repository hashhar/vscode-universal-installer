#!/usr/bin/python3

import urllib
import urllib.request
import shutil
import subprocess
import platform

app_osx_stable_link = "http://go.microsoft.com/fwlink/?LinkID=620882"
windows_stable_link = "http://go.microsoft.com/fwlink/?LinkID=623230"
linux64_stable_link = "http://go.microsoft.com/fwlink/?LinkID=620884"
linux32_stable_link = "http://go.microsoft.com/fwlink/?LinkID=620885"

app_osx_stable_file = "VSCode-darwin.zip"
windows_stable_file = "VSCodeSetup-stable.exe"
linux64_stable_file = "VSCode-linux-x64-stable.zip"
linux32_stable_file = "VSCode-linux-ia32-stable.zip"

app_osx_insider_link = "http://go.microsoft.com/fwlink/?LinkId=723966"
windows_insider_link = "http://go.microsoft.com/fwlink/?LinkId=723965"
linux64_insider_link = "http://go.microsoft.com/fwlink/?LinkId=723968"
linux32_insider_link = "http://go.microsoft.com/fwlink/?LinkId=723969"

app_osx_insider_file = "VSCode-darwin-insider.zip"
windows_insider_file = "VSCodeSetup-insider.exe"
linux64_insider_file = "VSCode-linux-x64-insider.zip"
linux32_insider_file = "VSCode-linux-ia32-insider.zip"

def main():
	# Check the channel users want to use
	print("There are currently two channels available: Insider and Stable (or Preview)")
	insider = input("Download from the Insider channel? (y or n): ")
	if insider != 'y':
		insider = 'n'
	# Check the current platform and architecture
	# We don't care about bitness for Windows and Apple
	if platform.system() == "Linux":
		os_type = 'l'
		if platform.machine().endswith("64"):
			os_64bit = 'y'
		else:
			os_64bit = 'n'
	elif platform.system() == "Darwin":
		os_type = 'a'
		os_64bit = "64"
	elif platform.system() == "Windows":
		os_type = 'w'
		os_64bit = "64"
	else:
	# Collect the information manually instead of failing
		print("We were unable to determine your operating system type...")
		os_type = input("l for Linux, w for Windows, a for Apple OSX: ")
		if os_type == 'l':
			os_64bit = input("64 bit OS? (y or n): ")

	# Set the download links according to collected information
	# Insider channel
	if insider == 'y':
		if os_type == 'w':
			latest_url = windows_insider_link
		elif os_type == 'a':
			latest_url = app_osx_insider_link
		elif os_type == 'l':
			if os_64bit == 'y':
				latest_url = linux64_insider_link
			else:
				# Assuming anything other than y for 64bit meant a no
				latest_url = linux32_insider_link
				os_64bit = 'n'
	# Stable channel
	else:
		if os_type == 'w':
			latest_url = windows_stable_link
		elif os_type == 'a':
			latest_url = app_osx_stable_link
		elif os_type == 'l':
			if os_64bit == 'y':
				latest_url = linux64_stable_link
			else:
				# Assuming anything other than y for 64bit meant a no
				latest_url = linux32_stable_link
				os_64bit = 'n'

	# Hopefully we have got the links right by now
	# Download the file and take steps depending on the OS
	download(latest_url, os_type, os_64bit, insider)

	# Insider install
	if insider == 'y':
		if os_type == 'w':
			# Interactive install for Windows users. YAY!!!
			launch_setup = "./" + windows_insider_file
			win_install = subprocess.run(launch_setup)
			return
		elif os_type == 'a':
			# TODO: I don't know anything about OSX
			print("This hasn't been implemented yet...Sorry!!!")
			return
		elif os_type == 'l':
			install_dir = input("Where should we install the package? (Full absolute path): ")
			# Build the installation commands (unzip, symlink, icon, .desktop files)
			# TODO: What if no root access?
			if os_64bit == 'y':
				unzip_cmd = "unzip " + linux64_insider_file + " -d " + install_dir
				symlink_cmd = "sudo ln -s " + install_dir + linux64_insider_file[0:-4] + "/Code /usr/local/bin/code"
				icon_cmd = "sudo cp " + install_dir + linux64_insider_file[0:-4] + "/resources/app/resources/linux/VSCode.png /usr/share/icons/hicolor/512x512/apps/VSCode.png"
			else:
				unzip_cmd = "unzip " + linux32_insider_file + " -d " + install_dir
				symlink_cmd = "sudo ln -s " + install_dir + linux32_insider_file[0:-4] + "/Code /usr/local/bin/code"
				icon_cmd = "sudo cp " + install_dir + linux32_insider_file[0:-4] + "/resources/app/resources/linux/VSCode.png /usr/share/icons/hicolor/512x512/apps/VSCode.png"
			# The desktop file is common to everyone
			desktop_file_cmd = "sudo cp " + "VSCode.desktop /usr/share/applications/VSCode.desktop"

			# Execute the commands
			unzip_process = subprocess.run(unzip_cmd.split(), stdout=subprocess.PIPE)
			symlink_process = subprocess.run(symlink_cmd.split(), stdout=subprocess.PIPE)
			icon_process = subprocess.run(icon_cmd.split(), stdout=subprocess.PIPE)
			desktop_process = subprocess.run(desktop_file_cmd.split(), stdout=subprocess.PIPE)
			print("Installation finished. You can run VSCode from the Applications menu or by typing 'code' into a terminal.")
	# Stable install
	else:
		if os_type == 'w':
			# Interactive install for Windows users. YAY!!!
			launch_setup = "./" + windows_stable_file
			win_install = subprocess.run(launch_setup)
			return
		elif os_type == 'a':
			# TODO: I don't know anything about OSX
			print("This hasn't been implemented yet...Sorry!!!")
			return
		elif os_type == 'l':
			install_dir = input("Where should we install the package? (Full absolute path): ")
			# Build the installation commands (unzip, symlink, icon, .desktop files)
			# TODO: What if no root access?
			if os_64bit == 'y':
				unzip_cmd = "unzip " + linux64_stable_file + " -d " + install_dir
				symlink_cmd = "sudo ln -s " + install_dir + linux64_stable_file[0:-4] + "/Code /usr/local/bin/code"
				icon_cmd = "sudo cp " + install_dir + linux64_stable_file[0:-4] + "/resources/app/resources/linux/VSCode.png /usr/share/icons/hicolor/512x512/apps/VSCode.png"
			else:
				unzip_cmd = "unzip " + linux32_stable_file + " -d " + install_dir
				symlink_cmd = "sudo ln -s " + install_dir + linux32_stable_file[0:-4] + "/Code /usr/local/bin/code"
				icon_cmd = "sudo cp " + install_dir + linux32_stable_file[0:-4] + "/resources/app/resources/linux/VSCode.png /usr/share/icons/hicolor/512x512/apps/VSCode.png"
			# The desktop file is common to everyone
			desktop_file_cmd = "sudo cp " + "VSCode.desktop /usr/share/applications/VSCode.desktop"

			# Execute the commands
			unzip_process = subprocess.run(unzip_cmd.split(), stdout=subprocess.PIPE)
			symlink_process = subprocess.run(symlink_cmd.split(), stdout=subprocess.PIPE)
			icon_process = subprocess.run(icon_cmd.split(), stdout=subprocess.PIPE)
			desktop_process = subprocess.run(desktop_file_cmd.split(), stdout=subprocess.PIPE)
			print("Installation finished. You can run VSCode from the Applications menu or by typing 'code' into a terminal.")
	# Return, we are done
	return

# Helper to download the correct file and write it to disk
# TODO: What if the current working directory is read-only?
def download(latest_url, os_type, os_64bit, insider):
	# Set the file name according to the target OS and channel
	if insider == 'y':
		if os_type == 'w':
			file_name = windows_insider_file
		elif os_type == 'a':
			file_name = app_osx_insider_file
		elif os_type == 'l':
			if os_64bit == 'y':
				file_name = linux64_insider_file
			else:
				file_name = linux32_insider_file
	else:
		if os_type == 'w':
			file_name = windows_stable_file
		elif os_type == 'a':
			file_name = app_osx_stable_file
		elif os_type == 'l':
			if os_64bit == 'y':
				file_name = linux64_stable_file
			else:
				file_name = linux32_stable_file
	
	# Let's get that file
	# TODO: Better alternative to urllib?
	with urllib.request.urlopen(latest_url) as response, open(file_name, 'wb') as out_file:
		print("Please wait... The download is in progress.")
		shutil.copyfileobj(response, out_file)
	return

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		raise SystemExit
