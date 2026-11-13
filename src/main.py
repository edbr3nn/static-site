import sys
from copystatic import setup_public_dir, copy_files_recursive
from gencontent import generate_pages_recursive

static = "static/"
public = "public/"
docs = "docs/"

def main():
    basepath = "/static-site/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    setup_public_dir(docs)
    copy_files_recursive(static, docs)
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
