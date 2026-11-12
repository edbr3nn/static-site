from copystatic import setup_public_dir, copy_files_recursive
from gencontent import generate_pages_recursive

static = "static/"
public = "public/"

def main():
    setup_public_dir(public)
    copy_files_recursive(static, public)
    generate_pages_recursive("content", "template.html", "public")

main()
