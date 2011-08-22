#!/usr/bin/env python

from __future__ import print_function
from subprocess import Popen, PIPE
import sys
import os


###############################################

## USER CONFIGURATION OPTIONS

# compiler command to use, source code filename will be appended
compiler = 'g++ -Wall'

# the language is use (This needs to correspond to a language supported by the LaTeX listings package
lang = 'C++'

# filename extension used for temporary source files
source_filename_extension = '.cpp'

## 

###############################################

special_chars = ['#', '%', '{', '}']

###############################################

def main():
        if len(sys.argv) < 2:
                usage()
	else:
		source_lines = get_lines(sys.argv[1])
		
		check_no_error_compile()
		
		latex_header()
		include_original_source(source_lines, sys.argv[1])
		for i in range(0, len(source_lines)):
			if source_lines[i] == '\n': continue
			process_code(source_lines[i], source_lines[:i] + source_lines[i+1:], i)

		latex_footer()

###############################################

def check_no_error_compile():
	cmd = compiler + ' ' + sys.argv[1]
	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	if stderr:
		print('ERROR: The unmodified source compiles with warnings or errors!', file=sys.stderr)
		for line in stdout:
			print(line)
		sys.exit(1)

###############################################

def include_original_source(source_lines, source_filename):
	latex_command('begin', 'center')
	latex_command('large', 'Original Source')
	latex_command('end', 'center')
	latex_command('lstset', 'numbers=left')
	latex_command('lstinputlisting[language=%s]' % lang, source_filename)
	print('\\newpage')

###############################################

def get_lines(filename):
	res = []
	try:
		f = open(filename, 'r')
		res = f.readlines()
		if not res:
			print('ERROR: Empty Source File!', file=sys.stderr)
			sys.exit(1)
	except IOError as error:
		print(error)
	return res

###############################################

def process_code(commented_line, source, line_number):
	tempfilename = 'tempfile' + source_filename_extension
	f = open(tempfilename, 'w')
	for l in source:
		f.write(l + '\n')
	f.close()

	cmd = compiler + ' ' + tempfilename

	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	
	section_name = commented_line.strip() + ' [Line %d]' % int(line_number + 1)
	latex_command('section', section_name)
	
	if stderr:
		latex_command('begin', 'verbatim')
		print(stderr)
		latex_command('end', 'verbatim')
		print('\n\n')
	else:
		print('No Warnings or Errors')
		print('\n\n')

###############################################

def usage():
        print('Usage: generateCompilerMessages.py source.cpp', file=sys.stderr)

###############################################

def latex_header():
	res = '''
\\documentclass{article}

\\usepackage[pdftex, pdfusetitle, colorlinks, urlcolor=blue,]{hyperref}
\\usepackage{listings}

\\author{generateCompilerMessages.py}
\\title{Iterative Line Removal: Compiler Output Messages using %s}

\\begin{document}
\\maketitle
\\tableofcontents
\\newpage
		'''
	print(res % compiler)

###############################################
	
def latex_footer():
	res = '\end{document}'
	print(res)

###############################################

def latex_command(command, text):
	text = text.strip()
	for c in special_chars:
		text = text.replace(c, '\\' + c)
	res = '\\%s{%s}' % (command, text)
        print(res)

###############################################

if __name__ == '__main__': main()

