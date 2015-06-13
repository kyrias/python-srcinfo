from srcinfo.parse import parse_srcinfo
import sys

##
# Parse SRCINFO from stdin and pretty-print parsed info
#
def main():
    import pprint
    import sys

    srcinfo = sys.stdin.read()
    (info, errors) = parse_srcinfo(srcinfo)

    pprint.PrettyPrinter().pprint(info)
    if errors:
        print('==> The following errors occured while parsing:', file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
