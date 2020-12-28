#
from pathlib import Path
import zipfile
from zipfile import ZipFile

def print_files(alistoffiles):
    """Print a more readable ALISTOFFILES."""
    for file in alistoffiles:
        print(file)

def get_files(apattern, adir):
    """Return a list of files with APATTERN in ADIR."""
    list_files = []
    for afile in sorted(adir.rglob(apattern)):
        list_files.append(afile)

    return list_files

def write_files(allfiles, alistoffiles):
    """Create a text ALLFILES with ALISTOFFILES."""
    with open(allfiles, 'wt') as all_files:
        for file in alistoffiles:
            with open(file, 'rt') as afile:
                for line in afile:
                    all_files.write(line)

def get_regex_files(afilenames, aregex, adir):
    """Create a list of files that match AREGEX for files that share similar AFILENAME in ADIR."""
    list_of_files = []
    for afile in get_files(afilenames, adir):
        if aregex.match(afile.name):
            list_of_files.append(afile)
    return list_of_files

def sort_files_time(alistoffiles):
    """Return a sorted list of ALISTOFFILES based on the creation time of the file."""
    time_of_file = []
    name_of_file = []
    for file in alistoffiles:
        time_of_file.append(file.stat().st_mtime)
        name_of_file.append(file)
    return([x for _, x in sorted(zip(time_of_file, name_of_file))])

def create_txt_files(afileterm):
    """Write compiled text files of name AFILETERM."""
    files_to_compile = sort_files_time(get_files(afileterm, mx_dir))
    file_name = afileterm + '_logs_all.txt'
    write_files(mx_dir / file_name, files_to_compile)

def check_zip_ok(alistofzips):
    """Return a list of valid zip files out of ALISTOFZIPS."""
    checked_list = [x for x in alistofzips if zipfile.is_zipfile(x)]
    return checked_list

def get_root_path(alistofzips):
    """Return the root path to unzip ALISTOFZIPS."""
    return check_zip_ok(alistofzips)[0].parent

def get_path_to_unzip(alistofzips):
    """Return a list with the paths where to unzip ALISTOFZIPS."""
    dir_of_zips = [x.parts[-1].replace(".zip", "") for x in alistofzips]
    root_path = get_root_path(alistofzips)
    path_of_zips = [root_path.joinpath(x) for x in dir_of_zips]
    return path_of_zips

def unzip_files(alistofzips):
    """Decompress the files in ALISTOFFILES into a directory with the name of the file."""
    files_to_unzip = check_zip_ok(alistofzips)
    path_to_unzip = get_path_to_unzip(files_to_unzip)
    files_and_paths = zip(files_to_unzip, path_to_unzip)
    for apair in files_and_paths:
        afile, apath = apair
        zipfile.ZipFile(afile, mode='r').extractall(path=apath)

## General General Information(alistofzips):

esc_dir = Path('/data')
acase = input("Please enter Case number: ")
case_dir = esc_dir / acase

case_dirs = [a_file for a_file in case_dir.iterdir() if a_file.is_dir()]
mx_dir = [a_dir for a_dir in case_dirs if 'mx' in a_dir.name]

if len(mx_dir) > 1:
    print("This Case" , acase , " has more than one MX on file")
    print(mx_dir)
    mx_num = int(input("Please select a MX: "))
    mx_dir = mx_dir[mx_num]
else:
    mx_dir = mx_dir[0]

mx_dirs = [x for x in mx_dir.iterdir() if x.is_dir()]

## Generate the basic Server Logs
server_basic_root_dir = mx_dir.joinpath(Path('opt/SecureSphere/server/SecureSphereWork/logs'))
server_logs = get_files("server_log*.txt", server_basic_root_dir)
server_logs = sort_files_time(server_logs)
write_files(mx_dir / "basic_server_log.txt", server_logs)

## Generate the archived Server Logs
mx_zip_files = get_files("*.zip", mx_dir)
server_log_zip = [x for x in mx_zip_files if "server_log" in x.name]
# Keep the zipfiles with data
server_log_zip = check_zip_ok(server_log_zip)

## Unzip files
unzip_files(server_log_zip)

## Create a list with all the files from zip files
server_archive_root_dir = get_root_path(server_log_zip)
archive_server_logs = get_files("server_log*.txt", server_archive_root_dir)
archive_server_logs = sort_files_time(archive_server_logs)
write_files(mx_dir / "archive_server_log.txt", archive_server_logs)
all_server_logs = [mx_dir / "archive_server_log.txt", mx_dir / "basic_server_log.txt"]

print(" **** Select files to print with print_files(get_files(<pattern>) **** ")
print(" **** Use create_txt_files(<pattern> ****)")