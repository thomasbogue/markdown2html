import sys
import markdownConverter

if len(sys.argv) <= 1:
    print("usage: " + sys.argv[0] + " markdownfilename.md [...]")
    print("approximately converts the selected markdown files to html")
    exit(-1)

for filename in sys.argv[1:]:
  markdownConverter.convert_markdown(filename)
