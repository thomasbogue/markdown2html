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

# converts the specified markdown file into html
# htmlFilename defaults to the same as the input filename, but with the
# extension changed to .html
def convert_markdown(markdownFilename, htmlFilename=""):
  infile = codecs.open(markdownFilename, encoding='utf-8')
  if htmlFilename == "":
    outfilename = re.sub(r'.md$', '.html', markdownFilename)
  else:
    outfilename = htmlFilename
  outfile = codecs.open(outfilename, 'w', encoding='utf-8')
  outfile.write("<html><head><title>" + markdownFilename+ "</title></head><body>\n")
  previousIndentLevel = 0
  lastrowTable = False
  codeBlock = False
  for line in infile:
    # skip blank lines
    if len(line.strip()) == 0:
      continue
    firstchar = line.strip()[0]
    if re.match(r"```.*", line.strip()): # ''' means start or stop code block
      if (codeBlock): # end the code block
          outfile.write("</code></pre>")
      else: # start the code block
          line = re.sub(r'```(.*)', r"<emph>\1</emph><br/><pre><code>", line.strip())
          outfile.write(line)
      codeBlock = not codeBlock
      continue
    # look for tables
    if (not codeBlock): # don't apply rules to lines in code blocks
      if firstchar == '|':
        if not lastrowTable:
          outfile.write("<table>\n")
        lastrowTable = True
        if re.match(r'^[-|]+$', line.strip()):
          # not sure how to format hrules -- skipping
          print("skipping hrule")
          continue
        else:
          line = line.strip()
          line = re.sub(r"^\|", "<tr><td>", line)
          line = re.sub(r"\|$", "</td></tr>", line)
          line = line.replace("|", "</td><td>")
          outfile.write(line + "\n")
          continue
      else:
          if lastrowTable:
              lastrowTable = False
              outfile.write("</table>\n")
      # look for header lines, ignore indents for them
      if firstchar == '#':
          headernum = 0
          while line.strip()[headernum] == '#':
              headernum = headernum + 1
          outfile.write("<h" + str(headernum) + ">" + line.strip().replace("#","") + "</h" + str(headernum) + ">\n")
          continue
      # don't process things that look like tags
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
      line = re.sub(r'!\[(.+)\]\((.+)\)', r'<img alt="\1" src="\2"></img>', line)
      if not line.find("["):
          line = re.sub(r'[-*](.+)[-*]', r'<emph>\1</emph>',line)
      previousIndentLevel = indentLevel
    outfile.write(line)
  outfile.write("</body>")
  outfile.close()
  infile.close()
