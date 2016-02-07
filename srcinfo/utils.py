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
# Return the info for a single package
#
def get_merged_package(package, srcinfo):
    if not package in srcinfo['packages']:
        return None

    merged = srcinfo.copy()
    package_info = merged['packages'][package]
    for key in package_info:
        merged[key] = package_info[key]

    merged.pop('packages')
    merged['pkgname'] = package

    return merged


##
# Get a list of package names
#
def get_package_names(info):
    return [p for p in info['packages'].keys()]
