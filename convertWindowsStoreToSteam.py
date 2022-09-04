#!/usr/bin/python

import re
from os import mkdir, path
from sys import exit
from zlib import decompress
from struct import unpack
from datetime import date
from time import time
from glob import glob

savePath = './windowsStoreSave'

def retrieveMd5FileName(content):
	return (content[0:4][::-1].hex() + \
			content[4:6][::-1].hex() + \
			content[6:8][::-1].hex() + \
			content[8:16].hex()).upper()

def main():
	for mainFolder in glob(f'{savePath}/wgs/*'):
		extractFolder = mainFolder.replace('wgs/', '')

		with open(f'{mainFolder}/containers.index', 'rb') as f:
			indexMatch = re.findall(re.compile(rb'\x00{4}\x10\x00{4}(.*?)$', re.MULTILINE|re.DOTALL), f.read())
		
		dirArray = {}

		if indexMatch is not None:
			indexContent = indexMatch[0]
			
			while len(indexContent) > 0:
				numBytes = unpack('<i', indexContent[0:4])[0]
				indexContent = indexContent[4:]

				directoryName = unpack(f'<{str(numBytes * 2)}s', indexContent[0:numBytes * 2])[0].replace(b'\x00', b'').decode('ascii')
				indexContent = indexContent[numBytes * 4 + 4:]

				numBytes = unpack('<i', indexContent[0:4])[0]
				indexContent = indexContent[9 + numBytes * 2:]

				dirArray[directoryName] = retrieveMd5FileName(indexContent[0:16])
				indexContent = indexContent[40:]

			timestampStr = str(int(time()))

			if not path.isdir(extractFolder):
				mkdir(extractFolder)

			try: 
				mkdir(f'{extractFolder}/{timestampStr}')
			except FileExistsError:
				exit(f'The directory {timestampStr} already exists!')

			for directory in dirArray:
				try:
					mkdir(f'{extractFolder}/{timestampStr}/{directory}')
				except FileExistsError:
					exit(f'The directory {extractFolder}/{timestampStr}/{directory} already exists!')

				with open(glob(f'{mainFolder}/{dirArray[directory]}/container.*')[0], 'rb') as f:
					containerContent = f.read()

				numEntries = unpack('<i', containerContent[4:8])[0]
				containerContent = containerContent[8:]
				cpt = 1
				while numEntries >= cpt:
					entryContent = containerContent[0:0xa0]
					containerContent = containerContent[0xa0:]
					
					#filenamePath = unpack(f'<{str(0x80)}s', entryContent[0:0x80])[0].replace(b'\x00', b'').replace(b'_S', b'/').decode('ascii')
					filenamePath = unpack(f'<{str(0x80)}s', entryContent[0:0x80])[0].replace(b'\x00', b'').decode('ascii')
					filenameMd5 = retrieveMd5FileName(entryContent[0x80:])

					print(f'{filenamePath} {filenameMd5}')

					with open(f'{mainFolder}/{dirArray[directory]}/{filenameMd5}', 'rb') as f:
						compressedFileContent = f.read()

					arrayPath = filenamePath.split('_S')
					intermediaryFolder = ''
					if len(arrayPath) < 2:
						filename = arrayPath[0]
					else:
						intermediaryFolder = arrayPath[0]
						filename = arrayPath[1]
						if not path.isdir(f'{extractFolder}/{timestampStr}/{directory}/{intermediaryFolder}'):
							mkdir(f'{extractFolder}/{timestampStr}/{directory}/{intermediaryFolder}')

					with open(f'{extractFolder}/{timestampStr}/{directory}/{intermediaryFolder}/{filename}', 'wb') as f:
						f.write(decompress(compressedFileContent[4:]))

					cpt += 1

if __name__ == "__main__":
	main()
