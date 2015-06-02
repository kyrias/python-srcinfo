def package_names_equal(srcinfo, package_names):
    return set(srcinfo['packages'].keys()) == set(package_names)


def test_simple_parse():
    from libsrcinfo.parse import parse_srcinfo

    srcinfo = '''pkgbase = ponies
    pkgdesc = Some description
    pkgver = 1.0.0
    pkgrel = 1
    url = https://example.com
    arch = i686
    arch = x86_64
    license = ISC
    source = git+https://example.com/package.git
    md5sums = SKIP

pkgname = ponies'''

    parsed = parse_srcinfo(srcinfo)
    assert parsed
    assert package_names_equal(parsed, ['ponies'])



def test_split_package_names():
    from libsrcinfo.parse import parse_srcinfo

    srcinfo = '''pkgbase = pony
    pkgdesc = Some description
    pkgver = 1.0.0
    pkgrel = 1
    url = https://example.com
    arch = i686
    arch = x86_64
    license = ISC
    source = git+https://example.com/package.git
    md5sums = SKIP

pkgname = applejack

pkgname = rainbowdash

pkgname = pinkiepie'''

    parsed = parse_srcinfo(srcinfo)
    assert package_names_equal(parsed, ['applejack', 'rainbowdash', 'pinkiepie'])
