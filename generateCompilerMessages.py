#!/usr/bin/env python

from __future__ import print_function
from subprocess import Popen, PIPE
import sys
import os


###############################################
###############################################
## USER CONFIGURATION OPTIONS

# compiler command to use, source code filename will be appended
compiler = 'g++ -Wall'

# the language is use (This needs to correspond to a language supported by the LaTeX listings package)
lang = 'C++'

# filename extension used for temporary source files
source_filename_extension = '.cpp'

# whether the output should be in LaTeX or plain text (True / False)
output_latex = True
###############################################
###############################################


###############################################
def main():
        if len(sys.argv) < 2:
                usage()
	else:
		source_lines = get_lines(sys.argv[1])
		
		check_no_error_compile()
		
		if output_latex:
			processor = latex_processor()
		else:
			processor = plaintext_processor()
		
		processor.header()
		processor.include_file(source_lines, sys.argv[1])
		for i in range(0, len(source_lines)):
			if source_lines[i] == '\n': continue
			process_code(source_lines[i], source_lines[:i] + source_lines[i+1:], i, processor)

		processor.footer()

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
def process_code(commented_line, source, line_number, processor):
	
	tempfilename = 'tempfile' + source_filename_extension
	f = open(tempfilename, 'w')
	for l in source:
		f.write(l + '\n')
	f.close()

	cmd = compiler + ' ' + tempfilename

	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	
	processor.section(commented_line.strip(), int(line_number + 1))
	
	if stderr:
		processor.compile_error(stderr)
	else:
		processor.no_problem()

###############################################
def usage():
        print('Usage: generateCompilerMessages.py source.cpp', file=sys.stderr)

###############################################
###############################################
###############################################
class latex_processor():

	special_chars = ['#', '%', '{', '}']

	def latex_command(self, command, text):
		text = text.strip()
		for c in self.special_chars:
			text = text.replace(c, '\\' + c)
		res = '\\%s{%s}' % (command, text)
		print(res)


	###############################################
	def include_file(self, source_lines, source_filename):
		self.latex_command('begin', 'center')
		self.latex_command('large', 'Original Source')
		self.latex_command('end', 'center')
		self.latex_command('lstset', 'numbers=left')
		self.latex_command('lstinputlisting[language=%s]' % lang, source_filename)
		print('\\newpage')	

	###############################################
	def header(self, ):
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
	def footer(self, ):
		res = '\end{document}'
		print(res)

	###############################################
	def compile_error(self, text):
		self.latex_command('begin', 'verbatim')
		print(text)
		self.latex_command('end', 'verbatim')
		print('\n')

	###############################################
	def no_problem(self, ):
		print('No Warnings or Errors')
	
	###############################################
	def section(self, name, line_number):
		section_name = '%s [Line %d]' % (name, line_number)
		self.latex_command('section', section_name)

###############################################
###############################################
###############################################

class plaintext_processor():

	###############################################
	def include_file(self, source_lines, source_filename):
		print('Original Source:')
		for l in source_lines:
			print(l)
		print('\n')	

	###############################################
	def header(self, ):
		res = 'Iterative Line Removal: Compiler Output Messages using %s\n\n'
		print(res % compiler)

	###############################################
	def footer(self, ):
		pass

	###############################################
	def compile_error(self, text):
		print(text)
		

	###############################################
	def no_problem(self, ):
		print('No Warnings or Errors')
	
	###############################################
	def section(self, name, line_number):
		print('Line %d: \t %s : ' % (line_number, name))

if __name__ == '__main__': main()

