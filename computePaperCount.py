EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class PaperCountComputing:
	@staticmethod
	def computePaperCount(lines:tuple|list|set) -> int:
		if isinstance(lines, (tuple, list, set)):
			paperCount = 0
			for line in lines:
				if line:
					paperCount += int(line.split(" * ")[1].split(" ")[0], 0) if " * " in line else 1
			return paperCount
		else:
			return EOF


def main() -> int:
	try:
		print("Paste the journals and conferences your have reviewed here compressed by \" * \". ")
		lines = []
		while True:
			line = input()
			if line:
				lines.append(line)
			else:
				break
		paperCount = PaperCountComputing.computePaperCount(lines)
		if 1 == paperCount:
			print("You have reviewed 1 paper. ")
			errorLevel = EXIT_SUCCESS
		elif paperCount >= 0:
			print("You have reviewed {0} papers. ".format(paperCount))
			errorLevel = EXIT_SUCCESS
		else:
			print("Failed to compute the paper count due to Code {0}. ".format(paperCount))
			errorLevel = EXIT_FAILURE
	except BaseException as e:
		print("Failed to compute the paper count due to {0}. ".format(repr(e)))
		errorLevel = EOF
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel))
		input()
	except:
		print()
	return errorLevel



if "__main__" == __name__:
	exit(main())