from srcinfo.parse import parse_srcinfo
import sys


##
# Parse SRCINFO from stdin and pretty-print parsed info
#
def main():
    output_json = len(sys.argv) > 1 and sys.argv[1] == "--json"

    srcinfo = sys.stdin.read()
    (info, errors) = parse_srcinfo(srcinfo)

    if output_json:
        if errors:
            sys.exit(1)
        else:
            import json
            print(json.dumps(info))
    else:
        import pprint
        pprint.PrettyPrinter().pprint(info)
        if errors:
            print('==> The following errors occured while parsing:', file=sys.stderr)
            for error in errors:
                print(error, file=sys.stderr)
