import unittest

class TestSrcinfo(unittest.TestCase):

    def assertPackageNamesEqual(self, srcinfo, package_names):
        self.assertCountEqual(srcinfo['packages'].keys(), package_names)


    def testSimpleParse(self):
        from srcinfo.parse import parse_srcinfo

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

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertTrue(parsed)
        self.assertEqual(errors, [])
        self.assertPackageNamesEqual(parsed, ['ponies'])


    def testSplitPackageNames(self):
        from srcinfo.parse import parse_srcinfo

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

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertEqual(errors, [])
        self.assertPackageNamesEqual(parsed, ['applejack', 'rainbowdash', 'pinkiepie'])


    def testRejectsMultiplePkgbase(self):
        from srcinfo.parse import parse_srcinfo

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

pkgname = luna

pkgbase = ponies'''

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertPackageNamesEqual(parsed, ['luna'])
        self.assertEqual(len(errors), 1)
        self.assertIn('pkgbase declared more than once', errors[0]['error'])


    def testRejectsPkgbaseAfterPkgname(self):
        from srcinfo.parse import parse_srcinfo

        srcinfo = '''pkgname = luna
pkgbase = pony'''

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertPackageNamesEqual(parsed, ['luna'])
        self.assertEqual(len(errors), 1)
        self.assertIn('pkgbase declared after pkgname', errors[0]['error'])


    def testCoverage(self):
        from srcinfo.parse import parse_srcinfo
        from srcinfo.utils import get_variable

        srcinfo = '''pkgbase = gcc
    pkgdesc = The GNU Compiler Collection
    pkgver = 4.9.1
    pkgrel = 2
    url = http://gcc.gnu.org
    arch = i686
    arch = x86_64
    license = GPL
    license = LGPL
    license = FDL
    license = custom
    checkdepends = dejagnu
    checkdepends = inetutils
    makedepends = binutils>=2.24
    makedepends = libmpc
    makedepends = cloog
    makedepends = gcc-ada
    makedepends = doxygen
    options = !emptydirs
    source = ftp://gcc.gnu.org/pub/gcc/snapshots/4.9-20140903/gcc-4.9-20140903.tar.bz2
    source = gcc-4.8-filename-output.patch
    source = gcc-4.9-isl-0.13-hack.patch
    md5sums = 24dfd67139fda4746d2deff18182611d
    md5sums = 40cb437805e2f7a006aa0d0c3098ab0f
    md5sums = f26ae06b9cbc8abe86f5ee4dc5737da8

pkgname = gcc
    pkgdesc = The GNU Compiler Collection - C and C++ frontends
    install = gcc.install
    groups = base-devel
    depends = gcc-libs=4.9.1-2
    depends = binutils>=2.24
    depends = libmpc
    depends = cloog
    options = staticlibs

pkgname = gcc-libs
    pkgdesc = Runtime libraries shipped by GCC
    install = gcc-libs.install
    groups = base
    depends = glibc>=2.20
    options = !emptydirs
    options = !strip

pkgname = gcc-fortran
    pkgdesc = Fortran front-end for GCC
    install = gcc-fortran.install
    depends = gcc=4.9.1-2
    options = staticlibs
    options = !emptydirs

pkgname = gcc-objc
    pkgdesc = Objective-C front-end for GCC
    depends = gcc=4.9.1-2

pkgname = gcc-ada
    pkgdesc = Ada front-end for GCC (GNAT)
    install = gcc-ada.install
    depends = gcc=4.9.1-2
    options = staticlibs
    options = !emptydirs

