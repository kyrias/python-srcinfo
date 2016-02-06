from parse import parse

arrays = ['pkgname', 'arch', 'license', 'groups', 'options',
          'conflicts', 'provides', 'replaces',
          'source', 'noextract', 'backup', 'validpgpkeys', 'md5sums',
          'sha1sums', 'sha224sums', 'sha256sums', 'sha384sums', 'sha512sums',
          'depends', 'makedepends', 'checkdepends', 'optdepends',
          ]


def remove_empty_values(values):
    return [v for v in values if v.strip()]


##
# Check if SRCINFO key is an array
#
def is_array(key):
    if key in arrays:
        return True
    for array in arrays:
        if key.startswith(array):
            return True
    return False


##
# Insert `value` into the list index `key` in list `target`
#
def list_insert(target, key, value):
    if key not in target:
            target[key] = []

    # Don't append value if already in the list
    if value not in target[key]:
        if value:
            target[key].append(value)


##
# Extract a SRCINFO variable from `string`
#
def extract_var(string):
    line = string.lstrip()
    key = None
    value = None
    errors = []

    parsed = parse('{} ={}', line)
    if parsed:
        (key, value) = parsed
        key = key.strip()
        value = value.strip()

    elif line.startswith('#'):
        pass

    else:
        errors.append('failed to parse line: "{}"'.format(line))

    return (key, value, errors)


##
# Parse SRCINFO from string
#
# Returns a tuple of the srcinfo dict and an list of any errors found while
# parsing
#
def parse_srcinfo(source):
    lines = source.splitlines()

    srcinfo = {'packages': {}}
    info = srcinfo
    errors = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        if line.startswith('pkgname'):
            pkgname = line.split('pkgname =')[1].strip()
            info = srcinfo['packages'][pkgname] = {}
            continue

        (key, value, err) = extract_var(line)
        if err:
            errors.append({
                'line': index,
                'error': err
            })

        if not key:
            continue

        if is_array(key):
            list_insert(info, key, value)
        else:
            info[key] = value

    return (srcinfo, errors)
