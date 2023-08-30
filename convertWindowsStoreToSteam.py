#!/usr/bin/python

import re
import os
import time
import struct
import zlib
import shutil
from glob import glob

SAVE_PATH = './windows_store_save'

def retrieve_md5_file_name(content):
    return (content[0:4][::-1].hex() +
            content[4:6][::-1].hex() +
            content[6:8][::-1].hex() +
            content[8:16].hex()).upper()

def create_directory(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

def extract_files():
    for main_folder in glob(f'{SAVE_PATH}/wgs/*'):
        extract_folder = main_folder.replace('wgs/', '')
        with open(f'{main_folder}/containers.index', 'rb') as f:
            index_match = re.findall(re.compile(rb'\x00{4}\x10\x00{4}(.*?)$', re.MULTILINE | re.DOTALL), f.read())

        dir_dict = {}

        if index_match is not None:
            index_content = index_match[0]
            while len(index_content) > 0:
                num_bytes = struct.unpack('<i', index_content[0:4])[0]
                index_content = index_content[4:]
                directory_name = struct.unpack(f'<{str(num_bytes * 2)}s', index_content[0:num_bytes * 2])[0].replace(b'\x00', b'').decode('ascii')
                index_content = index_content[num_bytes * 4 + 4:]
                num_bytes = struct.unpack('<i', index_content[0:4])[0]
                index_content = index_content[9 + num_bytes * 2:]
                dir_dict[directory_name] = retrieve_md5_file_name(index_content[0:16])
                index_content = index_content[40:]

            timestamp_str = str(int(time.time()))

            create_directory(extract_folder)
            create_directory(f'{extract_folder}/{timestamp_str}')

            for directory in dir_dict:
                create_directory(f'{extract_folder}/{timestamp_str}/{directory}')

                with open(glob(f'{main_folder}/{dir_dict[directory]}/container.*')[0], 'rb') as f:
                    container_content = f.read()

                num_entries = struct.unpack('<i', container_content[4:8])[0]
                container_content = container_content[8:]
                count = 1

                while num_entries >= count:
                    entry_content = container_content[0:0xa0]
                    container_content = container_content[0xa0:]

					#filenamePath = unpack(f'<{str(0x80)}s', entryContent[0:0x80])[0].replace(b'\x00', b'').replace(b'_S', b'/').decode('ascii')
                    filename_path = struct.unpack(f'<{str(0x80)}s', entry_content[0:0x80])[0].replace(b'\x00', b'').decode('ascii')
                    filename_md5 = retrieve_md5_file_name(entry_content[0x80:])

                    print(f'{filename_path} {filename_md5}')

                    array_path = filename_path.split('_S')
                    intermediary_folder = ''
                    if len(array_path) < 2:
                        filename = array_path[0]
                    else:
                        intermediary_folder = array_path[0]
                        filename = array_path[1]

                    if filename_path.endswith('.zip'):
                        shutil.copy2(f'{main_folder}/{dir_dict[directory]}/{filename_md5}.zip', f'{extract_folder}/{timestamp_str}/{directory}/{intermediary_folder}/{filename}')
                    else:
                        with open(f'{main_folder}/{dir_dict[directory]}/{filename_md5}', 'rb') as f:
                            compressed_file_content = f.read()
                            create_directory(f'{extract_folder}/{timestamp_str}/{directory}/{intermediary_folder}')

                        with open(f'{extract_folder}/{timestamp_str}/{directory}/{intermediary_folder}/{filename}', 'wb') as f:
                            f.write(zlib.decompress(compressed_file_content[4:]))

                    count += 1

if __name__ == "__main__":
    extract_files()