pkgname = gcc-go
    pkgdesc = Go front-end for GCC
    install = gcc-go.install
    depends = gcc=4.9.1-2
    options = staticlibs
    options = !emptydirs'''

        expected_packages = ['gcc', 'gcc-libs', 'gcc-fortran', 'gcc-objc', 'gcc-ada', 'gcc-go']

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertEqual(errors, [])
        self.assertPackageNamesEqual(parsed, expected_packages)

        for pkgname in expected_packages:
            self.assertEqual(get_variable('pkgver', pkgname, parsed), '4.9.1')
            self.assertEqual(get_variable('pkgrel', pkgname, parsed), '2')
            self.assertEqual(get_variable('arch', pkgname, parsed), ['i686', 'x86_64'])
            self.assertEqual(get_variable('license', pkgname, parsed), ['GPL', 'LGPL', 'FDL', 'custom'])
            self.assertEqual(get_variable('url', pkgname, parsed), 'http://gcc.gnu.org')
            self.assertEqual(get_variable('makedepends', pkgname, parsed), ['binutils>=2.24','libmpc', 'cloog', 'gcc-ada', 'doxygen'])
            self.assertEqual(get_variable('checkdepends', pkgname, parsed), ['dejagnu', 'inetutils'])
            self.assertEqual(get_variable('source', pkgname, parsed), [
                'ftp://gcc.gnu.org/pub/gcc/snapshots/4.9-20140903/gcc-4.9-20140903.tar.bz2',
                'gcc-4.8-filename-output.patch',
                'gcc-4.9-isl-0.13-hack.patch'])
            self.assertEqual(get_variable('md5sums', pkgname, parsed), [
                '24dfd67139fda4746d2deff18182611d',
                '40cb437805e2f7a006aa0d0c3098ab0f',
                'f26ae06b9cbc8abe86f5ee4dc5737da8'])

        self.assertEqual(get_variable('pkgdesc', 'gcc-libs', parsed), 'Runtime libraries shipped by GCC')
        self.assertEqual(get_variable('groups', 'gcc-libs', parsed), ['base'])
        self.assertEqual(get_variable('depends', 'gcc-libs', parsed), ['glibc>=2.20'])
        self.assertEqual(get_variable('options', 'gcc-libs', parsed), ['!emptydirs', '!strip'])
        self.assertEqual(get_variable('install', 'gcc-libs', parsed), 'gcc-libs.install')

        self.assertEqual(get_variable('pkgdesc', 'gcc', parsed), 'The GNU Compiler Collection - C and C++ frontends')
        self.assertEqual(get_variable('depends', 'gcc', parsed), ['gcc-libs=4.9.1-2', 'binutils>=2.24', 'libmpc', 'cloog'])
        self.assertEqual(get_variable('groups', 'gcc', parsed), ['base-devel'])
        self.assertEqual(get_variable('options', 'gcc', parsed), ['staticlibs'])
        self.assertEqual(get_variable('install', 'gcc', parsed), 'gcc.install')

        self.assertEqual(get_variable('pkgdesc', 'gcc-fortran', parsed), 'Fortran front-end for GCC')
        self.assertEqual(get_variable('depends', 'gcc-fortran', parsed), ['gcc=4.9.1-2'])
        self.assertEqual(get_variable('options', 'gcc-fortran', parsed), ['staticlibs', '!emptydirs'])
        self.assertEqual(get_variable('install', 'gcc-fortran', parsed), 'gcc-fortran.install')
        self.assertFalse(get_variable('groups', 'gcc-fortran', parsed))

        self.assertEqual(get_variable('pkgdesc', 'gcc-objc', parsed), 'Objective-C front-end for GCC')
        self.assertEqual(get_variable('depends', 'gcc-objc', parsed), ['gcc=4.9.1-2'])
        self.assertEqual(get_variable('options', 'gcc-objc', parsed), ['!emptydirs'])
        self.assertFalse(get_variable('install', 'gcc-objc', parsed))
        self.assertFalse(get_variable('groups', 'gcc-objc', parsed))

        self.assertEqual(get_variable('pkgdesc', 'gcc-ada', parsed), 'Ada front-end for GCC (GNAT)')
        self.assertEqual(get_variable('depends', 'gcc-ada', parsed), ['gcc=4.9.1-2'])
        self.assertEqual(get_variable('options', 'gcc-ada', parsed), ['staticlibs', '!emptydirs'])
        self.assertEqual(get_variable('install', 'gcc-ada', parsed), 'gcc-ada.install')
        self.assertFalse(get_variable('groups', 'gcc-ada', parsed))

        self.assertEqual(get_variable('pkgdesc', 'gcc-go', parsed), 'Go front-end for GCC')
        self.assertEqual(get_variable('depends', 'gcc-go', parsed), ['gcc=4.9.1-2'])
        self.assertEqual(get_variable('options', 'gcc-go', parsed), ['staticlibs', '!emptydirs'])
        self.assertEqual(get_variable('install', 'gcc-go', parsed), 'gcc-go.install')
        self.assertFalse(get_variable('groups', 'gcc-go', parsed))

    def testEmptyAttrInPackageOverridesGlobal(self):
        from srcinfo.parse import parse_srcinfo
        from srcinfo.utils import get_variable

        srcinfo = '''pkgbase = pony
    depends = global

pkgname = applejack

pkgname = pinkiepie
    depends =
'''

        (parsed, errors) = parse_srcinfo(srcinfo)
        self.assertEqual(errors, [])
        self.assertCountEqual(get_variable('depends', 'pinkiepie', parsed), [])
        self.assertCountEqual(get_variable('depends', 'applejack', parsed), ['global'])


if __name__ == '__main__':
    unittest.main()
