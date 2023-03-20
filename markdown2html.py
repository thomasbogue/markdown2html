import sys
import codecs
import re

def indentLevelOfLine(line):
  indent = 0
  for c in line:
    if c == ' ':
      indent = indent + 1
    elif c == '\t':
      indent = indent + 5
    else:
      return(indent)
  # if there is nothing but whitespace in the line, return 0
  return(0)

if len(sys.argv) <= 1:
    print("usage: " + sys.argv[0] + " markdownfilename.md [...]")
    print("converts the selected markdown files to approximate html")
    exit(-1)

for filename in sys.argv[2:]:
  infile = codecs.open(filename, encoding='utf-8')
  outfilename = re.sub(r'.md$', '.html', filename)
  outfile = codecs.open(outfilename, 'w', encoding='utf-8')
  outfile.write("<html><head><title>" + filename + "</title></head><body>\n")
  previousIndentLevel = 0
  for line in infile:
    # skip blank lines
    if len(line.strip()) == 0:
        continue
    firstchar = line.strip()[0]
    # look for header lines, ignore indents for them
    if firstchar == '#':
        headernum = 0
        while line.strip()[headernum] == '#':
            headernum = headernum + 1
        outfile.write("<h" + str(headernum) + ">" + line.strip().replace("#","") + "</h" + str(headernum) + ">\n")
        continue
    if line.strip()[0] == '<':
        outfile.write(line)
        continue
    indentLevel = indentLevelOfLine(line)
    if indentLevel > previousIndentLevel:
        outfile.write("<ol>")
    if indentLevel < previousIndentLevel:
        outfile.write("</ol>\n")
    if line.strip()[0] == '*':
        line = line.strip()[1:]
        line = "<li>" + line + "</li>\n"
    line = re.sub(r'[-*][-*](.*)[-*][-*]', r'<strong>\1</strong>', line)
    line = re.sub(r'([^!])\[(.+)\]\((.+)\)', r'\1<a href="\3">\2</a>', line)
    line = re.sub(r'!\[(.+)\]\((.+)\)', r'<img src="\1"></img>', line)
    if not line.find("["):
        line = re.sub(r'[-*](.+)[-*]', r'<emph>\1</emph>',line)
    outfile.write(line)
    previousIndentLevel = indentLevel
  outfile.write("</body>")
  outfile.close()
  infile.close()
