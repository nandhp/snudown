from distutils.core import setup, Extension, Command

import unittest, sys

import os
import fnmatch

def c_files_in(directory):
    paths = []
    names = os.listdir(directory)
    for f in fnmatch.filter(names, '*.c'):
        paths.append(os.path.join(directory, f))
    return paths

class RunTests(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    # From disttest, copyright (c) 2010 Jared Forsyth, MIT license
    # https://github.com/jabapyth/disttest/blob/master/disttest.py
    def with_project_on_sys_path(self, func):
        self.run_command('build')
        cmd = self.get_finalized_command('build_py')

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        from os.path import normpath as normalize_path

        try:
            sys.path.insert(0, normalize_path(cmd.build_lib))
            func()
        finally:
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)

    def run(self):
        self.with_project_on_sys_path(self.run_tests)

    def run_tests(self):
        import snudown_tests
        suite = unittest.TestLoader().loadTestsFromModule(snudown_tests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

setup(
    name='snudown',
    version='1.0.5',
    author='Vicent Marti',
    author_email='vicent@github.com',
    license='MIT',
    ext_modules=[
        Extension(
            name='snudown', 
            sources=['snudown.c'] + c_files_in('src/') + c_files_in('html/'),
            include_dirs=['src', 'html']
        )
    ],
    cmdclass = {'test': RunTests},
)
