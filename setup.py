from setuptools import find_packages, setup

package_name = 'dialoger'
version = '1.3.0'

setup(
    name=package_name,
    packages=find_packages(),
    version=version,
    include_package_data=True,
    package_data={
        'dialoger': ['images/*'],
    },
    description='A package that provides a simple and user-friendly interface for creating interactive windows in Tkinter. Provides functions to create input windows, option list windows, alerts, information, errors and confirmation windows with options. Simplify user interaction with your program quickly and efficiently. One of the main functions is that it is possible to use patterns for certain answers, which allows requiring the user to have a date pattern, or input of numbers.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Guilherme Saldanha',
    author_email='guisaldanha@gmail.com',
    url='https://github.com/guisaldanha/dialoger',
    license='MIT',
    keywords=['tkinter', 'dialog', 'dialoger', 'dialogbox', 'dialogboxer', 'dialoguer', 'dialoguerbox', 'box', 'user interface', 'interactive', 'input', 'choices', 'alert', 'information', 'error', 'confirmation', 'easy-to-use', 'efficiency', 'user-friendly', 'pattern', 'date', 'number', 'date pattern', 'number pattern', 'pattern input', 'pattern input date', 'pattern input number'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.11',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
)
