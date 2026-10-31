from re import compile
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_SOFTWARE = 70
EXIT_INTERRUPTED = 130


class PaperCountComputing:
	__PrefixPattern = compile("^(-|[1-9][0-9]*[).]) ")
	@staticmethod
	def __split(line:str) -> tuple:
		if isinstance(line, str):
			sanitizedLine = "".join(character for character in line.strip() if ' ' <= character <= '~')
			match = PaperCountComputing.__PrefixPattern.match(sanitizedLine)
			prefix, body = ("", sanitizedLine) if match is None else (match.group(0), sanitizedLine[match.end():])
			lastStarIndex = body.rfind("*")
			if lastStarIndex >= 1:
				try:
					count = int(body[lastStarIndex + 1:].strip())
					if count >= 0:
						return (prefix, body[:lastStarIndex].strip(), count)
					else: # treat the whole body as a venue
						return (prefix, body.strip(), 1)
				except ValueError: # treat the whole body as a venue
					return (prefix, body.strip(), 1)
			else: # treat the whole body as a venue
				return (prefix, body.strip(), 1)
		else:
			return (None, None, None)
	@staticmethod
	def computePaperCount(lines:tuple|list|set) -> tuple:
		if isinstance(lines, (tuple, list, set)):
			prefixMappings, venueMappings, flag = {}, {}, False
			for line in lines:
				prefix, venue, count = PaperCountComputing.__split(line)
				if isinstance(prefix, str) and isinstance(venue, str) and venue and isinstance(count, int) and count >= 0:
					if prefix:
						prefixMappings.setdefault(prefix, 0)
						prefixMappings[prefix] += 1
					if venue in venueMappings:
						flag = True # repeated venue
						venueMappings[venue] += count
					else:
						venueMappings[venue] = count
					if 0 == count:
						flag = True # zero-count venue
			for key in tuple(venueMappings.keys()): # Remove zero-count venues
				if not venueMappings[key]:
					del venueMappings[key]
			return (venueMappings, max(prefixMappings, key = lambda prefix:prefixMappings[prefix], default = "- ") if flag else None)
		else:
			return (None, None)


def main() -> int:
	try:
		print("Please paste the venues line-by-line here, using \" * \" to connect a venue with the corresponding count. ")
		lines = []
		try:
			while True:
				line = input()
				if line:
					lines.append(line)
				else:
					break
		except KeyboardInterrupt:
			print()
		venueMappings, preferredPrefix = PaperCountComputing.computePaperCount(lines)
		if isinstance(venueMappings, dict):
			if preferredPrefix:
				if venueMappings:
					print("Repeated or zero-count venues found, please consider replacing the original lines with the following ones. ")
					for key, value in venueMappings.items():
						print("{0}{1} * {2}".format(preferredPrefix, key, value))
					print()
				else:
					print("All venues are zero-count. ")
			paperCount, venueCount = sum(venueMappings.values()), len(venueMappings)
			print("There {0} {1} paper{2} in {3} venue{4}. ".format("is" if 1 == paperCount else "are", paperCount, "" if 1 == paperCount else "s", venueCount, "" if 1 == venueCount else "s"))
			exitStatus = EXIT_SUCCESS
		else:
			print("Failed to compute the paper count. ")
			exitStatus = EXIT_FAILURE
	except KeyboardInterrupt:
		print()
		print("The computing process was interrupted by users. ")
		exitStatus = EXIT_INTERRUPTED
	except BaseException as e:
		print()
		print("The computing process was interrupted by {0}. ".format(repr(e)))
		exitStatus = EXIT_SOFTWARE
	print("Please press the enter key to exit ({0}). ".format(exitStatus))
	try:
		input()
	except:
		print()
	return exitStatus



if "__main__" == __name__:
	exit(main())