from .parse import parse_srcinfo

##
# Get a specific variable for a package, falling back to the global one if no
# package-specific version exists
#
# Arguments:
#   variable:   Variable to find
#   package:    Package to look up variable for
#   info:       Global list to fall back to
#
def get_variable(variable, package, info):
    if variable in info['packages'][package]:
        return info['packages'][package][variable]
    elif variable in info:
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
