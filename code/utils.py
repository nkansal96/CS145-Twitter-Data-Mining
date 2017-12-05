from difflib import SequenceMatcher

def lcs(a, b):
	s = SequenceMatcher(None, a, b)
	return s.find_longest_match(0, len(a), 0, len(b)).size