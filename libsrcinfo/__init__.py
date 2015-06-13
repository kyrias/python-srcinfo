from .parse import parse_srcinfo

##
# Get a specific variable for a package, falling back to the global one if no
# package-specific version exists
#
# Arguments:
#   variable:   Variable to find
#   package:    Package to look up variable for
#   info:       Dict to look up in
#
def get_variable(variable, package, info):
    if package and package in info['packages']:
        package = info['packages'][package]
        if variable in package:
            return package[variable]

    if variable in info:
        return info[variable]

    else:
        return None

##
# If executed, parse SRCINFO from stdin and print parsed info
#
if __name__ == '__main__':
    import pprint
    import sys

    srcinfo = sys.stdin.read()
    info = parse_srcinfo(srcinfo)
    pprint.PrettyPrinter().pprint(info)
