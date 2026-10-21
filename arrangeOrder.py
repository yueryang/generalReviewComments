from os import chdir
from os.path import abspath, dirname
from sys import argv, exit
from time import sleep
try:
	chdir(abspath(dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_SOFTWARE = 70
EXIT_INTERRUPTED = 130


class Node:
	def __init__(self:object, parent:object|None = None) -> object:
		self.__content, self.__children, self.__parent = "", [], parent
	def addContent(self:object, content:str) -> bool:
		if isinstance(content, str):
			self.__content += content
			return True
		else:
			return False
	def addChild(self:object) -> object:
		child = Node(parent = self)
		self.__children.append(child)
		return child
	def getParent(self:object) -> object|None:
		return self.__parent
	def __str__(self:object) -> str:
		self.__children.sort(key = lambda x:x.__content)
		return "{0}{1}".format(self.__content, "".join(str(child) for child in self.__children))

class Arranger:
	def __init__(self:object, inputFilePath:str, outputFilePath:str) -> object:
		self.__inputFilePath, self.__outputFilePath, self.__root = inputFilePath, outputFilePath, None
	def __countLevel(self:object, line:str) -> int:
		if isinstance(line, str):
			level = 0
			for ch in line:
				if "#" == ch:
					level += 1
				else:
					break
			return level
		else:
			return -1
	def __getFence(self:object, line:str) -> tuple|None:
		if not isinstance(line, str):
			return None
		content = line.lstrip(" ")
		if len(line) - len(content) > 3 or not content or content[0] not in ("`", "~"):
			return None
		marker, length = content[0], 0
		while length < len(content) and marker == content[length]:
			length += 1
		if length < 3:
			return None
		remainder = content[length:]
		if "`" == marker and "`" in remainder:
			return None
		return marker, length, remainder
	def load(self:object, encoding:str = "utf-8") -> bool:
		try:
			with open(self.__inputFilePath, "r", encoding = encoding) as f:
				content = f.read()
		except Exception as e:
			print("Failed to load {0} due to {1}. ".format(repr(self.__inputFilePath), repr(e)))
			return False
		self.__root, nodeLevel = Node(), 0
		fenceMarker, fenceLength = None, 0
		node = self.__root
		for line in content.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
			fence = self.__getFence(line)
			if fenceMarker is None:
				if fence is None:
					level = self.__countLevel(line)
				else:
					fenceMarker, fenceLength = fence[0], fence[1]
					level = 0
			else:
				level = 0
				if fence is not None and fenceMarker == fence[0] and fenceLength <= fence[1] and not fence[2].strip():
					fenceMarker, fenceLength = None, 0
			if level >= 1:
				if nodeLevel < level:
					while nodeLevel < level:
						node = node.addChild()
						nodeLevel += 1
				else:
					while nodeLevel > level:
						node = node.getParent()
						nodeLevel -= 1
					node = node.getParent().addChild()
			node.addContent(line + "\n")
		print("Successfully loaded {0}. ".format(repr(self.__inputFilePath)))
		return True
	def dump(self:object, encoding:str = "utf-8") -> bool:
		try:
			with open(self.__outputFilePath, "w", encoding = encoding) as f:
				f.write(str(self.__root)[:-1])
			print("Successfully wrote to {0}. ".format(repr(self.__outputFilePath)))
			return True
		except Exception as e:
			print("Failed to write to {0} due to {1}. ".format(repr(self.__outputFilePath), repr(e)))
			return False

def main() -> int:
	# Parameters #
	warningTime = 3
	
	# Arrangement #
	try:
		argc = len(argv)
		if argc >= 3:
			arranger = Arranger(argv[1], argv[2])
			exitStatus = EXIT_SUCCESS if arranger.load() and arranger.dump() else EXIT_FAILURE
		elif 2 == argc:
			print("The script will process the file in place within {0} second(s). ".format(warningTime))
			sleep(warningTime)
			arranger = Arranger(argv[1], argv[1])
			exitStatus = EXIT_SUCCESS if arranger.load() and arranger.dump() else EXIT_FAILURE
		else:
			print("Nothing to handle. Please use the command line to specify the input and output files. ")
			exitStatus = EXIT_FAILURE
	except KeyboardInterrupt:
		print()
		print("The arranging process was interrupted by users. ")
		exitStatus = EXIT_INTERRUPTED
	except BaseException as e:
		print()
		print("The arranging process was interrupted by {0}. ".format(repr(e)))
		exitStatus = EXIT_SOFTWARE
	
	# Exit #
	print("Please press the enter key to exit ({0}). ".format(exitStatus))
	try:
		input()
	except:
		print()
	return exitStatus



if "__main__" == __name__:
	exit(main())