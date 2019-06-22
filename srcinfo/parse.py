from parse import parse

arrays = ['pkgname', 'arch', 'license', 'groups', 'options',
          'conflicts', 'provides', 'replaces',
          'source', 'noextract', 'backup', 'validpgpkeys', 'b2sums', 'md5sums',
          'sha1sums', 'sha224sums', 'sha256sums', 'sha384sums', 'sha512sums',
          'depends', 'makedepends', 'checkdepends', 'optdepends',
          ]


##
# Check if SRCINFO key is an array
#
def is_array(key):
    if key in arrays:
        return True
    return False


##
# Insert `value` into the list index `key` in list `target`
#
def list_insert(target, key, value):
    if key not in target:
        target[key] = []

    # Don't append value if already in the list
    if value and value not in target[key]:
        target[key].append(value)


##
# Extract a SRCINFO variable from `string`
#
def extract_var(string):
    line = string.lstrip()
    if line.startswith('#'):
        return (None, None, None)

    key = None
    value = None
    errors = []

    def value(string):
        return string.strip()
    value.pattern = r'.*'

    parsed = parse('{:^}={:value}', line, dict(value=value))
    if parsed:
        (key, value) = parsed
    else:
        errors.append('failed to parse line: {!r}'.format(line))

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

        (key, value, err) = extract_var(line)

        if err:
            errors.append({
                'line': index,
                'error': err
            })

        if key == 'pkgbase':
            if 'pkgbase' in srcinfo:
                errors.append({
                    'line': index,
                    'error': "pkgbase declared more than once",
                })

            elif info != srcinfo:
                errors.append({
                    'line': index,
                    'error': "pkgbase declared after pkgname",
                })

        if key == 'pkgname':
            pkgname = value
            info = srcinfo['packages'][pkgname] = {}
            continue

        elif not key:
            continue

        if is_array(key):
            list_insert(info, key, value)
        else:
            info[key] = value

    return (srcinfo, errors)
