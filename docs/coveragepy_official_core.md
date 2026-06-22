# TÀI LIỆU CỐT LÕI (Rút gọn từ coveragepy_official.pdf)

> **Tổng quan**: Giữ lại 128 trang, lọc bỏ 5 trang dư thừa (changelog, index, license...).

Coverage.py
Release 7.2.2
unknown
Mar 16, 2023

ii

Coverage.py, Release 7.2.2
Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts
of the code have been executed, then analyzes the source to identify code that could have been executed but was not.
Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are
being exercised by tests, and which are not.
The latest version is coverage.py 7.2.2, released March 16, 2023. It is supported on:
• Python versions 3.7 through 3.12.0a6.
• PyPy3 7.3.11.

Coverage.py, Release 7.2.2

CHAPTER
ONE
FOR ENTERPRISE
Available as part of the Tidelift Subscription. Coverage and thousands of other packages are working with Tidelift to
deliveroneenterprisesubscriptionthatcoversalloftheopensourceyouuse. Ifyouwanttheflexibilityofopensource
and the confidence of commercial-grade software, this is for you. Learn more.

Coverage.py, Release 7.2.2
4 Chapter 1. For Enterprise

CHAPTER
TWO
QUICK START
Getting started is easy:
1. Install coverage.py:
$ python3 -m pip install coverage
For more details, seeInstallation.
2. Use coverage run to run your test suite and gather data. However you normally run your test suite, you can
use your test runner under coverage.
Tip: If your test runner command starts with “python”, just replace the initial “python” with “coverage run”.
python something.py becomes coverage run something.py
python -m amodule becomes coverage run -m amodule
Other instructions for specific test runners:
• pytest
If you usually use:
$ pytest arg1 arg2 arg3
then you can run your tests under coverage with:
$ coverage run -m pytest arg1 arg2 arg3
Many people choose to use the pytest-cov plugin, but for most purposes, it is unnecessary.
• unittest
Change “python” to “coverage run”, so this:
$ python -m unittest discover
becomes:
$ coverage run -m unittest discover
To limit coverage measurement to code in the current directory, and also find files that weren’t executed at all,
add the--source=.argument to your coverage command line.
3. Use coverage report to report on the results:

Coverage.py, Release 7.2.2
$ coverage report -m
Name Stmts Miss Cover Missing
-------------------------------------------------------
my_program.py 20 4 80% 33-35, 39
my_other_module.py 56 6 89% 17-23
-------------------------------------------------------
TOTAL 76 10 87%
4. For a nicer presentation, usecoverage html to get annotated HTML listings detailing missed lines:
$ coverage html
Then open htmlcov/index.html in your browser, to see a report like this.
6 Chapter 2. Quick start

CHAPTER
THREE
CAPABILITIES
Coverage.py can do a number of things:
• By default it will measure line (statement) coverage.
• It can also measurebranch coverage.
• It can tell youwhat tests ran which lines.
• It can produce reports in a number of formats:text,HTML,XML,LCOV, andJSON.
• For advanced uses, there’s anAPI, and the result data is available in aSQLite database.

Coverage.py, Release 7.2.2
8 Chapter 3. Capabilities

CHAPTER
FOUR
USING COVERAGE.PY
There are a few different ways to use coverage.py. The simplest is thecommand line, which lets you run your program
and see the results. If you need more control over how your project is measured, you can use theAPI.
Some test runners provide coverage integration to make it easy to use coverage.py while running tests. For example,
pytest has the pytest-cov plugin.
You can fine-tune coverage.py’s view of your code by directing it to ignore parts that you know aren’t interesting. See
Specifying source filesand Excluding code from coverage.pyfor details.

Coverage.py, Release 7.2.2
10 Chapter 4. Using coverage.py

CHAPTER
FIVE
GETTING HELP
If theFAQdoesn’t answer your question, you can discuss coverage.py or get help using it on the Python discussion
forums. If you ping me (@nedbat), there’s a higher chance I’ll see the post.
Bug reports are gladly accepted at the GitHub issue tracker. GitHub also hosts the code repository.
Professional support for coverage.py is available as part of the Tidelift Subscription.
I can be reached in a number of ways. I’m happy to answer questions about using coverage.py.

Coverage.py, Release 7.2.2
12 Chapter 5. Getting help

CHAPTER
SIX
MORE INFORMATION
6.1 Installation
You can install coverage.py in the usual ways. The simplest way is with pip:
$ python3 -m pip install coverage
6.1.1 C Extension
Coverage.py includes a C extension for speed. It is strongly recommended to use this extension: it is much faster, and
is needed to support a number of coverage.py features. Most of the time, the C extension will be installed without any
special action on your part.
You can determine if you are using the extension by looking at the output ofcoverage --version :
$ coverage --version
Coverage.py, version 7.2.2 with C extension
Documentation at https://coverage.readthedocs.io/en/7.2.2
The first line will either say “with C extension,” or “without C extension.”
If you are missing the extension, first make sure you have the latest version of pip in use when installing coverage.
If you are installing on Linux, you may need to install the python-dev and gcc support files before installing coverage
viapip. Theexactcommandsdependonwhichpackagemanageryouuse,whichPythonversionyouareusing,andthe
names of the packages for your distribution. For example:
$ sudo apt-get install python-dev gcc
$ sudo yum install python-devel gcc
$ sudo apt-get install python3-dev gcc
$ sudo yum install python3-devel gcc
A few features of coverage.py aren’t supported without the C extension, such as concurrency and plugins.

Coverage.py, Release 7.2.2
6.1.2 Checking the installation
If all went well, you should be able to open a command prompt, and see coverage.py installed properly:
$ coverage --version
Coverage.py, version 7.2.2 with C extension
Documentation at https://coverage.readthedocs.io/en/7.2.2
You can also invoke coverage.py as a module:
$ python -m coverage --version
Coverage.py, version 7.2.2 with C extension
Documentation at https://coverage.readthedocs.io/en/7.2.2
6.2 Command line usage
When you install coverage.py, a command-line script calledcoverage is placed on your path. To help with multi-
version installs, it will also create acoverage3 alias, and a coverage-X.Y alias, depending on the version of
Python you’re using. For example, when installing on Python 3.7, you will be able to usecoverage, coverage3,
or coverage-3.7 on the command line.
Coverage.py has a number of commands:
• run –Run a Python program and collect execution data.
• combine –Combine together a number of data files.
• erase –Erase previously collected coverage data.
• report –Report coverage results.
• html –Produce annotated HTML listings with coverage results.
• xml –Produce an XML report with coverage results.
• json –Produce a JSON report with coverage results.
• lcov–Produce an LCOV report with coverage results.
• annotate –Annotate source files with coverage results.
• debug –Get diagnostic information.
Help is available with thehelpcommand, or with the--help switch on any other command:
$ coverage help
$ coverage help run
$ coverage run --help
Version information for coverage.py can be displayed withcoverage --version :
$ coverage --version
Coverage.py, version 7.2.2 with C extension
Documentation at https://coverage.readthedocs.io/en/7.2.2
Anycommandcanuseaconfigurationfilebyspecifyingitwiththe --rcfile=FILEcommand-lineswitch. Anyoption
youcansetonthecommandlinecanalsobesetintheconfigurationfile. Thiscanbeabetterwaytocontrolcoverage.py
sincetheconfigurationfilecanbecheckedintosourcecontrol,andcanprovideoptionsthatotherinvocationtechniques
(like test runner plugins) may not offer. SeeConfiguration referencefor more details.
14 Chapter 6. More information

Coverage.py, Release 7.2.2
6.2.1 Execution: coverage run
You collect execution data by running your Python program with therun command:
$ coverage run my_program.py arg1 arg2
blah blah ..your program 's output.. blah blah
Your program runs just as if it had been invoked with the Python command line. Arguments after your file name are
passedtoyourprogramasusualin sys.argv. Ratherthanprovidingafilename,youcanusethe -mswitchandspecify
an importable module name instead, just as you can with the Python-m switch:
$ coverage run -m packagename.modulename arg1 arg2
blah blah ..your program 's output.. blah blah
Note: In most cases, the program to use here is a test runner, not your program you are trying to measure. The test
runner will run your tests and coverage will measure the coverage of your code along the way.
There are many options:
$ coverage run --help
Usage: coverage run [options] <pyfile> [program options]
Run a Python program, measuring code execution.
Options:
-a, --append Append coverage data to .coverage, otherwise it starts
clean each time.
--branch Measure branch coverage in addition to statement
coverage.
--concurrency=LIBS Properly measure code using a concurrency library.
Valid values are: eventlet, gevent, greenlet,
multiprocessing, thread, or a comma-list of them.
--context=LABEL The context label to record for this coverage run.
--data-file=OUTFILE Write the recorded coverage data to this file.
Defaults to '.coverage'. [env: COVERAGE_FILE]
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
-m, --module <pyfile> is an importable Python module, not a script
path, to be run as 'python -m ' would run it.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
-L, --pylib Measure coverage even inside the Python installed
library, which isn 't done by default.
-p, --parallel-mode Append the machine name, process id and random number
to the data file name to simplify collecting data from
many processes.
--source=SRC1,SRC2,...
A list of directories or importable names of code to
measure.
--timid Use a simpler but slower trace method. Try this if you

6.2. Command line usage 15

Coverage.py, Release 7.2.2
(continued from previous page)
get seemingly impossible results!
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
If you wantbranch coveragemeasurement, use the--branchflag. Otherwise only statement coverage is measured.
You can specify the code to measure with the--source, --include, and --omit switches. SeeSpecifying source
filesfordetailsoftheirinterpretation. Remembertoputoptionsforrunafter“run”,butbeforetheprograminvocation:
$ coverage run --source=dir1,dir2 my_program.py arg1 arg2
$ coverage run --source=dir1,dir2 -m packagename.modulename arg1 arg2
Note: Specifying --source on thecoverage run command line won’t affect subsequent reporting commands like
coverage xml . Use thesourcesetting in the configuration file to apply the setting uniformly to all commands.
Coverage.py can measure multi-threaded programs by default. If you are using more other concurrency support, with
themultiprocessing,greenlet,eventlet,orgeventlibraries,thencoverage.pycangetconfused. Usethe --concurrency
switchtoproperlymeasureprogramsusingtheselibraries. Giveitavalueof multiprocessing, thread, greenlet,
eventlet, orgevent. Values other thanthread require theC extension.
Youcancombinemultiplevaluesfor --concurrency,separatedwithcommas. Youcanspecify threadandalsoone
of eventlet, gevent, orgreenlet.
If you are using--concurrency=multiprocessing, you must set other options in the configuration file. Options
on the command line will not be passed to the processes that multiprocessing creates. Best practice is to use the
configuration file for all options.
If you are measuring coverage in a multi-process program, or across a number of machines, you’ll want the
--parallel-modeswitchtokeepthedataseparateduringmeasurement. See Combiningdatafiles: coveragecombine
below.
You can specify astatic contextfor a coverage run with--context. This can be any label you want, and will be
recorded with the data. SeeMeasurement contextsfor more information.
By default, coverage.py does not measure code installed with the Python interpreter, for example, the standard library.
If you want to measure that code as well as your own, add the-L (or --pylib) flag.
If your coverage results seem to be overlooking code that you know has been executed, try running coverage.py again
with the--timidflag. This uses a simpler but slower trace method, and might be needed in rare cases.
Coverage.py sets an environment variable,COVERAGE_RUN to indicate that your code is running under coverage mea-
surement. The value is not relevant, and may change in the future.
These options can also be set in the[run] section of your .coveragerc file.
16 Chapter 6. More information

Coverage.py, Release 7.2.2
Warnings
During execution, coverage.py may warn you about conditions it detects that could affect the measurement process.
The possible warnings include:
Couldn’t parse Python file XXX (couldnt-parse)
During reporting, a file was thought to be Python, but it couldn’t be parsed as Python.
Trace function changed, data is likely wrong: XXX (trace-changed)
CoveragemeasurementdependsonaPythonsettingcalledthetracefunction. OtherPythoncodeinyourproduct
might change that function, which will disrupt coverage.py’s measurement. This warning indicates that has
happened. The XXX in the message is the new trace function value, which might provide a clue to the cause.
Module XXX has no Python source (module-not-python)
You asked coverage.py to measure module XXX, but once it was imported, it turned out not to have a corre-
sponding .py file. Without a .py file, coverage.py can’t report on missing lines.
Module XXX was never imported (module-not-imported)
You asked coverage.py to measure module XXX, but it was never imported by your program.
No data was collected (no-data-collected)
Coverage.py ran your program, but didn’t measure any lines as executed. This could be because you asked to
measure only modules that never ran, or for other reasons.
To debug this problem, try usingrun --debug=trace to see the tracing decision made for each file.
Module XXX was previously imported, but not measured (module-not-measured)
You asked coverage.py to measure module XXX, but it had already been imported when coverage started. This
meant coverage.py couldn’t monitor its execution.
Already imported a file that will be measured: XXX (already-imported)
File XXX had already been imported when coverage.py started measurement. Your setting for--source or
--includeindicates that you wanted to measure that file. Lines will be missing from the coverage report since
the execution during import hadn’t been measured.
--include is ignored because --source is set (include-ignored)
Both --includeand --sourcewerespecifiedwhilerunningcode. Botharemeanttofocusmeasurementona
particular part of your source code, so--include is ignored in favor of--source.
Conflicting dynamic contexts (dynamic-conflict)
The [run] dynamic_context option is set in the configuration file, but something (probably a test runner
plugin) is also calling theCoverage.switch_context() function to change the context. Only one of these
mechanisms should be in use at a time.
Individual warnings can be disabled with thedisable_warnings configuration setting. To silence “No data was col-
lected,” add this to your .coveragerc file:
[run]
disable_warnings = no-data-collected
or pyproject.toml:
[tool.coverage.run]
disable_warnings = [ 'no-data-collected']
6.2. Command line usage 17

Coverage.py, Release 7.2.2
Data file
Coverage.py collects execution data in a file called “.coverage”. If need be, you can set a new file name with the
COVERAGE_FILE environment variable. This can include a path to another directory.
By default, each run of your program starts with an empty data set. If you need to run your program multiple times
to get complete data (for example, because you need to supply different options), you can accumulate data across runs
with the--append flag on therun command.
6.2.2 Combining data files:coverage combine
Oftentestsuitesarerununderdifferentconditions, forexample, withdifferentversionsofPython, ordependencies, or
ondifferentoperatingsystems. Inthesecases,youcancollectcoveragedataforeachtestrun,andthencombineallthe
separate data files into one combined file for reporting.
The combine command reads a number of separate data files, matches the data by source file name, and writes a
combined data file with all of the data.
Coverage normally writes data to a filed named “.coverage”. Therun --parallel-mode switch (or [run]
parallel=True configuration option) tells coverage to expand the file name to include machine name, process id,
and a random number so that every data file is distinct:
.coverage.Neds-MacBook-Pro.local.88335.316857
.coverage.Geometer.8044.799674
You can also define a new data file name with the[run] data_file option.
Once you have created a number of these files, you can copy them all to a single directory, and use thecombine
command to combine them into one .coverage data file:
$ coverage combine
You can also name directories or files to be combined on the command line:
$ coverage combine data1.dat windows_data_files/
Coverage.py will collect the data from those places and combine them. The current directory isn’t searched if you use
command-line arguments. If you also want data from the current directory, name it explicitly on the command line.
When coverage.py combines data files, it looks for files named the same as the data file (defaulting to “.coverage”),
with a dotted suffix. Here are some examples of data files that can be combined:
.coverage.machine1
.coverage.20120807T212300
.coverage.last_good_run.ok
An existing combined data file is ignored and re-written. If you want to usecombine to accumulate results into the
.coverage data file over a number of runs, use the--append switch on thecombine command. This behavior was the
default before version 4.2.
If any of the data files can’t be read, coverage.py will print a warning indicating the file and the problem.
The original input data files are deleted once they’ve been combined. If you want to keep those files, use the--keep
command-line option.
18 Chapter 6. More information

Coverage.py, Release 7.2.2
$ coverage combine --help
Usage: coverage combine [options] <path1> <path2> ... <pathN>
Combine data from multiple coverage files. The combined results are written to
a single file representing the union of the data. The positional arguments are
data files or directories containing data files. If no paths are provided,
data files in the default data file 's directory are combined.
Options:
-a, --append Append coverage data to .coverage, otherwise it starts
clean each time.
--data-file=DATAFILE Base name of the data files to operate on. Defaults to
'.coverage'. [env: COVERAGE_FILE]
--keep Keep original coverage files, otherwise they are
deleted.
-q, --quiet Don 't print messages about what is happening.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
Re-mapping paths
To combine data for a source file, coverage has to find its data in each of the data files. Different test runs may run
the same source file from different locations. For example, different operating systems will use different paths for the
same file, or perhaps each Python version is run from a different subdirectory. Coverage needs to know that different
file paths are actually the same source file for reporting purposes.
You can tell coverage.py how different source locations relate with a[paths] section in your configuration file (see
[paths]). It might be more convenient to use the[run] relative_files setting to store relative file paths (see
relative_files).
If data isn’t combining properly, you can see details about the inner workings with--debug=pathmap.
6.2.3 Erase data: coverage erase
To erase the collected data, use theerase command:
$ coverage erase --help
Usage: coverage erase [options]
Erase previously collected coverage data.
Options:
--data-file=DATAFILE Base name of the data files to operate on. Defaults to
'.coverage'. [env: COVERAGE_FILE]
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',

6.2. Command line usage 19

Coverage.py, Release 7.2.2
(continued from previous page)
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
If your configuration file indicates parallel data collection,erase will remove all of the data files.
6.2.4 Reporting
Coverage.pyprovidesafewstylesofreporting,withthe report,html,annotate,json,lcov,and xmlcommands. They
share a number of common options.
The command-line arguments are module or file names to report on, if you’d like to report on a subset of the data
collected.
The --include and --omit flags specify lists of file name patterns. They control which files to report on, and are
described in more detail inSpecifying source files.
The -i or --ignore-errors switch tells coverage.py to ignore problems encountered trying to find source files to
report on. This can be useful if some files are missing, or if your Python execution is tricky enough that file names are
synthesized without real source files.
If you provide a--fail-under value, the total percentage covered will be compared to that value. If it is less, the
commandwillexitwithastatuscodeof2,indicatingthatthetotalcoveragewaslessthanyourtarget. Thiscanbeused
aspartofapass/failcondition,forexampleinacontinuousintegrationserver. Thisoptionisn’tavailablefor annotate.
These options can also be set in your .coveragerc file. SeeConfiguration: [report].
6.2.5 Coverage summary: coverage report
The simplest reporting is a textual summary produced withreport:
$ coverage report
Name Stmts Miss Cover
---------------------------------------------
my_program.py 20 4 80%
my_module.py 15 2 86%
my_other_module.py 56 6 89%
---------------------------------------------
TOTAL 91 12 87%
Foreachmoduleexecuted,thereportshowsthecountofexecutablestatements,thenumberofthosestatementsmissed,
and the resulting coverage, expressed as a percentage.
$ coverage report --help
Usage: coverage report [options] [modules]
Report coverage statistics on modules.
Options:
--contexts=REGEX1,REGEX2,...
Only display data from lines covered in the given
contexts. Accepts Python regexes, which must be
quoted.
--data-file=INFILE Read coverage data for report generation from this

20 Chapter 6. More information

Coverage.py, Release 7.2.2
(continued from previous page)
file. Defaults to '.coverage'. [env: COVERAGE_FILE]
--fail-under=MIN Exit with a status of 2 if the total coverage is less
than MIN.
--format=FORMAT Output format, either text (default), markdown, or
total.
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
--precision=N Number of digits after the decimal point to display
for reported coverage percentages.
--sort=COLUMN Sort the report by the named column: name, stmts,
miss, branch, brpart, or cover. Default is name.
-m, --show-missing Show line numbers of statements in each module that
weren't executed.
--skip-covered Skip files with 100% coverage.
--no-skip-covered Disable --skip-covered.
--skip-empty Skip files with no code.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
The -m flag also shows the line numbers of missing statements:
$ coverage report -m
Name Stmts Miss Cover Missing
-------------------------------------------------------
my_program.py 20 4 80% 33-35, 39
my_module.py 15 2 86% 8, 12
my_other_module.py 56 6 89% 17-23
-------------------------------------------------------
TOTAL 91 12 87%
If you are using branch coverage, then branch statistics will be reported in the Branch and BrPart (for Partial Branch)
columns, the Missing column will detail the missed branches:
$ coverage report -m
Name Stmts Miss Branch BrPart Cover Missing
---------------------------------------------------------------------
my_program.py 20 4 10 2 80% 33-35, 36->38, 39
my_module.py 15 2 3 0 86% 8, 12
my_other_module.py 56 6 5 1 89% 17-23, 40->45
---------------------------------------------------------------------
TOTAL 91 12 18 3 87%
You can restrict the report to only certain files by naming them on the command line:
6.2. Command line usage 21

Coverage.py, Release 7.2.2
$ coverage report -m my_program.py my_other_module.py
Name Stmts Miss Cover Missing
-------------------------------------------------------
my_program.py 20 4 80% 33-35, 39
my_other_module.py 56 6 89% 17-23
-------------------------------------------------------
TOTAL 76 10 87%
The --skip-covered switch will skip any file with 100% coverage, letting you focus on the files that still need
attention. The--no-skip-coveredoption can be used if needed to see all the files. The--skip-emptyswitch will
skip any file with no executable statements.
If you haverecorded contexts, the --contexts option lets you choose which contexts to report on. SeeContext
reportingfor details.
The --precision option controls the number of digits displayed after the decimal point in coverage percentages,
defaulting to none.
The --sort option is the name of a column to sort the report by.
The --format option controls the style of the report.--format=text creates plain text tables as shown above.
--format=markdown creates Markdown tables. --format=total writes out a single number, the total coverage
percentage as shown at the end of the tables, but without a percent sign.
Other common reporting options are described above inReporting. These options can also be set in your .coveragerc
file. SeeConfiguration: [report].
6.2.6 HTML reporting: coverage html
Coverage.pycanannotateyoursourcecodetoshowwhichlineswereexecutedandwhichwerenot. The htmlcommand
creates an HTML report similar to thereport summary, but as an HTML file. Each module name links to the source
file decorated to show the status of each line.
Here’s a sample report.
Lines are highlighted green for executed, red for missing, and gray for excluded. The counts at the top of the file are
buttons to turn on and off the highlighting.
A number of keyboard shortcuts are available for navigating the report. Click the keyboard icon in the upper right to
see the complete list.
$ coverage html --help
Usage: coverage html [options] [modules]
Create an HTML report of the coverage of the files. Each file gets its own
page, with the source decorated to show executed, excluded, and missed lines.
Options:
--contexts=REGEX1,REGEX2,...
Only display data from lines covered in the given
contexts. Accepts Python regexes, which must be
quoted.
-d DIR, --directory=DIR
Write the output files to DIR.
--data-file=INFILE Read coverage data for report generation from this
file. Defaults to '.coverage'. [env: COVERAGE_FILE]

22 Chapter 6. More information

Coverage.py, Release 7.2.2
(continued from previous page)
--fail-under=MIN Exit with a status of 2 if the total coverage is less
than MIN.
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
--precision=N Number of digits after the decimal point to display
for reported coverage percentages.
-q, --quiet Don 't print messages about what is happening.
--show-contexts Show contexts for covered lines.
--skip-covered Skip files with 100% coverage.
--no-skip-covered Disable --skip-covered.
--skip-empty Skip files with no code.
--title=TITLE A text string to use as the title on the HTML.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
Thetitleofthereportcanbesetwiththe titlesettinginthe [html]sectionoftheconfigurationfile,orthe --title
switch on the command line.
If you prefer a different style for your HTML report, you can provide your own CSS file to apply, by specifying a CSS
file in the[html] section of the configuration file. See[html] extra_cssfor details.
The -d argument specifies an output directory, defaulting to “htmlcov”:
$ coverage html -d coverage_html
Other common reporting options are described above inReporting.
Generating the HTML report can be time-consuming. Stored with the HTML report is a data file that is used to speed
up reporting the next time. If you generate a new report into the same directory, coverage.py will skip generating
unchanged pages, making the process faster.
The --skip-covered switch will skip any file with 100% coverage, letting you focus on the files that still need
attention. The--skip-emptyswitch will skip any file with no executable statements.
The --precision option controls the number of digits displayed after the decimal point in coverage percentages,
defaulting to none.
If you have recorded contexts, the --contexts option lets you choose which contexts to report on, and the
--show-contextsoption will annotate lines with the contexts that ran them. SeeContext reportingfor details.
These options can also be set in your .coveragerc file. SeeConfiguration: [html].
6.2. Command line usage 23

Coverage.py, Release 7.2.2
6.2.7 XML reporting: coverage xml
The xml command writes coverage data to a “coverage.xml” file in a format compatible with Cobertura.
$ coverage xml --help
Usage: coverage xml [options] [modules]
Generate an XML report of coverage results.
Options:
--data-file=INFILE Read coverage data for report generation from this
file. Defaults to '.coverage'. [env: COVERAGE_FILE]
--fail-under=MIN Exit with a status of 2 if the total coverage is less
than MIN.
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
-o OUTFILE Write the XML report to this file. Defaults to
'coverage.xml'
-q, --quiet Don 't print messages about what is happening.
--skip-empty Skip files with no code.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
You can specify the name of the output file with the-o switch.
Other common reporting options are described above inReporting.
To include complete file paths in the output file, rather than just the file name, use [include] vs [source] in your “.cov-
eragerc” file.
For example, use this:
[run]
include =
foo/*
bar/*
which will result in
<class filename="bar/hello.py">
<class filename="bar/baz/hello.py">
<class filename="foo/hello.py">
in place of this:
24 Chapter 6. More information

Coverage.py, Release 7.2.2
[run]
source =
foo
bar
which may result in
<class filename="hello.py">
<class filename="baz/hello.py">
These options can also be set in your .coveragerc file. SeeConfiguration: [xml].
6.2.8 JSON reporting: coverage json
The json command writes coverage data to a “coverage.json” file.
$ coverage json --help
Usage: coverage json [options] [modules]
Generate a JSON report of coverage results.
Options:
--contexts=REGEX1,REGEX2,...
Only display data from lines covered in the given
contexts. Accepts Python regexes, which must be
quoted.
--data-file=INFILE Read coverage data for report generation from this
file. Defaults to '.coverage'. [env: COVERAGE_FILE]
--fail-under=MIN Exit with a status of 2 if the total coverage is less
than MIN.
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
-o OUTFILE Write the JSON report to this file. Defaults to
'coverage.json'
--pretty-print Format the JSON for human readers.
-q, --quiet Don 't print messages about what is happening.
--show-contexts Show contexts for covered lines.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
You can specify the name of the output file with the-o switch. The JSON can be nicely formatted by specifying the
--pretty-print switch.
Other common reporting options are described above inReporting. These options can also be set in your .coveragerc
file. SeeConfiguration: [json].
6.2. Command line usage 25

Coverage.py, Release 7.2.2
6.2.9 LCOV reporting: coverage lcov
The lcovcommand writes coverage data to a “coverage.lcov” file.
$ coverage lcov --help
Usage: coverage lcov [options] [modules]
Generate an LCOV report of coverage results.
Options:
--data-file=INFILE Read coverage data for report generation from this
file. Defaults to '.coverage'. [env: COVERAGE_FILE]
--fail-under=MIN Exit with a status of 2 if the total coverage is less
than MIN.
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
-o OUTFILE Write the LCOV report to this file. Defaults to
'coverage.lcov'
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
-q, --quiet Don 't print messages about what is happening.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
Common reporting options are described above inReporting. Also seeConfiguration: [lcov].
New in version 6.3.
6.2.10 Text annotation:coverage annotate
Note: The annotate command has been obsoleted by more modern reporting tools, including thehtml command.
annotate will be removed in a future version.
The annotate command produces a text annotation of your source code. With a-d argument specifying an output
directory,eachPythonfilebecomesatextfileinthatdirectory. Without -d,thefilesarewrittenintothesamedirectories
as the original Python files.
Coverage status for each line of source is indicated with a character prefix:
> executed
! missing (not executed)
- excluded
For example:
26 Chapter 6. More information

Coverage.py, Release 7.2.2
# A simple function, never called with x==1
> def h(x):
"""Silly function."""
- if 0: # pragma: no cover
- pass
> if x == 1:
! a = 1
> else:
> a = 2
$ coverage annotate --help
Usage: coverage annotate [options] [modules]
Make annotated copies of the given files, marking statements that are executed
with > and statements that are missed with !.
Options:
-d DIR, --directory=DIR
Write the output files to DIR.
--data-file=INFILE Read coverage data for report generation from this
file. Defaults to '.coverage'. [env: COVERAGE_FILE]
-i, --ignore-errors Ignore errors while reading source files.
--include=PAT1,PAT2,...
Include only files whose paths match one of these
patterns. Accepts shell-style wildcards, which must be
quoted.
--omit=PAT1,PAT2,... Omit files whose paths match one of these patterns.
Accepts shell-style wildcards, which must be quoted.
--debug=OPTS Debug options, separated by commas. [env:
COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are
tried. [env: COVERAGE_RCFILE]
Other common reporting options are described above inReporting.
6.2.11 Diagnostics: coverage debug
The debug command shows internal information to help diagnose problems. If you are reporting a bug about cover-
age.py, including the output of this command can often help:
$ coverage debug sys > please_attach_to_bug_report.txt
A few types of information are available:
• config: show coverage’s configuration
• sys: show system configuration
• data: show a summary of the collected coverage data
• premain: show the call stack invoking coverage
6.2. Command line usage 27

Coverage.py, Release 7.2.2
• pybehave: show internal flags describing Python behavior
$ coverage debug --help
Usage: coverage debug <topic>
Display information about the internals of coverage.py, for diagnosing
problems. Topics are: 'data' to show a summary of the collected data; 'sys' to
show installation information; 'config' to show the configuration; 'premain'
to show what is calling coverage; 'pybehave' to show internal flags describing
Python behavior.
Options:
--debug=OPTS Debug options, separated by commas. [env: COVERAGE_DEBUG]
-h, --help Get help on this command.
--rcfile=RCFILE Specify configuration file. By default '.coveragerc',
'setup.cfg', 'tox.ini', and 'pyproject.toml' are tried.
[env: COVERAGE_RCFILE]
--debug
The --debugoption is also available on all commands. It instructs coverage.py to log internal details of its operation,
to help with diagnosing problems. It takes a comma-separated list of options, each indicating a facet of operation to
log:
• callers: annotate each debug message with a stack trace of the callers to that point.
• config: before starting, dump all theconfigurationvalues.
• dataio: log when reading or writing any data file.
• dataop: log when data is added to the CoverageData object.
• lock: log operations acquiring locks in the data layer.
• multiproc: log the start and stop of multiprocessing processes.
• pathmap: log the remapping of paths that happens duringcoverage combine . See[paths].
• pid: annotate all warnings and debug output with the process and thread ids.
• plugin: print information about plugin operations.
• process: showprocesscreationinformation,andchangesinthecurrentdirectory. Thisalsowritesatimestamp
and command arguments into the data file.
• pybehave: show the values of internal flags describing the behavior of the current version of Python.
• self: annotate each debug message with the object printing the message.
• sql: log the SQL statements used for recording data.
• sqldata: when used withdebug=sql, also log the full data being used in SQL statements.
• sys: before starting, dump all the system and environment information, as withcoverage debug sys.
• trace: print every decision about whether to trace a file or not. For files not being traced, the reason is also
given.
Debug options can also be set with theCOVERAGE_DEBUG environment variable, a comma-separated list of these op-
tions, or in the[run] debugsection of the .coveragerc file.
28 Chapter 6. More information

Coverage.py, Release 7.2.2
The debug output goes to stderr, unless the[run] debug_filesetting or theCOVERAGE_DEBUG_FILEenvironment vari-
able names a different file, which will be appended to. This can be useful because many test runners capture output,
which could hide important details.COVERAGE_DEBUG_FILE accepts the special namesstdout and stderr to write
to those destinations.
6.3 Configuration reference
Coverage.py options can be specified in a configuration file. This makes it easier to re-run coverage.py with consistent
settings, and also allows for specification of options that are otherwise only available in theAPI.
Configurationfilesalsomakeiteasiertogetcoveragetestingofspawnedsub-processes. See Measuringsub-processes
for more details.
The default name for configuration files is.coveragerc, in the same directory coverage.py is being run in. Most of
the settings in the configuration file are tied to your source code and how it should be measured, so it should be stored
with your source, and checked into source control, rather than put in your home directory.
A different location for the configuration file can be specified with the--rcfile=FILE command line option or with
the COVERAGE_RCFILEenvironment variable.
Coverage.py will read settings from other usual configuration files if no other configuration file is used. It will auto-
matically read from “setup.cfg” or “tox.ini” if they exist. In this case, the section names have “coverage:” prefixed, so
the [run]options described below will be found in the[coverage:run] section of the file.
Coverage.py will read from “pyproject.toml” if TOML support is available, either because you are running on Python
3.11 or later, or because you installed with thetoml extra (pip install coverage[toml] ). Configuration must
be within the[tool.coverage] section, for example,[tool.coverage.run]. Environment variable expansion in
values is available, but only within quoted strings, even for non-string values.
6.3.1 Syntax
A coverage.py configuration file is in classic .ini file format: sections are introduced by a[section] header, and
contain name = value entries. Lines beginning with#or ;are ignored as comments.
Strings don’t need quotes. Multi-valued strings can be created by indenting values on multiple lines.
Boolean values can be specified ason, off, true, false, 1, or0and are case-insensitive.
Environment variables can be substituted in by using dollar signs:$WORD or ${WORD} will be replaced with the value
of WORDintheenvironment. Adollarsigncanbeinsertedwith $$. Specialformscanbeusedtocontrolwhathappens
if the variable isn’t defined in the environment:
• If you want to raise an error if an environment variable is undefined, use a question mark suffix:${WORD?}.
• Ifyouwanttoprovideadefaultformissingvariables,useadashwithadefaultvalue: ${WORD-default value} .
• Otherwise, missing environment variables will result in empty strings with no error.
Many sections and settings correspond roughly to commands and options in thecommand-line interface.
Here’s a sample configuration file:
# .coveragerc to control coverage.py
[run]
branch = True
[report]

6.3. Configuration reference 29

Coverage.py, Release 7.2.2
(continued from previous page)
# Regexes for lines to exclude from consideration
exclude_lines =
# Have to re-enable the standard pragma
pragma: no cover
# Don 't complain about missing debug-only code:
def __repr__
if self\.debug
# Don 't complain if tests don 't hit defensive assertion code:
raise AssertionError
raise NotImplementedError
# Don 't complain if non-runnable code isn 't run:
if 0:
if __name__ == .__main__.:
# Don 't complain about abstract methods, they aren 't run:
@(abc\.)?abstractmethod
ignore_errors = True
[html]
directory = coverage_html_report
6.3.2 [run]
These settings are generally used when running product code, though some apply to more than one command.
[run] branch
(boolean, default False) Whether to measurebranch coveragein addition to statement coverage.
[run] command_line
(string)Thecommand-linetorunyourprogram. Thiswillbeusedifyourun coverage run withnofurtherarguments.
Coverage.py options cannot be specified here, other than-m to indicate the module to run.
New in version 5.0.
[run] concurrency
(multi-string, default “thread”) The concurrency libraries in use by the product code. If your program uses multipro-
cessing,gevent,greenlet,oreventlet,youmustnamethatlibraryinthisoption,orcoverage.pywillproduceverywrong
results.
See Measuring sub-processesfor details of multi-process measurement.
Before version 4.2, this option only accepted a single string.
New in version 4.0.
30 Chapter 6. More information

Coverage.py, Release 7.2.2
[run] context
(string) The static context to record for this coverage run. SeeMeasurement contextsfor more information
New in version 5.0.
[run] cover_pylib
(boolean, default False) Whether to measure the Python standard library.
[run] data_file
(string, default “.coverage”) The name of the data file to use for storing or reporting coverage. This value can include
a path to another directory.
[run] disable_warnings
(multi-string) A list of warnings to disable. Warnings that can be disabled include a short string at the end, the name
of the warning. SeeWarningsfor specific warnings.
[run] debug
(multi-string) A list of debug options. Seethe run –debug optionfor details.
[run] debug_file
(string) A file name to write debug output to. Seethe run –debug optionfor details.
[run] dynamic_context
(string) The name of a strategy for setting the dynamic context during execution. SeeDynamic contextsfor details.
[run] include
(multi-string) A list of file name patterns, the files to include in measurement or reporting. Ignored ifsource is set.
See Specifying source filesfor details.
[run] omit
(multi-string)Alistoffilenamepatterns,thefilestoleaveoutofmeasurementorreporting. See Specifyingsourcefiles
for details.
6.3. Configuration reference 31

Coverage.py, Release 7.2.2
[run] parallel
(boolean, default False) Append the machine name, process id and random number to the data file name to simplify
collecting data from many processes. SeeCombining data files: coverage combinefor more information.
[run] plugins
(multi-string) A list of plugin package names. SeePlug-ins for more information.
[run] relative_files
(boolean,defaultFalse)storerelativefilepathsinthedatafile. Thismakesiteasiertomeasurecodeinone(ormultiple)
environments, and then report in another. SeeCombining data files: coverage combinefor details.
Note that settingsourcehas to be done in the configuration file rather than the command line for this option to work,
since the reporting commands need to know the source origin.
New in version 5.0.
[run] sigterm
(boolean, default False) if true, register a SIGTERM signal handler to capture data when the process ends due to a
SIGTERM signal. This includesProcess.terminate, and other ways to terminate a process. This can help when
collecting data in usual situations, but can also introduce problems (see issue 1310).
Only on Linux and Mac.
New in version 6.4: (in 6.3 this was always enabled)
[run] source
(multi-string)Alistofpackagesordirectories,thesourcetomeasureduringexecution. Ifset, includeisignored. See
Specifying source filesfor details.
[run] source_pkgs
(multi-string)Alistofpackages,thesourcetomeasureduringexecution. Operatesthesameas source,butonlynames
packages, for resolving ambiguities between packages and directories.
New in version 5.3.
[run] timid
(boolean, default False) Use a simpler but slower trace method. This uses PyTracer instead of CTracer, and is only
needed in very unusual circumstances. Try this if you get seemingly impossible results.
32 Chapter 6. More information

Coverage.py, Release 7.2.2
6.3.3 [paths]
Theentriesinthissectionarelistsoffilepathsthatshouldbeconsideredequivalentwhencombiningdatafromdifferent
machines:
[paths]
source =
src/
/jenkins/build/*/src
c:\myproj\src
The names of the entries (“source” in this example) are ignored, you may choose any name that you like. The value is
a list of strings. When combining data with thecombine command, two file paths will be combined if they start with
paths from the same list.
The first value must be an actual file path on the machine where the reporting will happen, so that source code can be
found. The other values can be file patterns to match against the paths of collected data, or they can be absolute or
relative file paths on the current machine.
In this example, data collected for “/jenkins/build/1234/src/module.py” will be combined with data for
“c:\myproj\src\module.py”, and will be reported against the source file found at “src/module.py”.
If you specify more than one list of paths, they will be considered in order. A file path will only be remapped if the
result exists. If a path matches a list, but the result doesn’t exist, the next list will be tried. The first list that has an
existing result will be used.
Remappingwillalsobedoneduringreporting,butonlywithinthesingledatafilebeingreported. Combiningmultiple
files requires thecombinecommand.
The --debug=pathmapoption can be used to log details of the re-mapping of paths. Seethe –debug option.
See Re-mapping pathsand File patternsfor more information.
6.3.4 [report]
Settings common to many kinds of reporting.
[report] exclude_lines
(multi-string)Alistofregularexpressions. Anylineofyoursourcecodecontainingamatchforoneoftheseregexesis
excludedfrombeingreportedasmissing. Moredetailsarein Excludingcodefromcoverage.py . Ifyouusethisoption,
you are replacing all the exclude regexes, so you’ll need to also supply the “pragma: no cover” regex if you still want
to use it.
You can exclude lines introducing blocks, and the entire block is excluded. If you exclude adef line or decorator line,
the entire function is excluded.
Be careful when writing this setting: the values are regular expressions that only have to match a portion of the line.
For example, if you write..., you’ll exclude any line with three or more of any character. If you writepass, you’ll
also exclude the linemy_pass="foo", and so on.
6.3. Configuration reference 33

Coverage.py, Release 7.2.2
[report] exclude_also
(multi-string)Alistofregularexpressions. Thissettingisthesameas [report]exclude_lines: itaddspatternsforlines
to exclude from reporting. This setting will preserve the default exclude patterns instead of overwriting them.
New in version 7.2.0.
[report] fail_under
(float) A target coverage percentage. If the total coverage measurement is under this value, then exit with a status code
of2. Ifyouspecifyanon-integralvalue,youmustalsoset [report] precision properlytomakeuseofthedecimal
places. A setting of 100 will fail any value under 100, regardless of the number of decimal places of precision.
[report] ignore_errors
(boolean, default False) Ignore source code that can’t be found, emitting a warning instead of an exception.
[report] include
(multi-string) A list of file name patterns, the files to include in reporting. SeeSpecifying source filesfor details.
[report] include_namespace_packages
(boolean, default False) When searching for completely un-executed files, include directories without__init__.py
files. These are implicit namespace packages, and are usually skipped.
New in version 7.0.
[report] omit
(multi-string) A list of file name patterns, the files to leave out of reporting. SeeSpecifying source filesfor details.
[report] partial_branches
(multi-string) A list of regular expressions. Any line of code that matches one of these regexes is excused from being
reportedasapartialbranch. Moredetailsarein Branchcoveragemeasurement. Ifyouusethisoption,youarereplacing
all the partial branch regexes so you’ll need to also supply the “pragma: no branch” regex if you still want to use it.
[report] precision
(integer) The number of digits after the decimal point to display for reported coverage percentages. The default is
0, displaying for example “87%”. A value of 2 will display percentages like “87.32%”. This setting also affects the
interpretation of thefail_undersetting.
34 Chapter 6. More information

Coverage.py, Release 7.2.2
[report] show_missing
(boolean,defaultFalse)Whenrunningasummaryreport,showmissinglines. See Coveragesummary: coveragereport
for more information.
[report] skip_covered
(boolean, default False) Don’t report files that are 100% covered. This helps you focus on files that need attention.
[report] skip_empty
(boolean, default False) Don’t report files that have no executable code (such as__init__.py files).
[report] sort
(string, default “Name”) Sort the text report by the named column. Allowed values are “Name”, “Stmts”, “Miss”,
“Branch”, “BrPart”, or “Cover”. Prefix with-for descending sort (for example, “-cover”).
6.3.5 [html]
Settings particular to HTML reporting. The settings in the[report] section also apply to HTML output, where
appropriate.
[html] directory
(string, default “htmlcov”) Where to write the HTML report files.
[html] extra_css
(string)ThepathtoafileofCSStoapplytotheHTMLreport. ThefilewillbecopiedintotheHTMLoutputdirectory.
Don’t name it “style.css”. This CSS is in addition to the CSS normally used, though you can overwrite as many of the
rules as you like.
[html] show_contexts
(boolean)ShouldtheHTMLreportincludeanindicationoneachlineofwhichcontextsexecutedtheline. See Dynamic
contextsfor details.
[html] skip_covered
(boolean,defaultedfrom [report] skip_covered )Don’tincludefilesinthereportthatare100%coveredfiles. See
Coverage summary: coverage reportfor more information.
New in version 5.4.
6.3. Configuration reference 35

Coverage.py, Release 7.2.2
[html] skip_empty
(boolean, defaulted from [report] skip_empty ) Don’t include empty files (those that have 0 statements) in the
report. SeeCoverage summary: coverage reportfor more information.
New in version 5.4.
[html] title
(string, default “Coverage report”) The title to use for the report. Note this is text, not HTML.
6.3.6 [xml]
Settings particular to XML reporting. The settings in the[report] section also apply to XML output, where appro-
priate.
[xml] output
(string, default “coverage.xml”) Where to write the XML report.
[xml] package_depth
(integer, default 99) Controls which directories are identified as packages in the report. Directories deeper than this
depth are not reported as packages. The default is that all directories are reported as packages.
6.3.7 [json]
Settings particular to JSON reporting. The settings in the[report]section also apply to JSON output, where appro-
priate.
New in version 5.0.
[json] output
(string, default “coverage.json”) Where to write the JSON file.
[json] pretty_print
(boolean, default false) Controls if the JSON is outputted with white space formatted for human consumption (True)
or for minimum file size (False).
36 Chapter 6. More information

Coverage.py, Release 7.2.2
[json] show_contexts
(boolean, default false) Should the JSON report include an indication of which contexts executed each line. SeeDy-
namic contextsfor details.
6.3.8 [lcov]
Settings particular to LCOV reporting (seeLCOV reporting: coverage lcov).
New in version 6.3.
[lcov] output
(string, default “coverage.lcov”) Where to write the LCOV file.
6.4 Specifying source files
When coverage.py is running your program and measuring its execution, it needs to know what code to measure and
what code not to. Measurement imposes a speed penalty, and the collected data must be stored in memory and then
on disk. More importantly, when reviewing your coverage reports, you don’t want to be distracted with modules that
aren’t your concern.
Coverage.py has a number of ways you can focus it in on the code you care about.
6.4.1 Execution
Whenrunningyourcode,the coverage run commandwillbydefaultmeasureallcode,unlessitispartofthePython
standard library.
You can specify source to measure with the--source command-line switch, or the[run] source configuration
value. The value is a comma- or newline-separated list of directories or importable names (packages or modules).
Ifthesourceoptionisspecified,onlycodeinthoselocationswillbemeasured. Specifyingthesourceoptionalsoenables
coverage.pytoreportonun-executedfiles,sinceitcansearchthesourcetreeforfilesthathaven’tbeenmeasuredatall.
Only importable files (ones at the root of the tree, or in directories with a__init__.pyfile) will be considered. Files
with unusual punctuation in their names will be skipped (they are assumed to be scratch files written by text editors).
Files that do not end with.py, .pyw, .pyo, or.pycwill also be skipped.
Note: Modules named as sources may be imported twice, once by coverage.py to find their location, then again by
your own code or test suite. Usually this isn’t a problem, but could cause trouble if a module has side-effects at import
time.
Exceptions during the early import are suppressed and ignored.
You can further fine-tune coverage.py’s attention with the--include and --omit switches (or[run] include and
[run] omit configuration values). --include is a list of file name patterns. If specified, only files matching those
patternswillbemeasured. --omitisalsoalistoffilenamepatterns,specifyingfilesnottomeasure. Ifboth include
and omit are specified, first the set of files is reduced to only those that match the include patterns, then any files that
match the omit pattern are removed from the set.
The includeand omitfilenamepatternsfollowcommonshellsyntax,describedbelowin Filepatterns. Patternsthat
start with a wildcard character are used as-is, other patterns are interpreted relative to the current directory:
6.4. Specifying source files 37

Coverage.py, Release 7.2.2
[run]
omit =
# omit anything in a .local directory anywhere
*/.local/*
# omit everything in /usr
/usr/*
# omit this single file
utils/tirefire.py
The source, include, andomitvalues all work together to determine the source that will be measured.
If bothsource and include are set, theincludevalue is ignored and a warning is issued.
6.4.2 Reporting
Once your program is measured, you can specify the source files you want reported. Usually you want to see all the
code that was measured, but if you are measuring a large project, you may want to get reports for just certain parts.
The report commands (report, html, json, lcov, annotate, and xml) all take optionalmodules arguments, and
--include and --omit switches. The modules arguments specify particular modules to report on. Theinclude
and omitvalues are lists of file name patterns, just as with theruncommand.
Remember that thereporting commands can only reporton the data that hasbeen collected, so the data you’re looking
for may not be in the data available for reporting.
Note that these are ways of specifying files to measure. You can also exclude individual source lines. SeeExcluding
code from coverage.pyfor details.
6.4.3 File patterns
Filepathpatternsareusedforincludeandomit,andforcombiningpathremapping. Theyfollowcommonshellsyntax:
• *matches any number of file name characters, not including the directory separator.
• ?matches a single file name character.
• **matches any number of nested directory names, including none.
• Both /and \will match either a slash or a backslash, to make cross-platform matching easier.
6.5 Excluding code from coverage.py
You may have code in your project that you know won’t be executed, and you want to tell coverage.py to ignore it. For
example,youmayhavedebugging-onlycodethatwon’tbeexecutedduringyourunittests. Youcantellcoverage.pyto
exclude this code during reporting so that it doesn’t clutter your reports with noise about code that you don’t need to
hear about.
Coverage.pywilllookforcommentsmarkingclausesforexclusion. Inthiscode,the“ifdebug”clauseisexcludedfrom
reporting:
a = my_function1()
if debug: # pragma: no cover
msg = "blah blah"

38 Chapter 6. More information

Coverage.py, Release 7.2.2
(continued from previous page)
log_message(msg, a)
b = my_function2()
Any line with a comment of “pragma: no cover” is excluded. If that line introduces a clause, for example, an if clause,
or a function or class definition, then the entire clause is also excluded. Here the __repr__ function is not reported as
missing:
class MyObject (object):
def __init__(self):
blah1()
blah2()
def __repr__(self): # pragma: no cover
return "<MyObject>"
Excludedcodeisexecutedasusual,anditsexecutionisrecordedinthecoveragedataasusual. Whenproducingreports
though, coverage.py excludes it from the list of missing code.
6.5.1 Branch coverage
When measuringbranch coverage, a conditional will not be counted as a branch if one of its choices is excluded:
def only_one_choice(x):
if x:
blah1()
blah2()
else: # pragma: no cover
# x is always true.
blah3()
Because theelseclause is excluded, theif only has one possible next line, so it isn’t considered a branch at all.
6.5.2 Advanced exclusion
Coverage.pyidentifiesexclusionsbymatchinglinesagainstalistofregularexpressions. Using configurationfiles orthe
coverageAPI, you can add to that list. This is useful if you have often-used constructs to exclude that can be matched
with a regex. You can exclude them all at once without littering your code with exclusion pragmas.
If the matched line introduces a block, the entire block is excluded from reporting. Matching adef line or decorator
line will exclude an entire function.
For example, you might decide that __repr__ functions are usually only used in debugging code, and are uninteresting
to test themselves. You could exclude all of them by adding a regex to the exclusion list:
[report]
exclude_lines =
def __repr__
For example, here’s a list of exclusions I’ve used:
[report]
exclude_lines =

6.5. Excluding code from coverage.py 39

Coverage.py, Release 7.2.2
(continued from previous page)
pragma: no cover
def __repr__
if self.debug:
if settings.DEBUG
raise AssertionError
raise NotImplementedError
if 0:
if __name__ == .__main__.:
if TYPE_CHECKING:
class .*\bProtocol\):
@(abc\.)?abstractmethod
Note that when using theexclude_lines option in a configuration file, you are taking control of the entire list of
regexes,soyouneedtore-specifythedefault“pragma: nocover”matchifyoustillwantittoapply. The exclude_also
option can be used instead to preserve the default exclusions while adding new ones.
The regexes only have to match part of a line. Be careful not to over-match. A value of... will match any line with
more than three characters in it.
Asimilarpragma,“nobranch”,canbeusedtotailorbranchcoveragemeasurement. See Branchcoveragemeasurement
for details.
6.5.3 Excluding source files
See Specifying source filesfor ways to limit what files coverage.py measures or reports on.
6.6 Branch coverage measurement
In addition to the usual statement coverage, coverage.py also supports branch coverage measurement. Where a line
in your program could jump to more than one next line, coverage.py tracks which of those destinations are actually
visited, and flags lines that haven’t visited all of their possible destinations.
For example:
1 def my_partial_fn(x):
2 if x:
3 y = 10
4 return y

6 my_partial_fn(1)
In this code, line 2 is anif statement which can go next to either line 3 or line 4. Statement coverage would show all
lines of the function as executed. But the if was never evaluated as false, so line 2 never jumps to line 4.
Branch coverage will flag this code as not fully covered because of the missing jump from line 2 to line 4. This is
known as a partial branch.
40 Chapter 6. More information

Coverage.py, Release 7.2.2
6.6.1 How to measure branch coverage
To measure branch coverage, run coverage.py with the--branch flag:
coverage run --branch myprog.py
When you report on the results withcoverage report or coverage html , the percentage of branch possibilities
taken will be included in the percentage covered total for each file. The coverage percentage for a file is the actual
executions divided by the execution opportunities. Each line in the file is an execution opportunity, as is each branch
destination.
The HTML report gives information about which lines had missing branches. Lines that were missing some branches
areshowninyellow,withanannotationatthefarrightshowingbranchdestinationlinenumbersthatwerenotexercised.
The XML and JSON reports produced bycoverage xml and coverage json also include branch information, in-
cluding separate statement and branch coverage percentages.
6.6.2 How it works
Whenmeasuringbranches,coverage.pycollectspairsoflinenumbers,asourceanddestinationforeachtransitionfrom
one line to another. Static analysis of the source provides a list of possible transitions. Comparing the measured to the
possible indicates missing branches.
The idea of tracking how lines follow each other was from Titus Brown. Thanks, Titus!
6.6.3 Excluding code
If you haveexcluded code, a conditional will not be counted as a branch if one of its choices is excluded:
1 def only_one_choice(x):
2 if x:
3 blah1()
4 blah2()
5 else: # pragma: no cover
6 # x is always true.
7 blah3()
Because theelseclause is excluded, theif only has one possible next line, so it isn’t considered a branch at all.
6.6.4 Structurally partial branches
Sometimes branching constructs are used in unusual ways that don’t actually branch. For example:
while True :
if cond:
break
do_something()
Here the while loop will never exit normally, so it doesn’t take both of its “possible” branches. For some of these
constructs, such as “while True:” and “if 0:”, coverage.py understands what is going on. In these cases, the line will
not be marked as a partial branch.
But there are many ways in your own code to write intentionally partial branches, and you don’t want coverage.py
pestering you about them. You can tell coverage.py that you don’t want them flagged by marking them with a pragma:
6.6. Branch coverage measurement 41

Coverage.py, Release 7.2.2
i = 0
while i < 999999999: # pragma: no branch
if eventually():
break
Herethewhileloopwillnevercompletebecausethebreakwillalwaysbetakenatsomepoint. Coverage.pycan’twork
that out on its own, but the “no branch” pragma indicates that the branch is known to be partial, and the line is not
flagged.
6.7 Measuring sub-processes
Complextestsuitesmayspawnsub-processestoruntests,eithertoruntheminparallel,orbecausesub-processbehavior
is an important part of the system under test. Measuring coverage in those sub-processes can be tricky because you
have to modify the code spawning the process to invoke coverage.py.
There’s an easier way to do it: coverage.py includes a function,coverage.process_startup() designed to be
invokedwhenPythonstarts. Itexaminesthe COVERAGE_PROCESS_STARTenvironmentvariable,andifitisset,begins
coverage measurement. The environment variable’s value will be used as the name of theconfiguration fileto use.
Note: Thesubprocessonlyseesoptionsintheconfigurationfile. Optionssetonthecommandlinewillnotbeusedin
the subprocesses.
Note: If you have subprocesses created with multiprocessing, the --concurrency=multiprocessing
command-line option should take care of everything for you. SeeExecution: coverage runfor details.
When using this technique, be sure to set the parallel option to true so that multiple coverage.py runs will each write
their data to a distinct file.
6.7.1 Configuring Python for sub-process measurement
Measuring coverage in sub-processes is a little tricky. When you spawn a sub-process, you are invoking Python to
run your program. Usually, to get coverage measurement, you have to use coverage.py to run your program. Your
sub-process won’t be using coverage.py, so we have to convince Python to use coverage.py even when not explicitly
invoked.
Todothat,we’llconfigurePythontorunalittlecoverage.pycodewhenitstarts. Thatcodewilllookforanenvironment
variable that tells it to start coverage measurement at the start of the process.
To arrange all this, you have to do two things: set a value for theCOVERAGE_PROCESS_START environment variable,
and then configure Python to invokecoverage.process_startup()when Python processes start.
How you setCOVERAGE_PROCESS_START depends on the details of how you create sub-processes. As long as the
environment variable is visible in your sub-process, it will work.
You can configure your Python installation to invoke theprocess_startupfunction in two ways:
1. Create or append to sitecustomize.py to add these lines:
import coverage
coverage.process_startup()
2. Create a .pth file in your Python installation containing:
42 Chapter 6. More information

Coverage.py, Release 7.2.2
import coverage ; coverage.process_startup()
The sitecustomize.py technique is cleaner, but may involve modifying an existing sitecustomize.py, since there can be
only one. If there is no sitecustomize.py already, you can create it in any directory on the Python path.
The .pth technique seems like a hack, but works, and is documented behavior. On the plus side, you can create the file
with any name you like so you don’t have to coordinate with other .pth files. On the minus side, you have to create the
file in a system-defined directory, so you may need privileges to write it.
Notethatifyouuseoneofthesetechniques,youmustundothemifyouuninstallcoverage.py,sinceyouwillbetryingto
importitduringPythonstart-up. Besuretoremovethechangewhenyouuninstallcoverage.py,oruseamoredefensive
approach to importing it.
6.7.2 Process termination
To successfully write a coverage data file, the Python sub-process under analysis must shut down cleanly and have a
chanceforcoverage.pytorunitsterminationcode. Itwilldothatwhentheprocessendsnaturally,orwhenaSIGTERM
signal is received.
Coverage.py usesatexit to handle usual process ends, and asignal handler to catch SIGTERM signals.
Otherwaysofendingaprocess,likeSIGKILLor os._exit,willpreventcoverage.pyfromwritingitsdatafile,leaving
you with incomplete or non-existent coverage data.
6.8 Measurement contexts
New in version 5.0.
Coverage.py measures whether code was run, but it can also record the context in which it was run. This can provide
more information to help you understand the behavior of your tests.
There are two kinds of context: static and dynamic. Static contexts are fixed for an entire run, and are set explicitly
with an option. Dynamic contexts change over the course of a single run.
6.8.1 Static contexts
Astaticcontextissetbyanoptionwhenyouruncoverage.py. Thevalueisfixedforthedurationofarun. Theycanbe
any text you like, for example, “python3” or “with_numpy”. The context is recorded with the data.
When youcombine multiple data filestogether, they can have differing contexts. All of the information is retained, so
that the different contexts are correctly recorded in the combined file.
A static context is specified with the--context=CONTEXT option to the coverage run command, or the [run]
contextsetting in the configuration file.
6.8. Measurement contexts 43

Coverage.py, Release 7.2.2
6.8.2 Dynamic contexts
Dynamiccontextsarefoundduringexecution. Theyaremostcommonlyusedtoanswerthequestion“whattestranthis
line?,” but have been generalized to allow any kind of context tracking. As execution proceeds, the dynamic context
changes to record the context of execution. Separate data is recorded for each context, so that it can be analyzed later.
There are three ways to enable dynamic contexts:
• you can set the[run] dynamic_context option in your .coveragerc file, or
• you can enable adynamic context switcherplugin, or
• another tool (such as a test runner) can call theCoverage.switch_context() method to set the context ex-
plicitly. The pytest plugin pytest-cov has a--cov-context option that uses this to set the dynamic context for
each test.
The [run] dynamic_context setting has only one option now. Set it totest_function to start a new dynamic
context for every test function:
[run]
dynamic_context = test_function
Each test function you run will be considered a separate dynamic context, and coverage data will be segregated for
each. A test function is any function whose name starts with “test”.
If you have both a static context and a dynamic context, they are joined with a pipe symbol to be recorded as a single
string.
Initially, when your program starts running, the dynamic context is an empty string. Any code measured before a
dynamiccontextissetwillberecordedinthisemptycontext. Forexample,ifyouarerecordingtestnamesascontexts,
then the code run by the test runner before (and between) tests will be in the empty context.
Dynamic contexts can be explicitly disabled by settingdynamic_contextto none.
6.8.3 Context reporting
The coverage report and coverage html commands both accept--contextsoption, a comma-separated list of
regular expressions. The report will be limited to the contexts that match one of those patterns.
The coverage html command also has--show-contexts. If set, the HTML report will include an annotation on
eachcoveredlineindicatingthenumberofcontextsthatexecutedtheline. Clickingtheannotationdisplaysalistofthe
contexts.
6.8.4 Raw data
Formoreadvancedreportingoranalysis,the.coveragedatafileisaSQLitedatabase. See Coverage.pydatabaseschema
for details.
44 Chapter 6. More information

Coverage.py, Release 7.2.2
6.9 Coverage.py API
There are a few different ways to use coverage.py programmatically.
The API to coverage.py is in a module calledcoverage. Most of the interface is in thecoverage.Coverage class.
MethodsontheCoverageobjectcorrespondroughlytooperationsavailableinthecommandlineinterface. Forexample,
a simple use would be:
import coverage
cov = coverage.Coverage()
cov.start()
# .. call your code ..
cov.stop()
cov.save()
cov.html_report()
Any of the methods can raise specialized exceptions described inCoverage exceptions.
Coverage.py supports plugins that can change its behavior, to collect information from non-Python files, or to perform
complex configuration. SeePlug-in classesfor details.
If you want to access the data that coverage.py has collected, thecoverage.CoverageData class provides an API to
read coverage.py data files.
Note: Only the documented portions of the API are supported. Other names you may find in modules or objects can
change their behavior at any time. Please limit yourself to documented methods to avoid problems.
For more intensive data use, you might want to access the coverage.py database file directly. The schema is subject to
change, so this is for advanced uses only.Coverage.py database schemaexplains more.
6.9.1 The Coverage class
class coverage.Coverage(data_file=MISSING, data_suffix=None,cover_pylib=None, auto_data=False,
timid=None,branch=None, config_file=True,source=None,source_pkgs=None,
omit=None, include=None,debug=None, concurrency=None,
check_preimported=False,context=None,messages=False)
Programmatic access to coverage.py.
To use:
from coverage import Coverage
cov = Coverage()
cov.start()
#.. call your code ..
cov.stop()
cov.html_report(directory='covhtml')
6.9. Coverage.py API 45

Coverage.py, Release 7.2.2
Note: inkeepingwithPythoncustom,namesstartingwithunderscorearenotpartofthepublicAPI.Theymight
stop working at any point. Please limit yourself to documented methods to avoid problems.
Methods can raise any of the exceptions described inCoverage exceptions.
Parameters
• data_file (Optional[Union[FilePath , DefaultValue]] ) –
• data_suffix (Optional[Union[str, bool]] ) –
• cover_pylib (Optional[bool]) –
• auto_data (bool) –
• timid (Optional[bool]) –
• branch (Optional[bool]) –
• config_file (Union[FilePath , bool] ) –
• source (Optional[Iterable[str]]) –
• source_pkgs (Optional[Iterable[str]]) –
• omit(Optional[Union[str, Iterable[str]]] ) –
• include(Optional[Union[str, Iterable[str]]] ) –
• debug (Optional[Iterable[str]]) –
• concurrency (Optional[Union[str, Iterable[str]]] ) –
• check_preimported (bool) –
• context(Optional[str]) –
• messages (bool) –
__init__(data_file=MISSING, data_suffix=None,cover_pylib=None, auto_data=False,timid=None,
branch=None,config_file=True,source=None, source_pkgs=None,omit=None, include=None,
debug=None,concurrency=None,check_preimported=False,context=None,messages=False)
Manyoftheseargumentsduplicateandoverridevaluesthatcanbeprovidedinaconfigurationfile. Param-
eters that are missing here will use values from the config file.
data_fileis the base name of the data file to use. The config value defaults to “.coverage”. None can be
providedtopreventwritingadatafile. data_suffixisappended(withadot)to data_filetocreatethefinalfile
name. Ifdata_suffixissimplyTrue,thenasuffixiscreatedwiththemachineandprocessidentityincluded.
cover_pylibisabooleandeterminingwhetherPythoncodeinstalledwiththePythoninterpreterismeasured.
This includes the Python standard library and any packages installed with the interpreter.
If auto_data is true, then any existing data file will be read when coverage measurement starts, and data
will be saved automatically when measurement stops.
If timid is true, then a slower and simpler trace function will be used. This is important for some environ-
ments where manipulation of tracing functions breaks the faster trace function.
If branchis true, then branch coverage will be measured in addition to the usual statement coverage.
config_filedetermines what configuration file to read:
• If it is “.coveragerc”, it is interpreted as if it were True, for backward compatibility.
• If it is a string, it is the name of the file to read. If the file can’t be read, it is an error.
• If it is True, then a few standard files names are tried (“.coveragerc”, “setup.cfg”, “tox.ini”). It is not
an error for these files to not be found.
46 Chapter 6. More information

Coverage.py, Release 7.2.2
• If it is False, then no configuration file is read.
sourceis a list of file paths or package names. Only code located in the trees indicated by the file paths or
package names will be measured.
source_pkgs is a list of package names. It works the same assource, but can be used to name packages
where the name can also be interpreted as a file path.
includeandomit are lists of file name patterns. Files that matchincludewill be measured, files that match
omit will not. Each will also accept a single string argument.
debug is a list of strings indicating what debugging information is desired.
concurrencyis a string indicating the concurrency library being used in the measured code. Without this,
coverage.py will get incorrect results if these libraries are in use. Valid strings are “greenlet”, “eventlet”,
“gevent”, “multiprocessing”, or “thread” (the default). This can also be a list of these strings.
If check_preimportedis true, then when coverage is started, the already-imported files will be checked to
see if they should be measured by coverage. Importing measured files before coverage is started can mean
that code is missed.
context is a string to use as thestatic contextlabel for collected data.
If messagesis true, some messages will be printed to stdout indicating what is happening.
New in version 4.0: Theconcurrencyparameter.
New in version 4.2: Theconcurrencyparameter can now be a list of strings.
New in version 5.0: Thecheck_preimportedand context parameters.
New in version 5.3: Thesource_pkgsparameter.
New in version 6.0: Themessagesparameter.
Parameters
• data_file (Optional[Union[str, PathLike, DefaultValue]] ) –
• data_suffix(Optional[Union[str, bool]] ) –
• cover_pylib(Optional[bool]) –
• auto_data (bool) –
• timid (Optional[bool]) –
• branch (Optional[bool]) –
• config_file(Union[str, PathLike, bool] ) –
• source(Optional[Iterable[str]]) –
• source_pkgs(Optional[Iterable[str]]) –
• omit(Optional[Union[str, Iterable[str]]] ) –
• include(Optional[Union[str, Iterable[str]]] ) –
• debug(Optional[Iterable[str]]) –
• concurrency(Optional[Union[str, Iterable[str]]] ) –
• check_preimported (bool) –
• context(Optional[str]) –
• messages(bool) –
6.9. Coverage.py API 47

Coverage.py, Release 7.2.2
Return type
None
analysis(morf )
Likeanalysis2but doesn’t return excluded line numbers.
Parameters
morf (Union[module, str] ) –
Return type
Tuple[str,List[int], List[int], str]
analysis2(morf )
Analyze a module.
morf is a module or a file name. It will be analyzed to determine its coverage statistics. The return value
is a 5-tuple:
• The file name for the module.
• A list of line numbers of executable statements.
• A list of line numbers of excluded statements.
• A list of line numbers of statements not run (missing from execution).
• A readable formatted string of the missing line numbers.
The analysis uses the source file itself and the current measured coverage data.
Parameters
morf (Union[module, str] ) –
Return type
Tuple[str,List[int], List[int], List[int], str]
annotate(morfs=None,directory=None,ignore_errors=None, omit=None,include=None, contexts=None)
Annotate a list of modules.
Note: This method has been obsoleted by more modern reporting tools, including thehtml_report()
method. It will be removed in a future version.
Each module inmorfs is annotated. The source is written to a new file, named with a “,cover” suffix, with
eachlineprefixedwithamarkertoindicatethecoverageoftheline. Coveredlineshave“>”,excludedlines
have “-”, and missing lines have “!”.
See report() for other arguments.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• directory (Optional[str]) –
• ignore_errors(Optional[bool]) –
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• contexts(Optional[List[str]]) –
Return type
None
48 Chapter 6. More information

Coverage.py, Release 7.2.2
clear_exclude(which=/quotesingle.ts1exclude/quotesingle.ts1)
Clear the exclude list.
Parameters
which (str) –
Return type
None
combine(data_paths=None,strict=False, keep=False)
Combine together a number of similarly-named coverage data files.
Allcoveragedatafileswhosenamestartswith data_file(fromthecoverage()constructor)willberead,and
combined together into the current measurements.
data_paths is a list of files or directories from which data should be combined. If no list is passed, then
the data files from the directory indicated by the current data file (probably the current directory) will be
combined.
If strict is true, then it is an error to attempt to combine when there are no data files to combine.
If keepis true, then original input data files won’t be deleted.
New in version 4.0: Thedata_pathsparameter.
New in version 4.3: Thestrict parameter.
Parameters
• data_paths(Optional[Iterable[str]]) –
• strict (bool) –
• keep(bool) –
Return type
None
classmethod current ()
Get the latest startedCoverageinstance, if any.
Returns: aCoverageinstance, or None.
New in version 5.0.
Return type
Optional[Coverage]
erase()
Erase previously collected coverage data.
This removes the in-memory data collected in this session as well as discarding the data file.
Return type
None
exclude(regex, which=/quotesingle.ts1exclude/quotesingle.ts1)
Exclude source lines from execution consideration.
A number of lists of regular expressions are maintained. Each list selects lines that are treated differently
during reporting.
whichdetermineswhichlistismodified. The“exclude”listselectslinesthatarenotconsideredexecutable
at all. The “partial” list indicates lines with branches that are not taken.
6.9. Coverage.py API 49

Coverage.py, Release 7.2.2
regex is a regular expression. The regex is added to the specified list. If any of the regexes in the list is
found in a line, the line is marked for special treatment during reporting.
Parameters
• regex(str) –
• which (str) –
Return type
None
get_data()
Get the collected data.
Also warn about various problems collecting data.
Returns acoverage.CoverageData, the collected coverage data.
New in version 4.0.
Return type
CoverageData
get_exclude_list(which=/quotesingle.ts1exclude/quotesingle.ts1)
Return a list of excluded regex strings.
whichindicates which list is desired. Seeexclude() for the lists that are available, and their meaning.
Parameters
which (str) –
Return type
List[str]
get_option(option_name)
Get an option from the configuration.
option_nameis a colon-separated string indicating the section and option name. For example, thebranch
option in the[run] section of the config file would be indicated with“run:branch”.
Returns the value of the option. The type depends on the option selected.
As a special case, anoption_name of "paths" will return an dictionary with the entire[paths] section
value.
New in version 4.0.
Parameters
option_name (str) –
Return type
Optional[Union[bool, int, float, str,List[str]]]
html_report(morfs=None,directory=None, ignore_errors=None, omit=None, include=None,
extra_css=None,title=None,skip_covered=None,show_contexts=None, contexts=None,
skip_empty=None,precision=None)
Generate an HTML report.
The HTML is written todirectory. The file “index.html” is the overview starting point, with links to more
detailed pages for individual modules.
extra_cssis a path to a file of other CSS to apply on the page. It will be copied into the HTML directory.
titleis a text string (not HTML) to use as the title of the HTML report.
50 Chapter 6. More information

Coverage.py, Release 7.2.2
See report() for other arguments.
Returns a float, the total percentage covered.
Note: The HTML report files are generated incrementally based on the source files and coverage results.
If you modify the report files, the changes will not be considered. You should be careful about changing
the files in the report folder.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• directory (Optional[str]) –
• ignore_errors(Optional[bool]) –
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• extra_css (Optional[str]) –
• title(Optional[str]) –
• skip_covered (Optional[bool]) –
• show_contexts(Optional[bool]) –
• contexts(Optional[List[str]]) –
• skip_empty(Optional[bool]) –
• precision (Optional[int]) –
Return type
float
json_report(morfs=None,outfile=None, ignore_errors=None,omit=None, include=None,contexts=None,
pretty_print=None, show_contexts=None)
Generate a JSON report of coverage results.
Eachmodulein morfsisincludedinthereport. outfileisthepathtowritethefileto,“-”willwritetostdout.
pretty_print is a boolean, whether to pretty-print the JSON output or not.
See report() for other arguments.
Returns a float, the total percentage covered.
New in version 5.0.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• outfile(Optional[str]) –
• ignore_errors(Optional[bool]) –
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• contexts (Optional[List[str]]) –
• pretty_print(Optional[bool]) –
6.9. Coverage.py API 51

Coverage.py, Release 7.2.2
• show_contexts(Optional[bool]) –
Return type
float
lcov_report(morfs=None,outfile=None, ignore_errors=None,omit=None, include=None,contexts=None)
Generate an LCOV report of coverage results.
Each module in ‘morfs’ is included in the report. ‘outfile’ is the path to write the file to, “-” will write to
stdout.
See :meth ‘report’ for other arguments.
New in version 6.3.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• outfile(Optional[str]) –
• ignore_errors(Optional[bool]) –
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• contexts (Optional[List[str]]) –
Return type
float
load()
Load previously-collected coverage data from the data file.
Return type
None
report(morfs=None,show_missing=None,ignore_errors=None, file=None,omit=None, include=None,
skip_covered=None,contexts=None, skip_empty=None,precision=None, sort=None,
output_format=None)
Write a textual summary report tofile.
Each module inmorfs is listed, with counts of statements, executed statements, missing statements, and a
list of lines missed.
If show_missingis true, then details of which lines or branches are missing will be included in the report.
Ifignore_errorsis true, then a failure while reporting a single file will not stop the entire report.
fileis a file-like object, suitable for writing.
output_format determines the format, either “text” (the default), “markdown”, or “total”.
include is a list of file name patterns. Files that match will be included in the report. Files matchingomit
will not be included in the report.
Ifskip_coveredis true, don’t report on files with 100% coverage.
Ifskip_emptyis true, don’t report on empty files (those that have no statements).
contexts is a list of regular expression strings. Only data fromdynamic contextsthat match one of those
expressions (usingre.search) will be included in the report.
precisionis the number of digits to display after the decimal point for percentages.
All of the arguments default to the settings read from theconfiguration file.
52 Chapter 6. More information

Coverage.py, Release 7.2.2
Returns a float, the total percentage covered.
New in version 4.0: Theskip_coveredparameter.
New in version 5.0: Thecontextsand skip_emptyparameters.
New in version 5.2: Theprecisionparameter.
New in version 7.0: Theformat parameter.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• show_missing(Optional[bool]) –
• ignore_errors(Optional[bool]) –
• file(Optional[IO[str]]) –
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• skip_covered (Optional[bool]) –
• contexts(Optional[List[str]]) –
• skip_empty(Optional[bool]) –
• precision (Optional[int]) –
• sort(Optional[str]) –
• output_format(Optional[str]) –
Return type
float
save()
Save the collected coverage data to the data file.
Return type
None
set_option(option_name,value)
Set an option in the configuration.
option_nameis a colon-separated string indicating the section and option name. For example, thebranch
option in the[run] section of the config file would be indicated with"run:branch".
valueis the new value for the option. This should be an appropriate Python value. For example, use True
for booleans, not the string"True".
As an example, calling:
cov.set_option("run:branch", True)
has the same effect as this configuration file:
[run]
branch = True
As a special case, anoption_nameof "paths" will replace the entire[paths] section. The value should
be a dictionary.
New in version 4.0.
6.9. Coverage.py API 53

Coverage.py, Release 7.2.2
Parameters
• option_name(str) –
• value (Union[bool, int, float, str, Iterable[str], None,
Mapping[str, Optional[Union[bool, int, float, str,
Iterable[str]]]]]) –
Return type
None
start()
Start measuring code coverage.
Coverage measurement only occurs in functions called afterstart() is invoked. Statements in the same
scope asstart()won’t be measured.
Once you invokestart(), you must also callstop() eventually, or your process might not shut down
cleanly.
Return type
None
stop()
Stop measuring code coverage.
Return type
None
switch_context(new_context)
Switch to a new dynamic context.
new_context is a string to use as thedynamic contextlabel for collected data. If astatic contextis in use,
the static and dynamic context labels will be joined together with a pipe character.
Coverage collection must be started already.
New in version 5.0.
Parameters
new_context (str) –
Return type
None
xml_report(morfs=None, outfile=None,ignore_errors=None, omit=None,include=None,contexts=None,
skip_empty=None)
Generate an XML report of coverage results.
The report is compatible with Cobertura reports.
Eachmodulein morfsisincludedinthereport. outfileisthepathtowritethefileto,“-”willwritetostdout.
See report() for other arguments.
Returns a float, the total percentage covered.
Parameters
• morfs(Optional[Iterable[Union[module, str]]] ) –
• outfile(Optional[str]) –
• ignore_errors(Optional[bool]) –
54 Chapter 6. More information

Coverage.py, Release 7.2.2
• omit(Optional[Union[str, List[str]]] ) –
• include(Optional[Union[str, List[str]]] ) –
• contexts(Optional[List[str]]) –
• skip_empty(Optional[bool]) –
Return type
float
6.9.2 Coverage exceptions
class coverage.exceptions.CoverageException
The base class of all exceptions raised by Coverage.py.
Exceptions coverage.py can raise.
exception coverage.exceptions.ConfigError
A problem with a config file, or a value in one.
exception coverage.exceptions.CoverageWarning
A warning from Coverage.py.
exception coverage.exceptions.DataError
An error in using a data file.
exception coverage.exceptions.NoCode
We couldn’t find any code at all.
exception coverage.exceptions.NoDataError
We didn’t have data to work with.
exception coverage.exceptions.NoSource
We couldn’t find the source for a module.
exception coverage.exceptions.NotPython
A source file turned out not to be parsable Python.
exception coverage.exceptions.PluginError
A plugin misbehaved.
6.9.3 coverage module
The most important thing in the coverage module is thecoverage.Coverage class, described inThe Coverage class,
but there are a few other things also.
coverage.version_info
A tuple of five elements, similar tosys.version_info: major, minor, micro, releaselevel, andserial. All values
except releaselevel are integers; the release level is'alpha', 'beta', 'candidate', or 'final'. Unlike sys.
version_info, the elements are not available by name.
coverage.__version__
A string with the version of coverage.py, for example,"5.0b2".
class coverage.CoverageException
The base class of all exceptions raised by Coverage.py.
6.9. Coverage.py API 55

Coverage.py, Release 7.2.2
Starting coverage.py automatically
This function is used to start coverage measurement automatically when Python starts. SeeMeasuring sub-processes
for details.
coverage.process_startup()
Call this at Python start-up to perhaps measure coverage.
If the environment variable COVERAGE_PROCESS_START is defined, coverage measurement is started. The
value of the variable is the config file to use.
There are two ways to configure your Python installation to invoke this function when Python starts:
1. Create or append to sitecustomize.py to add these lines:
import coverage
coverage.process_startup()
2. Create a .pth file in your Python installation containing:
import coverage ; coverage.process_startup()
Returns theCoverage instance that was started, or None if it was not started by this call.
Return type
Optional[Coverage]
6.9.4 Plug-in classes
New in version 4.0.
Plug-in interfaces for coverage.py.
Coverage.py supports a few different kinds of plug-ins that change its behavior:
• File tracers implement tracing of non-Python file types.
• Configurers add custom configuration, using Python code to change the configuration.
• Dynamic context switchers decide when the dynamic context has changed, for example, to record what test
function produced the coverage.
To write a coverage.py plug-in, create a module with a subclass ofCoveragePlugin. You will override methods in
your class to participate in various aspects of coverage.py’s processing. Different types of plug-ins have to override
different methods.
Any plug-in can optionally implementsys_info()to provide debugging information about their operation.
Your module must also contain acoverage_init function that registers an instance of your plug-in class:
import coverage
class MyPlugin (coverage.CoveragePlugin):
...
def coverage_init(reg, options):
reg.add_file_tracer(MyPlugin())
56 Chapter 6. More information

Coverage.py, Release 7.2.2
You use thereg parameter passed to yourcoverage_init function to register your plug-in object. The registration
method you call depends on what kind of plug-in it is.
If your plug-in takes options, theoptions parameter is a dictionary of your plug-in’s options from the coverage.py
configuration file. Use them however you want to configure your object before registering it.
Coverage.pywillstoreitsowninformationonyourplug-inobject,usingattributeswhosenamesstartwith _coverage_.
Don’t be startled.
Warning: Plug-ins are imported by coverage.py before it begins measuring code. If you write a plugin in your
ownproject,itmightimportyourproductcodebeforecoverage.pycanstartmeasuring. Thiscanresultinyourown
code being reported as missing.
One solution is to put your plugins in your project tree, but not in your importable Python package.
File Tracers
Filetracersimplementmeasurementsupportfornon-Pythonfiles. Filetracersimplementthe file_tracer()method
to claim files and thefile_reporter() method to report on those files.
In yourcoverage_init function, use theadd_file_tracermethod to register your file tracer.
Configurers
New in version 4.5.
Configurersmodifytheconfigurationofcoverage.pyduringstart-up. Configurersimplementthe configure()method
to change the configuration.
In yourcoverage_init function, use theadd_configurer method to register your configurer.
Dynamic Context Switchers
New in version 5.0.
Dynamic context switcher plugins implement thedynamic_context() method to dynamically compute the context
label for each measured frame.
Computed context labels are useful when you want to group measured data without modifying the source code.
For example, you could write a plugin that checksframe.f_codeto inspect the currently executed method, and set the
contextlabeltoafullyqualifiedmethodnameifit’saninstancemethodof unittest.TestCaseandthemethodnamestarts
with ‘test’. Such a plugin would provide basic coverage grouping by test and could be used with test runners that have
no built-in coveragepy support.
Inyour coverage_initfunction,usethe add_dynamic_contextmethodtoregisteryourdynamiccontextswitcher.
6.9. Coverage.py API 57

Coverage.py, Release 7.2.2
The CoveragePlugin class
class coverage.CoveragePlugin
Base class for coverage.py plug-ins.
file_tracer(filename)
Get aFileTracer object for a file.
Plug-in type: file tracer.
Every Python source file is offered to your plug-in to give it a chance to take responsibility for tracing the
file. If your plug-in can handle the file, it should return aFileTracer object. Otherwise return None.
There is no way to register your plug-in for particular files. Instead, this method is invoked for all files as
they are executed, and the plug-in decides whether it can trace the file or not. Be prepared forfilenameto
refer to all kinds of files that have nothing to do with your plug-in.
ThefilenamewillbeaPythonfilebeingexecuted. Therearetwobroadcategoriesofbehaviorforaplug-in,
depending on the kind of files your plug-in supports:
• Staticfilenames: eachofyouroriginalsourcefileshasbeenconvertedintoadistinctPythonfile. Your
plug-in is invoked with the Python file name, and it maps it back to its original source file.
• Dynamic file names: all of your source files are executed by the same Python file. In this case, your
plug-in implements FileTracer.dynamic_source_filename() to provide the actual source file
for each execution frame.
filenameisastring,thepathtothefilebeingconsidered. Thisistheabsoluterealpathtothefile. Ifyouare
comparing to other paths, be sure to take this into account.
Returns aFileTracer object to use to tracefilename, or None if this plug-in cannot trace this file.
Parameters
filename (str) –
Return type
Optional[FileTracer]
file_reporter(filename)
Get theFileReporter class to use for a file.
Plug-in type: file tracer.
Thiswillonlybeinvokedif filenamereturnsnon-Nonefrom file_tracer(). It’sanerrortoreturnNone
from this method.
Returns aFileReporter object to use to report onfilename, or the string“python”to have coverage.py
treat the file as Python.
Parameters
filename (str) –
Return type
Union[FileReporter, str]
dynamic_context(frame)
Get the dynamically computed context label forframe.
Plug-in type: dynamic context.
Thismethodisinvokedforeachframewhenoutsideofadynamiccontext,toseeifanewdynamiccontext
should be started. If it returns a string, a new context label is set for this and deeper frames. The dynamic
context ends when this frame returns.
58 Chapter 6. More information

Coverage.py, Release 7.2.2
Returns a string to start a new dynamic context, or None if no new context should be started.
Parameters
frame (frame) –
Return type
Optional[str]
find_executable_files(src_dir)
Yield all of the executable files insrc_dir, recursively.
Plug-in type: file tracer.
Executability is a plug-in-specific property, but generally means files which would have been considered
for coverage analysis, had they been included automatically.
Returnsoryieldsasequenceofstrings,thepathstofilesthatcouldhavebeenexecuted,includingfilesthat
had been executed.
Parameters
src_dir(str) –
Return type
Iterable[str]
configure(config)
Modify the configuration of coverage.py.
Plug-in type: configurer.
Thismethodiscalledduringcoverage.pystart-up,togiveyourplug-inachancetochangetheconfiguration.
Theconfigparameterisanobjectwith get_option()and set_option()methods. Donotcallanyother
methods on theconfigobject.
Parameters
config (TConfigurable) –
Return type
None
sys_info()
Get a list of information useful for debugging.
Plug-in type: any.
This method will be invoked for--debug=sys. Your plug-in can return any information it wants to be
displayed.
Returns a list of pairs:[(name, value), ...].
Return type
Iterable[Tuple[str,Any]]
6.9. Coverage.py API 59

Coverage.py, Release 7.2.2
The FileTracer class
class coverage.FileTracer
Support needed for files during the execution phase.
File tracer plug-ins implement subclasses of FileTracer to return from theirfile_tracer()method.
You may construct this object fromCoveragePlugin.file_tracer() any way you like. A natural choice
would be to pass the file name given tofile_tracer.
FileTracerobjects should only be created in theCoveragePlugin.file_tracer() method.
SeeHow coverage.py worksfor details of the different coverage.py phases.
source_filename()
The source file name for this file.
This may be any file name you like. A key responsibility of a plug-in is to own the mapping from Python
execution back to whatever source file name was originally the source of the code.
See CoveragePlugin.file_tracer() for details about static and dynamic file names.
Returns the file name to credit with this execution.
Return type
str
has_dynamic_source_filename()
Does this FileTracer have dynamic source file names?
FileTracers can provide dynamically determined file names by implementing
dynamic_source_filename(). Invoking that function is expensive. To determine whether
to invoke it, coverage.py uses the result of this function to know if it needs to bother invoking
dynamic_source_filename().
See CoveragePlugin.file_tracer() for details about static and dynamic file names.
Returns True ifdynamic_source_filename() should be called to get dynamic source file names.
Return type
bool
dynamic_source_filename(filename,frame)
Get a dynamically computed source file name.
Some plug-ins need to compute the source file name dynamically for each frame.
This function will not be invoked ifhas_dynamic_source_filename()returns False.
Returns the source file name for this frame, or None if this frame shouldn’t be measured.
Parameters
• filename(str) –
• frame(frame) –
Return type
Optional[str]
60 Chapter 6. More information

Coverage.py, Release 7.2.2
line_number_range(frame)
Get the range of source line numbers for a given a call frame.
The call frame is examined, and the source line number in the original file is returned. The return value
is a pair of numbers, the starting line number and the ending line number, both inclusive. For example,
returning (5, 7) means that lines 5, 6, and 7 should be considered executed.
This function might decide that the frame doesn’t indicate any lines from the source file were executed.
Return (-1, -1) in this case to tell coverage.py that no lines should be recorded for this frame.
Parameters
frame (frame) –
Return type
Tuple[int, int]
The FileReporter class
class coverage.FileReporter(filename)
Support needed for files during the analysis and reporting phases.
File tracer plug-ins implement a subclass ofFileReporter, and return instances from theirCoveragePlugin.
file_reporter()method.
There are many methods here, but onlylines()is required, to provide the set of executable lines in the file.
SeeHow coverage.py worksfor details of the different coverage.py phases.
Parameters
filename (str) –
relative_filename()
Get the relative file name for this file.
Thisfilepathwillbedisplayedinreports. Thedefaultimplementationwillsupplytheactualproject-relative
file path. You only need to supply this method if you have an unusual syntax for file paths.
Return type
str
source()
Get the source for the file.
Returns a Unicode string.
Thebaseimplementationsimplyreadsthe self.filenamefileanddecodesitasUTF-8. Overridethismethod
if your file isn’t readable as a text file, or if you need other encoding support.
Return type
str
lines()
Get the executable lines in this file.
Your plug-in must determine which lines in the file were possibly executable. This method returns a set of
those line numbers.
Returns a set of line numbers.
Return type
Set[int]
6.9. Coverage.py API 61

Coverage.py, Release 7.2.2
excluded_lines()
Get the excluded executable lines in this file.
Your plug-in can use any method it likes to allow the user to exclude executable lines from consideration.
Returns a set of line numbers.
The base implementation returns the empty set.
Return type
Set[int]
translate_lines(lines)
Translate recorded lines into reported lines.
Somefileformatswillwanttoreportlinesslightlydifferentlythantheyarerecorded. Forexample, Python
records the last line of a multi-line statement, but reports are nicer if they mention the first line.
Your plug-in can optionally define this method to perform these kinds of adjustment.
lines is a sequence of integers, the recorded line numbers.
Returns a set of integers, the adjusted line numbers.
The base implementation returns the numbers unchanged.
Parameters
lines (Iterable[int]) –
Return type
Set[int]
arcs()
Get the executable arcs in this file.
To support branch coverage, your plug-in needs to be able to indicate possible execution paths, as a set of
linenumberpairs. Eachpairisa (prev,next) pairindicatingthatexecutioncantransitionfromthe prevline
number to thenext line number.
Returns a set of pairs of line numbers. The default implementation returns an empty set.
Return type
Set[Tuple[int, int]]
no_branch_lines()
Get the lines excused from branch coverage in this file.
Your plug-in can use any method it likes to allow the user to exclude lines from consideration of branch
coverage.
Returns a set of line numbers.
The base implementation returns the empty set.
Return type
Set[int]
translate_arcs(arcs)
Translate recorded arcs into reported arcs.
Similar totranslate_lines(), but for arcs.arcsis a set of line number pairs.
Returns a set of line number pairs.
The default implementation returnsarcsunchanged.
62 Chapter 6. More information

Coverage.py, Release 7.2.2
Parameters
arcs(Iterable[Tuple[int, int]] ) –
Return type
Set[Tuple[int, int]]
exit_counts()
Get a count of exits from that each line.
To determine which lines are branches, coverage.py looks for lines that have more than one exit. This
function creates a dict mapping each executable line number to a count of how many exits it has.
To be honest, this feels wrong, and should be refactored. Let me know if you attempt to implement this
method in your plug-in...
Return type
Dict[int, int]
missing_arc_description(start,end, executed_arcs=None)
Provide an English sentence describing a missing arc.
The start and end arguments are the line numbers of the missing arc. Negative numbers indicate entering
or exiting code objects.
Theexecuted_arcsargument is a set of line number pairs, the arcs that were executed in this file.
By default, this simply returns the string “Line {start} didn’t jump to {end}”.
Parameters
• start(int) –
• end (int) –
• executed_arcs(Optional[Iterable[Tuple[int, int]]] ) –
Return type
str
source_token_lines()
Generate a series of tokenized lines, one for each line insource.
These tokens are used for syntax-colored reports.
Each line is a list of pairs, each pair is a token:
[('key', 'def'), ( 'ws', ' ' ), ( 'nam', 'hello'), ( 'op', '('), ... ]
Each pair has a token class, and the token text. The token classes are:
• 'com': a comment
• 'key': a keyword
• 'nam': a name, or identifier
• 'num': a number
• 'op': an operator
• 'str': a string literal
• 'ws': some white space
• 'txt': some other kind of text
6.9. Coverage.py API 63

Coverage.py, Release 7.2.2
If you concatenate all the token texts, and then join them with newlines, you should have your original
source back.
The default implementation simply returns each line tagged as'txt'.
Return type
Iterable[List[Tuple[str, str]]]
6.9.5 The CoverageData class
New in version 4.0.
class coverage.CoverageData(basename=None,suffix=None,no_disk=False, warn=None,debug=None)
Manages collected coverage data, including file storage.
ThisclassisthepublicsupportedAPItothedatathatcoverage.pycollectsduringprogramexecution. Itincludes
informationaboutwhatcodewasexecuted. Itdoesnotincludeinformationfromtheanalysisphase,todetermine
what lines could have been executed, or what lines were not executed.
Note: The data file is currently a SQLite database file, with adocumented schema. The schema is subject to
changethough,sobecarefulaboutqueryingitdirectly. UsethisAPIifyoucantoisolateyourselffromchanges.
There are a number of kinds of data that can be collected:
• lines: the line numbers of source lines that were executed. These are always available.
• arcs: pairs of source and destination line numbers for transitions between source lines. These are only
available if branch coverage was used.
• file tracer names: the module names of the file tracer plugins that handled each file in the data.
Lines, arcs, and file tracer names are stored for each source file. File names in this API are case-sensitive, even
on platforms with case-insensitive file systems.
A data file either stores lines, or arcs, but not both.
A data file is associated with the data when theCoverageData is created, using the parametersbasename,
suffix,and no_disk. Thebasenamecanbequeriedwith base_filename(),andtheactualfilenamebeingused
is available fromdata_filename().
To read an existing coverage.py data file, useread(). You can then access the line, arc, or file tracer data with
lines(), arcs(), orfile_tracer().
The has_arcs() method indicates whether arc data is available. You can get a set of the files in the data with
measured_files(). AswithmostPythoncontainers,youcandetermineifthereisanydataatallbyusingthis
object as a boolean value.
The contexts for each line in a file can be read withcontexts_by_lineno().
To limit querying to certain contexts, useset_query_context() or set_query_contexts(). These will
narrowthefocusofsubsequent lines(), arcs(),and contexts_by_lineno()calls. Thesetofallmeasured
context names can be retrieved withmeasured_contexts().
Mostdatafileswillbecreatedbycoverage.pyitself,butyoucanusemethodsheretocreatedatafilesifyoulike.
The add_lines(), add_arcs(),and add_file_tracers()methodsadddata,inwaysthatareconvenientfor
coverage.py.
To record data for contexts, useset_context() to set a context to be used for subsequentadd_lines() and
add_arcs()calls.
64 Chapter 6. More information

Coverage.py, Release 7.2.2
To add a source file without any measured data, usetouch_file(), ortouch_files() for a list of such files.
Write the data to its file withwrite().
You can clear the data in memory witherase(). Data for specific files can be removed from the database with
purge_files().
Two data collections can be combined by usingupdate()on oneCoverageData, passing it the other.
Data in aCoverageData can be serialized and deserialized withdumps()and loads().
Themethodsusedduringthecoverage.pycollectionphase( add_lines(), add_arcs(), set_context(),and
add_file_tracers()) are thread-safe. Other methods may not be.
Parameters
• basename (Optional[FilePath ]) –
• suffix (Optional[Union[str, bool]] ) –
• no_disk(bool) –
• warn (Optional[TWarnFn]) –
• debug (Optional[TDebugCtl]) –
__init__(basename=None, suffix=None,no_disk=False,warn=None,debug=None)
Create aCoverageData object to hold coverage-measured data.
Parameters
• basename (str) – the base name of the data file, defaulting to “.coverage”. This can be a
path to a file in another directory.
• suffix (str or bool ) – has the same meaning as the data_suffix argument to
coverage.Coverage.
• no_disk(bool) – if True, keep all data in memory, and don’t write any disk file.
• warn(Optional[TWarnFn])–awarningcallbackfunction,acceptingawarningmessage
argument.
• debug(Optional[TDebugCtl]) – aDebugControl object (optional)
Return type
None
add_arcs(arc_data)
Add measured arc data.
arc_datais a dictionary mapping file names to iterables of pairs of ints:
{ filename: { (l1,l2), (l1,l2), ... }, ...}
Parameters
arc_data (Mapping[str, Collection[Tuple[int, int]]] ) –
Return type
None
add_file_tracers(file_tracers)
Add per-file plugin information.
file_tracersis { filename: plugin_name, ... }
6.9. Coverage.py API 65

Coverage.py, Release 7.2.2
Parameters
file_tracers(Mapping[str, str] ) –
Return type
None
add_lines(line_data)
Add measured line data.
line_data is a dictionary mapping file names to iterables of ints:
{ filename: { line1, line2, ... }, ...}
Parameters
line_data (Mapping[str, Collection[int]] ) –
Return type
None
arcs(filename)
Get the list of arcs executed for a file.
If the file was not measured, returns None. A file might be measured, and have no arcs executed, in which
case an empty list is returned.
If the file was executed, returns a list of 2-tuples of integers. Each pair is a starting line number and an
ending line number for a transition from one line to another. The list is in no particular order.
Negativenumbershavespecialmeaning. Ifthestartinglinenumberis-N,itrepresentsanentrytothecode
object that starts at line N. If the ending ling number is -N, it’s an exit from the code object that starts at
line N.
Parameters
filename (str) –
Return type
Optional[List[Tuple[int, int]]]
base_filename()
The base filename for storing data.
New in version 5.0.
Return type
str
contexts_by_lineno(filename)
Get the contexts for each line in a file.
Returns
A dict mapping line numbers to a list of context names.
Parameters
filename (str) –
Return type
Dict[int,List[str]]
New in version 5.0.
66 Chapter 6. More information

Coverage.py, Release 7.2.2
data_filename()
Where is the data stored?
New in version 5.0.
Return type
str
dumps()
Serialize the current data to a byte string.
The format of the serialized data is not documented. It is only suitable for use withloads() in the same
version of coverage.py.
Note that this serialization is not what gets stored in coverage data files. This method is meant to produce
bytes that can be transmitted elsewhere and then deserialized withloads().
Returns
A byte string of serialized data.
Return type
bytes
New in version 5.0.
erase(parallel=False)
Erase the data in this object.
If parallel is true, then also deletes data files created from the basename by parallel-mode.
Parameters
parallel (bool) –
Return type
None
file_tracer(filename)
Get the plugin name of the file tracer for a file.
Returns the name of the plugin that handles this file. If the file was measured, but didn’t use a plugin, then
“” is returned. If the file was not measured, then None is returned.
Parameters
filename (str) –
Return type
Optional[str]
has_arcs()
Does the database have arcs (True) or lines (False).
Return type
bool
lines(filename)
Get the list of lines executed for a source file.
Ifthefilewasnotmeasured, returnsNone. Afilemightbemeasured,andhavenolinesexecuted, inwhich
case an empty list is returned.
If the file was executed, returns a list of integers, the line numbers executed in the file. The list is in no
particular order.
6.9. Coverage.py API 67

Coverage.py, Release 7.2.2
Parameters
filename (str) –
Return type
Optional[List[int]]
loads(data)
Deserialize data fromdumps().
Use with a newly-created emptyCoverageData object. It’s undefined what happens if the object already
has data in it.
Note that this is not for reading data from a coverage data file. It is only for use on data you produced with
dumps().
Parameters
data(bytes) – A byte string of serialized data produced bydumps().
Return type
None
New in version 5.0.
measured_contexts()
A set of all contexts that have been measured.
New in version 5.0.
Return type
Set[str]
measured_files()
A set of all files that have been measured.
Note that a file may be mentioned as measured even though no lines or arcs for that file are present in the
data.
Return type
Set[str]
purge_files(filenames)
Purge any existing coverage data for the givenfilenames.
New in version 7.2.
Parameters
filenames (Collection[str]) –
Return type
None
read()
Start using an existing data file.
Return type
None
set_context(context)
Set the current context for futureadd_lines() etc.
context isastr,thenameofthecontexttouseforthenextdataadditions. Thecontextpersistsuntilthenext
set_context().
New in version 5.0.
68 Chapter 6. More information

Coverage.py, Release 7.2.2
Parameters
context(Optional[str]) –
Return type
None
set_query_context(context)
Set a context for subsequent querying.
Thenext lines(), arcs(),or contexts_by_lineno()callswillbelimitedtoonlyonecontext. context
is a string which must match a context exactly. If it does not, no exception is raised, but queries will return
no data.
New in version 5.0.
Parameters
context(str) –
Return type
None
set_query_contexts(contexts)
Set a number of contexts for subsequent querying.
The nextlines(), arcs(), or contexts_by_lineno() calls will be limited to the specified contexts.
contexts is a list of Python regular expressions. Contexts will be matched usingre.search. Data will be
included in query results if they are part of any of the contexts matched.
New in version 5.0.
Parameters
contexts (Optional[Sequence[str]]) –
Return type
None
classmethod sys_info ()
Our information forCoverage.sys_info.
Returns a list of (key, value) pairs.
Return type
List[Tuple[str,Any]]
touch_file(filename,plugin_name=/quotesingle.ts1/quotesingle.ts1)
Ensure thatfilenameappears in the data, empty if needed.
plugin_nameis the name of the plugin responsible for this file. It is used to associate the right filereporter,
etc.
Parameters
• filename(str) –
• plugin_name(str) –
Return type
None
touch_files(filenames,plugin_name=None)
Ensure thatfilenamesappear in the data, empty if needed.
plugin_nameisthenameofthepluginresponsibleforthesefiles. Itisusedtoassociatetherightfilereporter,
etc.
6.9. Coverage.py API 69

Coverage.py, Release 7.2.2
Parameters
• filenames (Collection[str]) –
• plugin_name(Optional[str]) –
Return type
None
update(other_data, aliases=None)
Update this data with data from several otherCoverageData instances.
If aliases is provided, it’s aPathAliasesobject that is used to re-map paths to match the local machine’s.
Note: aliases is None only when called directly from the test suite.
Parameters
• other_data(CoverageData) –
• aliases(Optional[PathAliases]) –
Return type
None
write()
Ensure the data is written to the data file.
Return type
None
6.9.6 Coverage.py database schema
New in version 5.0.
Coverage.py stores data in a SQLite database, by default called.coverage. For most needs, theCoverageData API
will be sufficient, and should be preferred to accessing the database directly. Only advanced uses will need to use the
database.
The schema can change without changing the major version of coverage.py, so be careful when accessing the database
directly. Thecoverage_schematablehastheschemanumberofthedatabase. Theschemadescribedherecorresponds
to:
SCHEMA_VERSION = 7
You can use SQLite tools such as thesqlite3module in the Python standard library to access the data. Some data is
stored in a packed format that will need custom functions to access. Seeregister_sqlite_functions().
Database schema
This is the database schema:
CREATE TABLE coverage_schema (
-- One row, to record the version of the schema in this db.
version integer
);
CREATE TABLE meta (
-- Key-value pairs, to record metadata about the data

70 Chapter 6. More information

Coverage.py, Release 7.2.2
(continued from previous page)
key text,
value text,
unique (key)
-- Possible keys:
-- 'has_arcs' boolean -- Is this data recording branches?
-- 'sys_argv' text -- The coverage command line that recorded the data.
-- 'version' text -- The version of coverage.py that made the file.
-- 'when' text -- Datetime when the file was created.
);
CREATE TABLE file (
-- A row per file measured.
id integer primary key ,
path text,
unique (path)
);
CREATE TABLE context (
-- A row per context measured.
id integer primary key ,
context text,
unique (context)
);
CREATE TABLE line_bits (
-- If recording lines, a row per context per file executed.
-- All of the line numbers for that file/context are in one numbits.
file_id integer, -- foreign key to `file`.
context_id integer, -- foreign key to `context`.
numbits blob, -- see the numbits functions in coverage.numbits
foreign key (file_id) references file (id),
foreign key (context_id) references context (id),
unique (file_id, context_id)
);
CREATE TABLE arc (
-- If recording branches, a row per context per from/to line transition executed.
file_id integer, -- foreign key to `file`.
context_id integer, -- foreign key to `context`.
fromno integer, -- line number jumped from.
tono integer, -- line number jumped to.
foreign key (file_id) references file (id),
foreign key (context_id) references context (id),
unique (file_id, context_id, fromno, tono)
);
CREATE TABLE tracer (
-- A row per file indicating the tracer used for that file.
file_id integer primary key ,
tracer text,
foreign key (file_id) references file (id)
);
6.9. Coverage.py API 71

Coverage.py, Release 7.2.2
Numbits
Functions to manipulate packed binary representations of number sets.
To save space, coverage stores sets of line numbers in SQLite using a packed binary representation called a numbits.
A numbits is a set of positive integers.
A numbits is stored as a blob in the database. The exact meaning of the bytes in the blobs should be considered an
implementation detail that might change in the future. Use these functions to work with those binary blobs of data.
coverage.numbits.num_in_numbits(num,numbits)
Does the integernum appear innumbits?
Returns
A bool, True ifnum is a member ofnumbits.
Parameters
• num (int) –
• numbits(bytes) –
Return type
bool
coverage.numbits.numbits_any_intersection(numbits1, numbits2)
Is there any number that appears in both numbits?
Determinewhethertwonumbersetshaveanon-emptyintersection. Thisisfasterthancomputingtheintersection.
Returns
A bool, True if there is any number in bothnumbits1 andnumbits2.
Parameters
• numbits1 (bytes) –
• numbits2 (bytes) –
Return type
bool
coverage.numbits.numbits_intersection(numbits1,numbits2)
Compute the intersection of two numbits.
Returns
A new numbits, the intersectionnumbits1 andnumbits2.
Parameters
• numbits1 (bytes) –
• numbits2 (bytes) –
Return type
bytes
coverage.numbits.numbits_to_nums(numbits)
Convert a numbits into a list of numbers.
Parameters
numbits(bytes) – a binary blob, the packed number set.
Returns
A list of ints.
72 Chapter 6. More information

Coverage.py, Release 7.2.2
Return type
List[int]
When registered as a SQLite function byregister_sqlite_functions(), this returns a string, a JSON-
encoded list of ints.
coverage.numbits.numbits_union(numbits1, numbits2)
Compute the union of two numbits.
Returns
A new numbits, the union ofnumbits1and numbits2.
Parameters
• numbits1 (bytes) –
• numbits2 (bytes) –
Return type
bytes
coverage.numbits.nums_to_numbits(nums)
Convertnums into a numbits.
Parameters
nums(Iterable[int]) – a reusable iterable of integers, the line numbers to store.
Returns
A binary blob.
Return type
bytes
coverage.numbits.register_sqlite_functions(connection)
Define numbits functions in a SQLite connection.
This defines these functions for use in SQLite statements:
• numbits_union()
• numbits_intersection()
• numbits_any_intersection()
• num_in_numbits()
• numbits_to_nums()
connection is asqlite3.Connection object. After creating the connection, pass it to this function to register
the numbits functions. Then you can use numbits functions in your queries:
import sqlite3
from coverage.numbits import register_sqlite_functions
conn = sqlite3.connect( 'example.db')
register_sqlite_functions(conn)
c = conn.cursor()
# Kind of a nonsense query:
# Find all the files and contexts that executed line 47 in any file:
c.execute(
"select file_id, context_id from line_bits where num_in_numbits(?, numbits)",
(47,)
)
6.9. Coverage.py API 73

Coverage.py, Release 7.2.2
Parameters
connection (Connection) –
Return type
None
6.10 How coverage.py works
For advanced use of coverage.py, or just because you are curious, it helps to understand what’s happening behind the
scenes.
Coverage.py works in three phases:
• Execution: Coverage.py runs your code, and monitors it to see what lines were executed.
• Analysis: Coverage.py examines your code to determine what lines could have run.
• Reporting: Coverage.py combines the results of execution and analysis to produce a coverage number and an
indication of missing execution.
The execution phase is handled by thecoverage run command. The analysis and reporting phases are handled by
the reporting commands likecoverage report or coverage html .
As a short-hand, I say that coverage.py measures what lines were executed. But it collects more information than that.
Itcanmeasurewhatbranchesweretaken,andifyouhavecontextsenabled,foreachlineorbranch,itwillalsomeasure
what contexts they were executed in.
Let’s look at each phase in more detail.
6.10.1 Execution
At the heart of the execution phase is a trace function. This is a function that the Python interpreter invokes for each
line executed in a program. Coverage.py implements a trace function that records each file and line number as it is
executed.
Formoredetailsoftracefunctions,seethePythondocsforsys.settrace,orifyouarereallybrave,HowCtracefunctions
really work.
Executing a function for every line in your program can make execution very slow. Coverage.py’s trace function is
implemented in C to reduce that overhead. It also takes care to not trace code that you aren’t interested in.
When measuring branch coverage, the same trace function is used, but instead of recording line numbers, coverage.py
recordspairsoflinenumbers. Eachinvocationofthetracefunctionremembersthelinenumber,thenthenextinvocation
records the pair(prev, this)to indicate that execution transitioned from the previous line to this line. Internally, these
are called arcs.
As the data is being collected, coverage.py writes the data to a file, usually named.coverage. This is aSQLite
database containing all of the measured data.
74 Chapter 6. More information

Coverage.py, Release 7.2.2
Plugins
Of course coverage.py mostly measures execution of Python files. But it can also be used to analyze other kinds of
execution. File tracer pluginsprovide support for non-Python files. For example, Django HTML templates result
in Python code being executed somewhere, but as a developer, you want that execution mapped back to your .html
template file.
During execution, each new Python file encountered is provided to the plugins to consider. A plugin can claim the file
and then convert the runtime Python execution into source-level data to be recorded.
Dynamic contexts
Whenusing dynamiccontexts,thereisacurrentdynamiccontextthatchangesoverthecourseofexecution. Itstartsas
empty. While it is empty, every time a new function is entered, a check is made to see if the dynamic context should
change. While a non-empty dynamic context is current, the check is skipped until the function that started the context
returns.
6.10.2 Analysis
Afteryourprogramhasbeenexecutedandthelinenumbersrecorded,coverage.pyneedstodeterminewhatlinescould
havebeenexecuted. Luckily,compiledPythonfiles(.pycfiles)haveatableoflinenumbersinthem. Coverage.pyreads
this table to get the set of executable lines, with a little more source analysis to leave out things like docstrings.
The data file is read to get the set of lines that were executed. The difference between the executable lines and the
executed lines are the lines that were not executed.
The same principle applies for branch measurement, though the process for determining possible branches is more
involved. Coverage.py uses the abstract syntax tree of the Python source file to determine the set of possible branches.
6.10.3 Reporting
Once we have the set of executed lines and missing lines, reporting is just a matter of formatting that information in a
usefulway. Eachreportingmethod(text,HTML,JSON,annotatedsource,XML)hasadifferentoutputformat,butthe
process is the same: write out the information in the particular format, possibly including the source code itself.
6.11 Plug-ins
Coverage.py’s behavior can be extended with third-party plug-ins. A plug-in is a separately installed Python class that
youregisterinyour.coveragerc. Pluginscanalteranumberofaspectsofcoverage.py’sbehavior,includingimplement-
ing coverage measurement for non-Python files.
Information about using plug-ins is on this page. To write a plug-in, seePlug-in classes.
New in version 4.0.
6.11. Plug-ins 75

Coverage.py, Release 7.2.2
6.11.1 Using plug-ins
To use a coverage.py plug-in, you install it and configure it. For this example, let’s say there’s a Python package called
something that provides a coverage.py plug-in calledsomething.plugin.
1. Install the plug-in’s package as you would any other Python package:
$ python3 -m pip install something
2. Configure coverage.py to use the plug-in. You do this by editing (or creating) your .coveragerc file, as described
in Configuration reference. The plugins setting indicates your plug-in. It’s a list of importable module names
of plug-ins:
[run]
plugins =
something.plugin
3. If the plug-in needs its own configuration, you can add those settings in the .coveragerc file in a section named
for the plug-in:
[something.plugin]
option1 = True
option2 = abc.foo
Check the documentation for the plug-in for details on the options it takes.
4. Run your tests with coverage.py as you usually would. If you get a message like “Plugin file tracers (some-
thing.plugin) aren’t supported with PyTracer,” then you don’t have theC extensioninstalled. The C extension is
needed for certain plug-ins.
6.11.2 Available plug-ins
Some coverage.py plug-ins you might find useful:
• Django template coverage.py plug-in: for measuring coverage in Django templates.
• Conditionalcoverageplug-in: formeasuringcoveragebasedonanyrulesyoudefine! Canexcludedifferentlines
ofcodethatareonlyexecutedondifferentplatforms,pythonversions,andwithdifferentdependenciesinstalled.
• Mako template coverage plug-in: for measuring coverage in Mako templates. Doesn’t work yet, probably needs
some changes in Mako itself.
6.12 Contributing to coverage.py
Iwelcomecontributionstocoverage.py. Overtheyears,dozensofpeoplehaveprovidedpatchesofvarioussizestoadd
features or fix bugs. This page should have all the information you need to make a contribution.
One source of history or ideas are the bug reports against coverage.py. There you can find ideas for requested features,
or the remains of rejected ideas.
76 Chapter 6. More information

Coverage.py, Release 7.2.2
6.12.1 Before you begin
If you have an idea for coverage.py, run it by me before you begin writing code. This way, I can get you going in the
right direction, or point you to previous work in the area. Things are not always as straightforward as they seem, and
having the benefit of lessons learned by those before you can save you frustration.
6.12.2 Getting the code
The coverage.py code is hosted on a GitHub repository at https://github.com/nedbat/coveragepy. To get a working
environment, follow these steps:
1. Create a Python 3.7 virtualenv to work in, and activate it.
2. Clone the repository:
$ git clone https://github.com/nedbat/coveragepy
$ cd coveragepy
3. Install the requirements:
$ python3 -m pip install -r requirements/dev.pip
If this fails due to incorrect or missing hashes, usedev.in instead:
$ python3 -m pip install -r requirements/dev.in
4. InstallanumberofversionsofPython. Coverage.pysupportsarangeofPythonversions. Themoreyoucantest
with, the more easily your code can be used as-is. If you only have one version, that’s OK too, but may mean
more work integrating your contribution.
6.12.3 Running the tests
The tests are written mostly as standard unittest-style tests, and are run with pytest running under tox:
$ tox
py37 create: /Users/nedbat/coverage/trunk/.tox/py37
py37 installdeps: -rrequirements/pip.pip, -rrequirements/pytest.pip, eventlet==0.25.1,␣
˓→greenlet==0.4.15
py37 develop-inst: /Users/nedbat/coverage/trunk
py37 installed: apipkg==1.5,appdirs==1.4.4,attrs==20.3.0,backports.functools-lru-
˓→cache==1.6.4,-e git+git@github.com:nedbat/coveragepy.
˓→git@36ef0e03c0439159c2245d38de70734fa08cddb4#egg=coverage,decorator==5.0.7,distlib==0.
˓→3.1,dnspython==2.1.0,eventlet==0.25.1,execnet==1.8.0,filelock==3.0.12,flaky==3.7.0,
˓→future==0.18.2,greenlet==0.4.15,hypothesis==6.10.1,importlib-metadata==4.0.1,
˓→iniconfig==1.1.1,monotonic==1.6,packaging==20.9,pluggy==0.13.1,py==1.10.0,PyContracts␣
˓→@ git+https://github.com/slorg1/contracts@c5a6da27d4dc9985f68e574d20d86000880919c3,
˓→pyparsing==2.4.7,pytest==6.2.3,pytest-forked==1.3.0,pytest-xdist==2.2.1,qualname==0.1.
˓→0,six==1.15.0,sortedcontainers==2.3.0,toml==0.10.2,typing-extensions==3.10.0.0,
˓→virtualenv==20.4.4,zipp==3.4.1
py37 run-test-pre: PYTHONHASHSEED= '376882681'
py37 run-test: commands[0] | python setup.py --quiet clean develop
py37 run-test: commands[1] | python igor.py zip_mods remove_extension
py37 run-test: commands[2] | python igor.py test_with_tracer py

6.12. Contributing to coverage.py 77

Coverage.py, Release 7.2.2
(continued from previous page)
=== CPython 3.7.10 with Python tracer (.tox/py37/bin/python) ===
bringing up nodes...
.........................................................................................
˓→.................................................................. [ 15%]
.........................................................................................
˓→.................................................................. [ 31%]
.........................................................................................
˓→..................................................s............... [ 47%]
...........................................s.............................................
˓→......................................sss.sssssssssssssssssss..... [ 63%]
.........................................................................................
˓→...............................................................s.. [ 79%]
......................................s..................................s...............
˓→.................................................................. [ 95%]
........................................ss...... ␣
˓→ [100%]
949 passed, 29 skipped in 40.56s
py37 run-test: commands[3] | python setup.py --quiet build_ext --inplace
py37 run-test: commands[4] | python igor.py test_with_tracer c
=== CPython 3.7.10 with C tracer (.tox/py37/bin/python) ===
bringing up nodes...
.........................................................................................
˓→.................................................................. [ 15%]
.........................................................................................
˓→.................................................................. [ 31%]
......................................................................s..................
˓→.................................................................. [ 47%]
.........................................................................................
˓→.................................................................. [ 63%]
..........................s................................................s.............
˓→.................................................................. [ 79%]
.................................................................................s.......
˓→.................................................................. [ 95%]
......................................s......... ␣
˓→ [100%]
973 passed, 5 skipped in 41.36s
____________________________________________________________________________ summary ____
˓→_________________________________________________________________________
py37: commands succeeded
congratulations :)
Tox runs the complete test suite twice for each version of Python you have installed. The first run uses the Python
implementation of the trace function, the second uses the C implementation.
To limit tox to just a few versions of Python, use the-eswitch:
$ tox -e py37,py39
To run just a few tests, you can use pytest test selectors:
$ tox tests/test_misc.py
$ tox tests/test_misc.py::HasherTest
$ tox tests/test_misc.py::HasherTest::test_string_hashing
78 Chapter 6. More information

Coverage.py, Release 7.2.2
These command run the tests in one file, one class, and just one test, respectively.
You can also affect the test runs with environment variables. Define any of these as 1 to use them:
• COVERAGE_NO_PYTRACER=1disables the Python tracer if you only want to run the CTracer tests.
• COVERAGE_NO_CTRACER=1disables the C tracer if you only want to run the PyTracer tests.
• COVERAGE_ONE_TRACER=1 will use only one tracer for each Python version. This will use the C tracer if it is
available, or the Python tracer if not.
• COVERAGE_AST_DUMP=1will dump the AST tree as it is being used during code parsing.
There are other environment variables that affect tests. I use set_env.py as a simple terminal interface to see and set
them.
Of course, run all the tests on every version of Python you have, before submitting a change.
6.12.4 Lint, etc
I try to keep the coverage.py source as clean as possible. I use pylint to alert me to possible problems:
$ make lint
The source is pylint-clean, even if it’s because there are pragmas quieting some warnings. Please try to keep it that
way, but don’t let pylint warnings keep you from sending patches. I can clean them up.
Lines should be kept to a 100-character maximum length. I recommend an editorconfig.org plugin for your editor of
choice.
Other style questions are best answered by looking at the existing code. Formatting of docstrings, comments, long
lines, and so on, should match the code that already exists.
Many people love black, but I would prefer not to run it on coverage.py.
6.12.5 Continuous integration
When you make a pull request, GitHub actions will run all of the tests and quality checks on your changes. If any fail,
either fix them or ask for help.
6.12.6 Dependencies
Coverage.py has no direct runtime dependencies, and I would like to keep it that way.
It has many development dependencies. These are specified generically in therequirements/*.in files. The .in
filesshouldhavenoversionsspecifiedinthem. Thespecificversionstousearepinnedin requirements/*.pipfiles.
These are created by runningmake upgrade .
It’s important to use Python 3.7 to runmake upgrade so that the pinned versions will work on all of the Python
versions currently supported by coverage.py.
If for some reason we need to constrain a version of a dependency, the constraint should be specified in the
requirements/pins.pipfile, with a detailed reason for the pin.
6.12. Contributing to coverage.py 79

Coverage.py, Release 7.2.2
6.12.7 Coverage testing coverage.py
Coverage.py can measure itself, but it’s complicated. The process has been packaged up to make it easier:
$ make metacov metahtml
Thenlookathtmlcov/index.html. Notethatduetotherecursivenatureofcoverage.pymeasuringitself,therearesome
parts of the code that will never appear as covered, even though they are executed.
6.12.8 Contributing
When you are ready to contribute a change, any way you can get it to me is probably fine. A pull request on GitHub is
great, but a simple diff or patch works too.
All contributions are expected to include tests for new functionality and fixes. If you need help writing tests, please
ask.
6.13 Things that cause trouble
Coverage.py works well, and I want it to properly measure any Python program, but there are some situations it can’t
cope with. This page details some known problems, with possible courses of action, and links to coverage.py bug
reports with more information.
Iwouldloveto hearfromyou ifyouhaveinformationaboutanyoftheseproblems, evenjusttoexplaintomewhyyou
want them to start working properly.
If your problem isn’t discussed here, you can of course search the coverage.py bug tracker directly to see if there is
some mention of it.
6.13.1 Things that don’t work
There are a few modules or functions that prevent coverage.py from working properly:
• execv, or oneof itsvariants. These endthe currentprogram andreplace itwith a newone. Thisdoesn’t save the
collected coverage data, so your program that calls execv will not be fully measured. A patch for coverage.py is
in issue 43.
• thread,inthePythonstandardlibrary,isthelow-levelthreadinginterface. Threadscreatedwiththismodulewill
not be traced. Use the higher-level threading module instead.
• sys.settrace is the Python feature that coverage.py uses to see what’s happening in your program. If another part
of your program is using sys.settrace, then it will conflict with coverage.py, and it won’t be measured properly.
• sys.setprofilecallsyourcode,butwhilerunningyourcode,doesnotfiretraceevents. Thismeansthatcoverage.py
can’t see what’s happening in that code.
80 Chapter 6. More information

Coverage.py, Release 7.2.2
6.13.2 Still having trouble?
Ifyourproblemisn’tmentionedhere,andisn’talreadyreportedinthecoverage.pybugtracker,please getintouchwith
me, we’ll figure out a solution.
6.14 FAQ and other help
6.14.1 Frequently asked questions
Q: Why are some of my files not measured?
Coverage.py has a number of mechanisms for deciding which files to measure and which to skip. If your files aren’t
being measured, use the--debug=trace option, also settable as[run] debug=trace in the settings file, or as
COVERAGE_DEBUG=trace in an environment variable.
This will write a line for each file considered, indicating whether it is traced or not, and if not, why not. Be careful
though: the output might be swallowed by your test runner. If so, aCOVERAGE_DEBUG_FILE=/tmp/cov.out envi-
ronemnt variable can direct the output to a file insttead to ensure you see everything.
Q: Why do unexecutable lines show up as executed?
Usually this is because you’ve updated your code and run coverage.py on it again without erasing the old data. Cover-
age.pyrecordslinenumbersexecuted,sotheolddatamayhaverecordedalinenumberwhichhassincemoved,causing
coverage.py to claim a line has been executed which cannot be.
If old data is persisting, you can use an explicitcoverage erase command to clean out the old data.
Q: Why are my function definitions marked as run when I haven’t tested them?
The def and class lines in your Python file are executed when the file is imported. Those are the lines that define
your functions and classes. They run even if you never call the functions. It’s the body of the functions that will be
marked as not executed if you don’t test them, not thedef lines.
Thiscanmeanthatyourcodehasamoderatecoveragetotalevenifnotestshavebeenwrittenorrun. Thismightseem
surprising, but it is accurate: thedef lines have actually been run.
Q: Why do the bodies of functions show as executed, but the def lines do not?
If this happens, it’s because coverage.py has started after the functions are defined. The definition lines are executed
without coverage measurement, then coverage.py is started, then the function is called. This means the body is mea-
sured, but the definition of the function itself is not.
The same thing can happen with the bodies of classes.
Tofixthis,startcoverage.pyearlier. Ifyouusethe commandline torunyourprogramwithcoverage.py,thenyourentire
program will be monitored. If you are using theAPI, you need to call coverage.start() before importing the modules
that define your functions.
6.14. FAQ and other help 81

Coverage.py, Release 7.2.2
Q: My decorator lines are marked as covered, but the “def” line is not. Why?
Different versions of Python report execution on different lines. Coverage.py adapts its behavior to the version of
Python being used. In Python 3.7 and earlier, a decorated function definition only reported the decorator as executed.
In Python 3.8 and later, both the decorator and the “def” are reported. If you collect execution data on Python 3.7, and
then run coverage reports on Python 3.8, there will be a discrepancy.
Q: Can I find out which tests ran which lines?
Yes! Coverage.pyhasafeaturecalled Dynamiccontexts whichcancollectthisinformation. Addthistoyour.coveragerc
file:
[run]
dynamic_context = test_function
and then use the--contextsoption when generating an HTML report.
Q: How is the total percentage calculated?
Coverage.py counts the total number of possible executions. This is the number of executable statements minus the
number of excluded statements. It then counts the number of those possibilities that were actually executed. The total
percentage is the actual executions divided by the possible executions.
As an example, a coverage report with 1514 statements and 901 missed statements would calculate a total percentage
of (1514-901)/1514, or 40.49%.
Branch coverageextends the calculation to include the total number of possible branch exits, and the number of those
taken. Inthiscasethespecificnumbersshownincoveragereportsdon’tcalculateouttothepercentageshown,because
the number of missing branch exits isn’t reported explicitly. A branch line that wasn’t executed at all is counted once
asamissingstatementinthereport, insteadofastwomissingbranches. Reportsshowthenumberofpartialbranches,
which is the lines that were executed but did not execute all of their exits.
Q: Coverage.py is much slower than I remember, what’s going on?
Make sure you are using the C trace function. Coverage.py provides two implementations of the trace function. The
C implementation runs much faster. To see what you are running, usecoverage debug sys . The output contains
details of the environment, including a line that says eitherCTrace: available or CTracer: unavailable . If
it says unavailable, then you are using the slow Python implementation.
Try re-installing coverage.py to see what happened and if you get the CTracer as you should.
Q: Isn’t coverage testing the best thing ever?
It’s good, but it isn’t perfect.
82 Chapter 6. More information

Coverage.py, Release 7.2.2
Q: Where can I get more help with coverage.py?
You can discuss coverage.py or get help using it on the Python discussion forums. If you ping me (@nedbat), there’s
a higher chance I’ll see the post.
Bug reports are gladly accepted at the GitHub issue tracker.
I can be reached in a number of ways, I’m happy to answer questions about using coverage.py.
6.14.2 History
Coverage.py was originally written by Gareth Rees. Since 2004, Ned Batchelder has extended and maintained it with
the help of many others. Thechange historyhas all the details.
6.15 Change history for coverage.py
These changes are listed in decreasing version number order. Note this can be different from a strict chronological
order when there are two branches in development at the same time, such as 4.5.x and 5.0.
6.15.1 Version 7.2.2 — 2023-03-16
• Fix: if a virtualenv was created inside a source directory, and a sourced package was installed inside the vir-
tualenv,thenallofthethird-partypackagesinsidethevirtualenvwouldbemeasured. Thiswasincorrect,buthas
now been fixed: only the specified packages will be measured, thanks to Manuel Jacob.
• Fix: the coverage lcov command could create a .lcov file with incorrect LF (lines found) and LH (lines hit)
totals. This is now fixed, thanks to Ian Moore.
• Fix: the coverage xml command on Windows could create a .xml file with duplicate<package> elements.
This is now fixed, thanks to Benjamin Parzella, closing issue 1573.
6.15.2 Version 7.2.1 — 2023-02-26
• Fix: the PyPI page had broken links to documentation pages, but no longer does, closing issue 1566.
• Fix: publicmembersofthecoveragemodulearenowproperlyindicatedsothatmypywillfindthem,fixingissue
1564.
6.15.3 Version 7.2.0 — 2023-02-22
• Addedanewsetting [report] exclude_also toletyouaddmoreexclusionswithoutoverwritingthedefaults.
Thanks, Alpha Chen, closing issue 1391.
• Addeda CoverageData.purge_files()methodtoremoverecordeddataforaparticularfile. Contributedby
Stephan Deibel.
• Fix: whenreportingcommandsfail,theywillnolongercongratulatethemselveswithmessageslike“WroteXML
report to file.xml” before spewing a traceback about their failure.
6.15. Change history for coverage.py 83

Coverage.py, Release 7.2.2
• Fix: arguments in the public API that name file paths now accept pathlib.Path objects. This includes the
data_file and config_file arguments to the Coverage constructor and thebasename argument to Cov-
erageData. Closes issue 1552.
• Fix: In some embedded environments, an IndexError could occur on stop() when the originating thread exits
before completion. This is now fixed, thanks to Russell Keith-Magee, closing issue 1542.
• Added apy.typed file to announce our type-hintedness. Thanks, KotlinIsland.
6.15.4 Version 7.1.0 — 2023-01-24
• Added: the debug output file can now be specified with[run] debug_file in the configuration file. Closes
issue 1319.
• Performance: fixedaslowdownwithdynamiccontextsthat’sbeenaroundsince6.4.3. Thefixclosesissue1538.
Thankfully this doesn’t break the Cython change that fixed issue 972. Thanks to Mathieu Kniewallner for the
deep investigative work and comprehensive issue report.
• Typing: all product and test code has type annotations.
6.15.5 Version 7.0.5 — 2023-01-10
• Fix: On Python 3.7, a file with type annotations but nofrom __future__ import annotations would be
missing statements in the coverage report. This is now fixed, closing issue 1524.
6.15.6 Version 7.0.4 — 2023-01-07
• Performance: aninternalcacheoffilenameswasaccidentallydisabled,resultinginsometimesdrasticreductions
inperformance. Thisisnowfixed,closingissue1527. ThankstoIvanCiuvalschiiforthereproducibletestcase.
6.15.7 Version 7.0.3 — 2023-01-03
• Fix: when using pytest-cov or pytest-xdist, or perhaps both, the combining step could fail withassert row
is not None using 7.0.2. This was due to a race condition that has always been possible and is still possible.
In 7.0.1 and before, the error was silently swallowed by the combining code. Now it will produce a message
“Couldn’t combine data file” and ignore the data file as it used to do before 7.0.2. Closes issue 1522.
6.15.8 Version 7.0.2 — 2023-01-02
• Fix: whenusingthe [run] relative_files = True setting,arelative [paths]patternwasstillbeingmade
absolute. This is now fixed, closing issue 1519.
• Fix: ifPythondoesn’tprovidetomllib,thenTOMLconfigurationfilescanonlybereadifcoverage.pyisinstalled
with the [toml] extra. Coverage.py will raise an error if TOML support is not installed when it sees your
settings are in a .toml file. But it didn’t understand that[tools.coverage] was a valid section header, so the
error wasn’t reported if you used that header, and settings were silently ignored. This is now fixed, closing issue
1516.
• Fix: adjusted how decorators are traced on PyPy 7.3.10, fixing issue 1515.
• Fix: the coverage lcov report did not properly implement the--fail-under=MIN option. This has been
fixed.
84 Chapter 6. More information

Coverage.py, Release 7.2.2
• Refactor: added many type annotations, including a number of refactorings. This should not affect outward
behavior, but they were a bit invasive in some places, so keep your eyes peeled for oddities.
• Refactor: removed the vestigial and long untested support for Jython and IronPython.
6.15.9 Version 7.0.1 — 2022-12-23
• When checking if a file mapping resolved to a file that exists, we weren’t considering files in .whl files. This is
now fixed, closing issue 1511.
• File pattern rules were too strict, forbidding plus signs and curly braces in directory and file names. This is now
fixed, closing issue 1513.
• Unusual Unicode or control characters in source files could prevent reporting. This is now fixed, closing issue
1512.
• The PyPy wheel now installs on PyPy 3.7, 3.8, and 3.9, closing issue 1510.
6.15.10 Version 7.0.0 — 2022-12-18
Nothing new beyond 7.0.0b1.
6.15.11 Version 7.0.0b1 — 2022-12-03
A number of changes have been made to file path handling, including pattern matching and path remapping with the
[paths]setting (see[paths]). These changes might affect you, and require you to update your settings.
(This release includes the changes from6.6.0b1, since 6.6.0 was never released.)
• Changes to file pattern matching, which might require updating your configuration:
–Previously, *wouldincorrectlymatchdirectoryseparators, makingprecisematchingdifficult. Thisisnow
fixed, closing issue 1407.
–Now **matches any number of nested directories, including none.
• Improvements to combining data files when using the[run] relative_filessetting, which might require updating
your configuration:
–During coverage combine , relative file paths are implicitly combined without needing a[paths] con-
figuration setting. This also fixed issue 991.
–A [paths] setting like */foo will now matchfoo/bar.py so that relative file paths can be combined
more easily.
–The[run] relative_filessetting is properly interpreted in more places, fixing issue 1280.
• When remapping file paths with[paths], a path will be remapped only if the resulting path exists. The docu-
mentation has long said the prefix had to exist, but it was never enforced. This fixes issue 608, improves issue
649, and closes issue 757.
• Reporting operations now implicitly use the[paths]setting to remap file paths within a single data file. Com-
bining multiple files still requires thecoverage combine step, but this simplifies some single-file situations.
Closes issue 1212 and issue 713.
• The coverage report command now has a--format= option. The original style is now--format=text,
and is the default.
6.15. Change history for coverage.py 85

Coverage.py, Release 7.2.2
–Using --format=markdown will write the table in Markdown format, thanks to Steve Oswald, closing
issue 1418.
–Using --format=total will write a single total number to the output. This can be useful for making
badges or writing status updates.
• Combiningdatafileswith coverage combine nowhashesthedatafilestoskipfilesthataddnonewinformation.
Thiscanreducethetimeneeded. Manydetailsaffectthespeed-up,butforcoverage.py’sowntestsuite,combining
is about 40% faster. Closes issue 1483.
• When searching for completely un-executed files, coverage.py uses the presence of__init__.py files to de-
termine which directories have source that could have been imported. However, implicit namespace packages
don’t require__init__.py. A new setting[report] include_namespace_packages tells coverage.py to
consider these directories during reporting. Thanks to Felix Horvat for the contribution. Closes issue 1383 and
issue 1024.
• Fixed environment variable expansion in pyproject.toml files. It was overly broad, causing errors outside of
coverage.py settings, as described in issue 1481 and issue 1345. This is now fixed, but in rare cases will require
changing your pyproject.toml to quote non-string values that use environment substitution.
• An empty file has a coverage total of 100%, but used to fail with--fail-under. This has been fixed, closing
issue 1470.
• Thetextreporttablenolongerwritesouttwoseparatorlinesiftherearenofileslistedinthetable. Oneisplenty.
• Fixedamis-measurementofastrangeuseofwildcardalternativesinmatch/casestatements,closingissue1421.
• Fixed internal logic that prevented coverage.py from running on implementations other than CPython or PyPy
(issue 1474).
• The deprecated[run] note setting has been completely removed.
6.15.12 Version 6.6.0b1 — 2022-10-31
(Note: 6.6.0 final was never released. These changes are part of7.0.0b1.)
• Changes to file pattern matching, which might require updating your configuration:
–Previously, *wouldincorrectlymatchdirectoryseparators, makingprecisematchingdifficult. Thisisnow
fixed, closing issue 1407.
–Now **matches any number of nested directories, including none.
• Improvements to combining data files when using the[run] relative_filessetting:
–During coverage combine , relative file paths are implicitly combined without needing a[paths] con-
figuration setting. This also fixed issue 991.
–A [paths] setting like */foo will now matchfoo/bar.py so that relative file paths can be combined
more easily.
–The setting is properly interpreted in more places, fixing issue 1280.
• Fixed environment variable expansion in pyproject.toml files. It was overly broad, causing errors outside of
coverage.py settings, as described in issue 1481 and issue 1345. This is now fixed, but in rare cases will require
changing your pyproject.toml to quote non-string values that use environment substitution.
• Fixed internal logic that prevented coverage.py from running on implementations other than CPython or PyPy
(issue 1474).
86 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.13 Version 6.5.0 — 2022-09-29
• TheJSONreportnowincludesdetailsofwhichbranchesweretaken,andwhicharemissingforeachfile. Thanks,
Christoph Blessing. Closes issue 1425.
• Starting with coverage.py 6.2,class statements were marked as a branch. This wasn’t right, and has been
reverted, fixing issue 1449. Note this will very slightly reduce your coverage total if you are measuring branch
coverage.
• Packaging is now compliant with PEP 517, closing issue 1395.
• A new debug option--debug=pathmap shows details of the remapping of paths that happens during combine
due to the[paths]setting.
• Fix an internal problem with caching of invalid Python parsing. Found by OSS-Fuzz, fixing their bug 50381.
6.15.14 Version 6.4.4 — 2022-08-16
• Wheels are now provided for Python 3.11.
6.15.15 Version 6.4.3 — 2022-08-06
• Fix a failure when combining data files if the file names contained glob-like patterns. Thanks, Michael Krebs
and Benjamin Schubert.
• FixamessagingfailurewhencombiningWindowsdatafilesonadifferentdrivethanthecurrentdirectory,closing
issue 1428. Thanks, Lorenzo Micò.
• Fix path calculations when running in the root directory, as you might do in a Docker container. Thanks Arthur
Rio.
• Filtering in the HTML report wouldn’t work when reloading the index page. This is now fixed. Thanks, Marc
Legendre.
• Fix a problem with Cython code measurement, closing issue 972. Thanks, Matus Valo.
6.15.16 Version 6.4.2 — 2022-07-12
• Updated for a small change in Python 3.11.0 beta 4: modules now start with a line with line number 0, which is
ignored. Thislinecannotbeexecuted,socoveragetotalswerethrownoff. Thislineisnowignoredbycoverage.py,
butthisalsomeansthattrulyemptymodules(like __init__.py)havenolinesinthem,ratherthanonephantom
line. Fixes issue 1419.
• Internal debugging data added to sys.modules is now an actual module, to avoid confusing code that examines
everything in sys.modules. Thanks, Yilei Yang.
6.15. Change history for coverage.py 87

Coverage.py, Release 7.2.2
6.15.17 Version 6.4.1 — 2022-06-02
• Greatly improved performance on PyPy, and other environments that need the pure Python trace function.
Thanks, Carl Friedrich Bolz-Tereick (pull 1381 and pull 1388). Slightly improved performance when using
the C trace function, as most environments do. Closes issue 1339.
• Theconditionsforusingtomllibfromthestandardlibraryhavebeenmademoreprecise,sothat3.11alphaswill
continue to work. Closes issue 1390.
6.15.18 Version 6.4 — 2022-05-22
• A new setting,[run] sigterm, controls whether a SIGTERM signal handler is used. In 6.3, the signal handler
wasalwaysinstalled,tocapturedataatunusualprocessends. Unfortunately,thisintroducedotherproblems(see
issue 1310). Now the signal handler is only used if you opt-in by setting[run] sigterm = true .
• Small changes to the HTML report:
–Added links to next and previous file, and more keyboard shortcuts:[and ]for next file and previous file;
ufor up to the index; and?to open/close the help panel. Thanks, J. M. F. Tsang.
–The time stamp and version are displayed at the top of the report. Thanks, Ammar Askar. Closes issue
1351.
• A new debug optiondebug=sqldata adds more detail todebug=sql, logging all the data being written to the
database.
• Previously, runningcoverage report (or any of the reporting commands) in an empty directory would create
a .coverage data file. Now they do not, fixing issue 1328.
• OnPython3.11,the [toml]extranolongerinstallstomli,insteadusingtomllibfromthestandardlibrary. Thanks
Shantanu.
• In-memory CoverageData objects now properly update(), closing issue 1323.
6.15.19 Version 6.3.3 — 2022-05-12
• Fix: Coverage.py now builds successfully on CPython 3.11 (3.11.0b1) again. Closes issue 1367. Some results
for generators may have changed.
6.15.20 Version 6.3.2 — 2022-02-20
• Fix: adapt to pypy3.9’s decorator tracing behavior. It now traces function decorators like CPython 3.8: both the
@-line and the def-line are traced. Fixes issue 1326.
• Debug: added pybehave to the list ofcoverage debugand --debugoptions.
• Fix: show an intelligible error message if--concurrency=multiprocessingis used without a configuration
file. Closes issue 1320.
88 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.21 Version 6.3.1 — 2022-02-01
• Fix: deadlocks could occur when terminating processes. Some of these deadlocks (described in issue 1310) are
now fixed.
• Fix: a signal handler was being set from multiple threads, causing an error: “ValueError: signal only works in
main thread”. This is now fixed, closing issue 1312.
• Fix: --precision on the command-line was being ignored while considering--fail-under. This is now
fixed, thanks to Marcelo Trylesinski.
• Fix: releasesnolongerprovide3.11.0-alphawheels. Coverage.pyusesCPythoninternalfieldswhicharemoving
during the alpha phase. Fixes issue 1316.
6.15.22 Version 6.3 — 2022-01-25
• Feature: Added thelcov command to generate reports in LCOV format. Thanks, Bradley Burns. Closes issues
587 and 626.
• Feature: the coverage data file can now be specified on the command line with the--data-file option in any
command that reads or writes data. This is in addition to the existingCOVERAGE_FILE environment variable.
Closes issue 624. Thanks, Nikita Bloshchanevich.
• Feature: coverage measurement data will now be written when a SIGTERM signal is received by the process.
This includesProcess.terminate, and other ways to terminate a process. Currently this is only on Linux and
Mac; Windows is not supported. Fixes issue 1307.
• Dropped support for Python 3.6, which reached end-of-life on 2021-12-23.
• Updated Python 3.11 support to 3.11.0a4, fixing issue 1294.
• Fix: the coverage data file is now created in a more robust way, to avoid problems when multiple processes are
trying to write data at once. Fixes issues 1303 and 883.
• Fix: a .gitignore file will only be written into the HTML report output directory if the directory is empty. This
should prevent certain unfortunate accidents of writing the file where it is not wanted.
• Releases now have MacOS arm64 wheels for Apple Silicon, fixing issue 1288.
6.15.23 Version 6.2 — 2021-11-26
• Feature: Now the--concurrencysetting can now have a list of values, so that threads and another lightweight
threadingpackagecanbemeasuredtogether,suchas --concurrency=gevent,thread. Closesissue1012and
issue 1082.
• Fix: A module specified as thesource setting is imported during startup, before the user program imports it.
Thiscouldcauseproblemsiftherestoftheprogramisn’treadyyet. Forexample,issue1203describesaDjango
setting that is accessed before settings have been configured. Now the early import is wrapped in a try/except so
errors then don’t stop execution.
• Fix: Acoloninadecoratorexpressionwouldcauseanexclusiontoendtooearly,preventingtheexclusionofthe
decorated function. This is now fixed.
• Fix: The HTML report now will not overwrite a .gitignore file that already exists in the HTML output directory
(follow-on for issue 1244).
• API:TheexceptionsraisedbyCoverage.pyhavebeenspecialized,toprovidefiner-grainedcatchingofexceptions
by third-party code.
6.15. Change history for coverage.py 89

Coverage.py, Release 7.2.2
• API: Using suffix=False when constructing a Coverage object with multiprocessing wouldn’t suppress the
data file suffix (issue 989). This is now fixed.
• Debug: The coverage debug data command will now sniff out combinable data files, and report on all of
them.
• Debug: The coverage debug command used to accept a number of topics at a time, and show all of them,
though this was never documented. This no longer works, to allow for command-line options in the future.
6.15.24 Version 6.1.2 — 2021-11-10
• Python3.11issupported(testedwith3.11.0a2). Onestill-openissuehastodowithexitsthroughwith-statements.
• Fix: When remapping file paths through the[paths] setting while combining, the[run] relative_files
setting was ignored, resulting in absolute paths for remapped file names (issue 1147). This is now fixed.
• Fix: Complex conditionals over excluded lines could have incorrectly reported a missing branch (issue 1271).
This is now fixed.
• Fix: More exceptions are now handled when trying to parse source files for reporting. Problems that used to
terminate coverage.py can now be handled with[report] ignore_errors . This helps with plugins failing to
read files (django_coverage_plugin issue 78).
• Fix: Removed another vestige of jQuery from the source tarball (issue 840).
• Fix: Added a default value for a new-to-6.x argument of an internal class. This unsupported class is being used
by coveralls (issue 1273). Although I’d rather not “fix” unsupported interfaces, it’s actually nicer with a default
value.
6.15.25 Version 6.1.1 — 2021-10-31
• Fix: The sticky header on the HTML report didn’t work unless you had branch coverage enabled. This is now
fixed: the sticky header works for everyone. (Do people still use coverage without branch measurement!? j/k)
• Fix: When using explicitly declared namespace packages, the “already imported a file that will be measured”
warning would be issued (issue 888). This is now fixed.
6.15.26 Version 6.1 — 2021-10-30
• Deprecated: The annotate command and theCoverage.annotate function will be removed in a future ver-
sion, unless people let me know that they are using it. Instead, thehtml command gives better-looking (and
more accurate) output, and thereport -m command will tell you line numbers of missing lines. Please get in
touch if you have a reason to useannotateover those better options: ned@nedbatchelder.com.
• Feature: Coverage now sets an environment variable, COVERAGE_RUN when running your code with the
coverage run command. The value is not important, and may change in the future. Closes issue 553.
• Feature: The HTML report pages for Python source files now have a sticky header so the file name and controls
are always visible.
• Feature: Thexml and jsoncommands now describe what they wrote where.
• Feature: The html, combine, xml, andjson commands all accept a-q/--quiet option to suppress the mes-
sages they write to stdout about what they are doing (issue 1254).
• Feature: The html command writes a.gitignore file into the HTML output directory, to prevent the report
from being committed to git. If you want to commit it, you will need to delete that file. Closes issue 1244.
90 Chapter 6. More information

Coverage.py, Release 7.2.2
• Feature: Added support for PyPy 3.8.
• Fix: Moregeneratedcodeisnowexcludedfrommeasurement. Codesuchasattrsboilerplate,ordoctestcode,was
being measured though the synthetic line numbers meant they were never reported. Once Cython was involved
though, the generated .so files were parsed as Python, raising syntax errors, as reported in issue 1160. This is
now fixed.
• Fix: Whensortinghuman-readablenames, numericcomponentsaresortedcorrectly: file10.pywillappearafter
file9.py. This applies to file names, module names, environment variables, and test contexts.
• Performance: Branch coverage measurement is faster, though you might only notice on code that is executed
many times, such as long-running loops.
• Build: jQuery is no longer used or vendored (issue 840 and issue 1118). Huge thanks to Nils Kattenbeck (sep-
tatrix) for the conversion to vanilla JavaScript in pull request 1248.
6.15.27 Version 6.0.2 — 2021-10-11
• Namespacepackagesbeingmeasuredweren’tproperlyhandledbythenewcodethatignoresthird-partypackages.
If the namespace package was installed, it was ignored as a third-party package. That problem (issue 1231) is
now fixed.
• Packagesnamedas“sourcepackages”(with source,or source_pkgs,orpytest-cov’s--cov)mighthavebeen
onlypartiallymeasured. Theirtop-levelstatementscouldbemarkedasun-executed,becausetheywereimported
by coverage.py before measurement began (issue 1232). This is now fixed, but the package will be imported
twice, once by coverage.py, then again by your test suite. This could cause problems if importing the package
has side effects.
• The CoverageData.contexts_by_lineno() method was documented to return a dict, but was returning a
defaultdict. Now it returns a plain dict. It also no longer returns negative numbered keys.
6.15.28 Version 6.0.1 — 2021-10-06
• In 6.0, the coverage.py exceptions moved from coverage.misc to coverage.exceptions. These exceptions are not
part of the public supported API, CoverageException is. But a number of other third-party packages were im-
porting the exceptions from coverage.misc, so they are now available from there again (issue 1226).
• Changed an internal detail of how tomli is imported, so that tomli can use coverage.py for their own test suite
(issue 1228).
• Defend against an obscure possibility under code obfuscation, where a function can have an argument called
“self”, but no local named “self” (pull request 1210). Thanks, Ben Carlsson.
6.15.29 Version 6.0 — 2021-10-03
• The coverage html command now prints a message indicating where the HTML report was written. Fixes
issue 1195.
• The coverage combine command now prints messages indicating each data file being combined. Fixes issue
1105.
• The HTML report now includes a sentence about skipped files due toskip_covered or skip_empty settings.
Fixes issue 1163.
• Unrecognized options in the configuration file are no longer errors. They are now warnings, to ease the use of
coverage across versions. Fixes issue 1035.
6.15. Change history for coverage.py 91

Coverage.py, Release 7.2.2
• FixhandlingofexceptionsthroughcontextmanagersinPython3.10. Amissingexceptionisnolongerconsidered
a missing branch from the with statement. Fixes issue 1205.
• Fix another rarer instance of “Error binding parameter 0 - probably unsupported type.” (issue 1010).
• Creating a directory for the coverage data file now is safer against conflicts when two coverage runs happen
simultaneously (pull 1220). Thanks, Clément Pit-Claudel.
6.15.30 Version 6.0b1 — 2021-07-18
• Dropped support for Python 2.7, PyPy 2, and Python 3.5.
• Added support for the Python 3.10match/casesyntax.
• Data collection is now thread-safe. There may have been rare instances of exceptions raised in multi-threaded
programs.
• Plugins(liketheDjangocoverageplugin)weregenerating“Alreadyimportedafilethatwillbemeasured”warn-
ings about Django itself. These have been fixed, closing issue 1150.
• Warnings generated by coverage.py are now real Python warnings.
• Using --fail-under=100 with coverage near 100% could result in the self-contradictory messagetotal of
100 is less than fail-under=100 . This bug (issue 1168) is now fixed.
• The COVERAGE_DEBUG_FILE environment variable now acceptsstdout and stderr to write to those destina-
tions.
• TOML parsing now uses the tomli library.
• Some minor changes to usually invisible details of the HTML report:
–Use a modern hash algorithm when fingerprinting, for high-security environments (issue 1189). When
generating the HTML report, we save the hash of the data, to avoid regenerating an unchanged HTML
page. We used to use MD5 to generate the hash, and now use SHA-3-256. This was never a security
concern, but security scanners would notice the MD5 algorithm and raise a false alarm.
–Change how report file names are generated, to avoid leading underscores (issue 1167), to avoid rare file
name collisions (issue 584), and to avoid file names becoming too long (issue 580).
6.15.31 Version 5.6b1 — 2021-04-13
Note: 5.6 final was never released. These changes are part of 6.0.
• Third-party packages are now ignored in coverage reporting. This solves a few problems:
–Coverage will no longer report about other people’s code (issue 876). This is true even when using
--source=.with a venv in the current directory.
–Coveragewillnolongergenerate“Alreadyimportedafilethatwillbemeasured”warningsaboutcoverage
itself (issue 905).
• The HTML report uses j/k to move up and down among the highlighted chunks of code. They used to highlight
the current chunk, but 5.0 broke that behavior. Now the highlighting is working again.
• The JSON report now includespercent_covered_display, a string with the total percentage, rounded to the
same number of decimal places as the other reports’ totals.
92 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.32 Version 5.5 — 2021-02-28
• coverage combine hasanewoption, --keeptokeeptheoriginaldatafilesaftercombiningthem. Thedefault
is still to delete the files after they have been combined. This was requested in issue 1108 and implemented in
pull request 1110. Thanks, Éric Larivière.
• When reporting missing branches incoverage report , branches aren’t reported that jump to missing lines.
This adds to the long-standing behavior of not reporting branches from missing lines. Now branches are only
reported if both the source and destination lines are executed. Closes both issue 1065 and issue 955.
• Minor improvements to the HTML report:
–Thestateofthelinevisibilityselectorbuttonsissavedinlocalstoragesoyoudon’thavetofiddlewiththem
so often, fixing issue 1123.
–It has a little more room for line numbers so that 4-digit numbers work well, fixing issue 1124.
• Improvedtheerrormessagewhencombininglineandbranchdata,sothatuserswillbemorelikelytounderstand
what’s happening, closing issue 803.
6.15.33 Version 5.4 — 2021-01-24
• Thetextreportproducedby coverage report nowalwaysoutputsaTOTALline,evenifonlyonePythonfile
is reported. This makes regex parsing of the output easier. Thanks, Judson Neer. This had been requested a
number of times (issue 1086, issue 922, issue 732).
• The skip_covered and skip_empty settings in the configuration file can now be specified in the[html]
section, so that text reports and HTML reports can use separate settings. The HTML report will still use the
[report]settings if there isn’t a value in the[html] section. Closes issue 1090.
• Combining files on Windows across drives now works properly, fixing issue 577. Thanks, Valentin Lab.
• Fix an obscure warning from deep in the _decimal module, as reported in issue 1084.
• Update to support Python 3.10 alphas in progress, including PEP 626: Precise line numbers for debugging and
other tools.
6.15.34 Version 5.3.1 — 2020-12-19
• Whenusing --sourceonalargesourcetree,v5.xwasslowerthanpreviousversions. Thisperformanceregres-
sion is now fixed, closing issue 1037.
• Mysterious SQLite errors can happen on PyPy, as reported in issue 1010. An immediate retry seems to fix the
problem, although it is an unsatisfying solution.
• TheHTMLreportnowsavesthesortorderinamorewidelysupportedway,fixingissue986. Thanks,Sebastián
Ramírez (pull request 1066).
• The HTML report pages now have aSleepy Snakefavicon.
• Wheels are now provided for manylinux2010, and for PyPy3 (pp36 and pp37).
• Continuous integration has moved from Travis and AppVeyor to GitHub Actions.
6.15. Change history for coverage.py 93

Coverage.py, Release 7.2.2
6.15.35 Version 5.3 — 2020-09-13
• The sourcesettinghasalwaysbeeninterpretedaseitherafilepathoramodule,dependingonwhichexisted. If
both interpretations were valid, it was assumed to be a file path. The newsource_pkgs setting can be used to
name a package to disambiguate this case. Thanks, Thomas Grainger. Fixes issue 268.
• If a plugin was disabled due to an exception, we used to still try to record its information, causing an exception,
as reported in issue 1011. This is now fixed.
6.15.36 Version 5.2.1 — 2020-07-23
• ThedarkmodeHTMLreportstillusedlightcolorsforthecontextlisting,makingthemunreadable(issue1009).
This is now fixed.
• The time stamp on the HTML report now includes the time zone. Thanks, Xie Yanbo (pull request 960).
6.15.37 Version 5.2 — 2020-07-05
• The HTML report has been redesigned by Vince Salvino. There is now a dark mode, the code text is larger, and
system sans serif fonts are used, in addition to other small changes (issue 858 and pull request 931).
• The coverage report and coverage html commandsnowaccepta --precisionoptiontocontrolthenum-
ber of decimal points displayed. Thanks, Teake Nutma (pull request 982).
• The coverage report and coverage html commands now accept a--no-skip-covered option to negate
--skip-covered. Thanks, Anthony Sottile (issue 779 and pull request 932).
• The --skip-emptyoption is now available for the XML report, closing issue 976.
• The coverage report commandnowacceptsa --sortoptiontospecifyhowtosorttheresults. Thanks,Jerin
Peter George (pull request 1005).
• If coverage fails due to the coverage total not reaching the--fail-under value, it will now print a message
making the condition clear. Thanks, Naveen Yadav (pull request 977).
• TOML configuration files with non-ASCII characters would cause errors on Windows (issue 990). This is now
fixed.
• The output of--debug=trace now includes information about how the--source option is being interpreted,
and the module names being considered.
6.15.38 Version 5.1 — 2020-04-12
• The JSON report now includes counts of covered and missing branches. Thanks, Salvatore Zagaria.
• On Python 3.8, try-finally-return reported wrong branch coverage with decorated async functions (issue 964).
This is now fixed. Thanks, Kjell Braden.
• The get_option() and set_option() methods can now manipulate the [paths] configuration setting.
Thanks to Bernát Gábor for the fix for issue 967.
94 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.39 Version 5.0.4 — 2020-03-16
• If using the[run] relative_files setting, the XML report will use relative files in the<source> elements
indicating the location of source code. Closes issue 948.
• The textual summary report could report missing lines with negative line numbers on PyPy3 7.1 (issue 943).
This is now fixed.
• Windows wheels for Python 3.8 were incorrectly built, but are now fixed. (issue 949)
• Updated Python 3.9 support to 3.9a4.
• HTML reports couldn’t be sorted if localStorage wasn’t available. This is now fixed: sorting works even though
the sorting setting isn’t retained. (issue 944 and pull request 945). Thanks, Abdeali Kothari.
6.15.40 Version 5.0.3 — 2020-01-12
• A performance improvement in 5.0.2 didn’t work for test suites that changed directory before combining data,
causing “Couldn’t use data file: no such table: meta” errors (issue 916). This is now fixed.
• Coverage could fail to run your program with some form of “ModuleNotFound” or “ImportError” trying to
importfromthecurrentdirectory. Thiswouldhappenifcoveragehadbeenpackagedintoazipfile(forexample,
on Windows), or was found indirectly (for example, by pyenv-virtualenv). A number of different scenarios were
described in issue 862 which is now fixed. Huge thanks to Agbonze O. Jeremiah for reporting it, and Alexander
Waters and George-Cristian Bîrzan for protracted debugging sessions.
• Added the “premain” debug option.
• Added SQLite compile-time options to the “debug sys” output.
6.15.41 Version 5.0.2 — 2020-01-05
• Programs that used multiprocessing and changed directories would fail under coverage. This is now fixed (issue
890). A side effect is that debug information about the config files read now shows absolute paths to the files.
• When running programs as modules (coverage run -m ) with --source, some measured modules were im-
ported before coverage starts. This resulted in unwanted warnings (“Already imported a file that will be mea-
sured”) and a reduction in coverage totals (issue 909). This is now fixed.
• Ifnodatawascollected,anexceptionabout“Nodatatoreport”couldhappeninsteadofa0%reportbeingcreated
(issue 884). This is now fixed.
• The handling of source files with non-encodable file names has changed. Previously, if a file name could not be
encoded as UTF-8, an error occurred, as described in issue 891. Now, those files will not be measured, since
their data would not be recordable.
• A new warning (“dynamic-conflict”) is issued if two mechanisms are trying to change the dynamic context.
Closes issue 901.
• coverage run --debug=sys would fail with an AttributeError. This is now fixed (issue 907).
6.15. Change history for coverage.py 95

Coverage.py, Release 7.2.2
6.15.42 Version 5.0.1 — 2019-12-22
• If a 4.x data file is the cause of a “file is not a database” error, then use a more specific error message, “Looks
like a coverage 4.x data file, are you mixing versions of coverage?” Helps diagnose the problems described in
issue 886.
• Measurement contexts and relative file names didn’t work together, as reported in issue 899 and issue 900. This
is now fixed, thanks to David Szotten.
• Whenusing coverage run --concurrency=multiprocessing ,alldatafilesshouldbenamedwithparallel-
ready suffixes. 5.0 mistakenly named the main process’ file with no suffix when using--append. This is now
fixed, closing issue 880.
• Fixed a problem on Windows when the current directory is changed to a different drive (issue 895). Thanks,
Olivier Grisel.
• Updated Python 3.9 support to 3.9a2.
6.15.43 Version 5.0 — 2019-12-14
Nothing new beyond 5.0b2.
A summary of major changes in 5.0 since 4.5.x is in see whatsnew5x.
6.15.44 Version 5.0b2 — 2019-12-08
• An experimental [run] relative_files setting tells coverage to store relative file names in the data file.
This makes it easier to run tests in one (or many) environments, and then report in another. It has not had much
real-world testing, so it may change in incompatible ways in the future.
• Whenconstructinga coverage.Coverageobject,data_filecanbespecifiedasNonetopreventwritinganydata
fileatall. Inpreviousversions,anexplicit data_file=Noneargumentwouldusethedefaultof“.coverage”. Fixes
issue 871.
• Pythonfiles runwith -mnow have__spec__definedproperly. This fixesissue 745(about notbeing ableto run
unittest tests that spawn subprocesses), and issue 838, which described the problem directly.
• The [paths] configuration section is now ordered. If you specify more than one list of patterns, the first one
that matches will be used. Fixes issue 649.
• The coverage.numbits.register_sqlite_functions()functionnowalsoregisters numbits_to_numsfor
use in SQLite queries. Thanks, Simon Willison.
• Python 3.9a1 is supported.
• Coverage.py has a mascot:Sleepy Snake.
6.15.45 Version 5.0b1 — 2019-11-11
• The HTML and textual reports now have a--skip-empty option that skips files with no statements, notably
__init__.pyfiles. Thanks, Reya B.
• Configuration can now be read from TOML files. This requires installing coverage.py with the[toml] extra.
Thestandard“pyproject.toml”filewillbereadautomaticallyifnootherconfigurationfileisfound,withsettings
inthe [tool.coverage.]namespace. ThankstoFrazerMcLeanforimplementationandpersistence. Finishes
issue 664.
96 Chapter 6. More information

Coverage.py, Release 7.2.2
• The [run] note setting has been deprecated. Using it will result in a warning, and the note will not be written
to the data file. The correspondingCoverageData methods have been removed.
• The HTML report has been reimplemented (no more table around the source code). This allowed for a better
presentation of the context information, hopefully resolving issue 855.
• Added sqlite3 module version information tocoverage debug sys output.
• Asking the HTML report to show contexts ( [html] show_contexts=True or coverage html
--show-contexts) will issue a warning if there were no contexts measured (issue 851).
6.15.46 Version 5.0a8 — 2019-10-02
• The CoverageDataAPIhaschangedhowqueriesarelimitedtospecificcontexts. Nowyouuse CoverageData.
set_query_context()tosetasingleexact-matchstring, or CoverageData.set_query_contexts()toset
alistofregularexpressionstomatchcontexts. Thischangesthecommand-line --contextsoptiontouseregular
expressions instead of filename-style wildcards.
6.15.47 Version 5.0a7 — 2019-09-21
• Datacannowbe“reported”inJSONformat,forprogrammaticuse,asrequestedinissue720. Thenew coverage
jsoncommand writes raw and summarized data to a JSON file. Thanks, Matt Bachmann.
• Dynamic contexts are now supported in the Python tracer, which is important for PyPy users. Closes issue 846.
• The compact line number representation introduced in 5.0a6 is called a “numbits.” Thecoverage.numbits
module provides functions for working with them.
• The reporting methods used to permanently apply their arguments to the configuration of the Coverage object.
Now they no longer do. The arguments affect the operation of the method, but do not persist.
• A class named “test_something” no longer confuses thetest_function dynamic context setting. Fixes issue
829.
• Fixed an unusual tokenizing issue with backslashes in comments. Fixes issue 822.
• debug=plugindidn’tproperlysupportconfigurationordynamiccontextplugins, butnowitdoes, closingissue
834.
6.15.48 Version 5.0a6 — 2019-07-16
• Reporting on contexts. Big thanks to Stephan Richter and Albertas Agejevas for the contribution.
–The --contexts option is available on thereport and html commands. It’s a comma-separated list of
shell-stylewildcards, selectingthecontextstoreporton. Onlycontextsmatchingoneofthewildcardswill
be included in the report.
–The --show-contextsoptionforthe htmlcommandaddscontextinformationtoeachcoveredline. Hov-
ering over the “ctx” marker at the end of the line reveals a list of the contexts that covered the line.
• Database changes:
–Linenumbersarenowstoredinamuchmorecompactway. Foreachfileandcontext,asinglebinarystring
is stored with a bit per line number. This greatly improves memory use, but makes ad-hoc use difficult.
–Dynamic contexts with no data are no longer written to the database.
–SQLitedatastorageisnowfaster. There’snolongerareasontokeeptheJSONdatafilecode,soithasbeen
removed.
6.15. Change history for coverage.py 97

Coverage.py, Release 7.2.2
• Changes to theCoverageData interface:
–The new CoverageData.dumps() method serializes the data to a string, and a corresponding
CoverageData.loads()methodreconstitutesthisdata. Theformatofthedatastringissubjecttochange
at any time, and so should only be used between two installations of the same version of coverage.py.
–The CoverageData constructor has a new argument,no_disk (default: False). Setting it to True pre-
vents writing any data to the disk. This is useful for transient data objects.
• Added the class methodCoverage.current() to get the latest started Coverage instance.
• Multiprocessing support in Python 3.8 was broken, but is now fixed. Closes issue 828.
• Error handling during reporting has changed slightly. All reporting methods now behave the same. The
--ignore-errors option keeps errors from stopping the reporting, but files that couldn’t parse as Python
will always be reported as warnings. As with other warnings, you can suppress them with the [run]
disable_warningsconfiguration setting.
• Coverage.py no longer fails if the user program deletes its current directory. Fixes issue 806. Thanks, Dan
Hemberger.
• The scrollbar markers in the HTML report now accurately show the highlighted lines, regardless of what cate-
gories of line are highlighted.
• ThehacktoaccommodateShiningPandalookingforanobsoleteinternaldatafilehasbeenremoved,sinceShin-
ingPanda 0.22 fixed it four years ago.
• The deprecatedReporter.file_reportersproperty has been removed.
6.15.49 Version 5.0a5 — 2019-05-07
• Drop support for Python 3.4
• Dynamic contexts can now be set two new ways, both thanks to Justas Sadzevičius.
–A plugin can implement adynamic_context method to check frames for whether a new context should
be started. SeeDynamic Context Switchersfor more details.
–Another tool (such as a test runner) can use the newCoverage.switch_context()method to explicitly
change the context.
• The dynamic_context = test_function setting now works with Python 2 old-style classes, though it only
reports the method name, not the class it was defined on. Closes issue 797.
• fail_undervalues more than 100 are reported as errors. Thanks to Mike Fiedler for closing issue 746.
• The “missing” values in the text output are now sorted by line number, so that missing branches are reported
near the other lines they affect. The values used to show all missing lines, and then all missing branches.
• Access to the SQLite database used for data storage is now thread-safe. Thanks, Stephan Richter. This closes
issue 702.
• Combining data stored in SQLite is now about twice as fast, fixing issue 761. Thanks, Stephan Richter.
• The filename attribute on CoverageData objects has been made private. You can use thedata_filename
method to get the actual file name being used to store data, and thebase_filename method to get the original
filename before parallelizing suffixes were added. This is part of fixing issue 708.
• LinenumbersintheHTMLreportnowalignproperlywithsourcelines,evenwhenChrome’sminimumfontsize
is set, fixing issue 748. Thanks Wen Ye.
98 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.50 Version 5.0a4 — 2018-11-25
• You can specify the command line to run your program with the[run] command_line configuration setting,
as requested in issue 695.
• Coverage will create directories as needed for the data file if they don’t exist, closing issue 721.
• The coverage run command has always adjusted the first entry in sys.path, to properly emulate how Python
runsyourprogram. Nowthisadjustmentisskippedifsys.path[0]isalreadydifferentthanPython’sdefault. This
fixes issue 715.
• Improvements to context support:
–The “no such table: meta” error is fixed.: issue 716.
–Combining data files is now much faster.
• Python 3.8 (as of today!) passes all tests.
6.15.51 Version 5.0a3 — 2018-10-06
• Context support: static contexts let you specify a label for a coverage run, which is recorded in the data, and
retained when you combine files. SeeMeasurement contextsfor more information.
• Dynamic contexts: specifying[run] dynamic_context = test_function in the config file will record the
test function name as a dynamic context during execution. This is the core of “Who Tests What” (issue 170).
Things to note:
–Thereisnoreportingsupportyet. UseSQLitetoquerythe.coveragefileforinformation. Ideasarewelcome
about how reporting could be extended to use this data.
–There’s a noticeable slow-down before any test is run.
–Data files will now be roughly N times larger, where N is the number of tests you have. Combining data
files is therefore also N times slower.
–No other values fordynamic_context are recognized yet. Let me know what else would be useful. I’d
like to use a pytest plugin to get better information directly from pytest, for example.
• Environment variable substitution in configuration files now supports two syntaxes for controlling the behavior
of undefined variables: ifVARNAMEis not defined,${VARNAME?} will raise an error, and${VARNAME-default
value} will use “default value”.
• Partial support for Python 3.8, which has not yet released an alpha. Fixes issue 707 and issue 714.
6.15.52 Version 5.0a2 — 2018-09-03
• Coverage’s data storage has changed. In version 4.x, .coverage files were basically JSON. Now, they are SQLite
databases. This means the data file can be created earlier than it used to. A large amount of code was refactored
to support this change.
–Because the data file is created differently than previous releases, you may needparallel=true where
you didn’t before.
–The old data format is still available (for now) by setting the environment variable COVER-
AGE_STORAGE=json. Please tell me if you think you need to keep the JSON format.
–Thedatabaseschemaisguaranteedtochangeinthefuture,tosupportnewfeatures. I’mlookingforopinions
about making the schema part of the public API to coverage.py or not.
• Development moved from Bitbucket to GitHub.
6.15. Change history for coverage.py 99

Coverage.py, Release 7.2.2
• HTML files no longer have trailing and extra white space.
• The sort order in the HTML report is stored in local storage rather than cookies, closing issue 611. Thanks,
Federico Bond.
• pickle2json, for converting v3 data files to v4 data files, has been removed.
6.15.53 Version 5.0a1 — 2018-06-05
• Coverage.py no longer supports Python 2.6 or 3.3.
• The location of the configuration file can now be specified with aCOVERAGE_RCFILE environment variable, as
requested in issue 650.
• NamespacepackagesaresupportedonPython3.7,wheretheyusedtocauseTypeErrorsaboutpathbeingNone.
Fixes issue 700.
• A new warning (already-imported) is issued if measurable files have already been imported before cover-
age.py started measurement. SeeWarningsfor more information.
• Running coverage many times for small runs in a single process should be faster, closing issue 625. Thanks,
David MacIver.
• Large HTML report pages load faster. Thanks, Pankaj Pandey.
6.15.54 Version 4.5.4 — 2019-07-29
• Multiprocessing support in Python 3.8 was broken, but is now fixed. Closes issue 828.
6.15.55 Version 4.5.3 — 2019-03-09
• Only packaging metadata changes.
6.15.56 Version 4.5.2 — 2018-11-12
• NamespacepackagesaresupportedonPython3.7,wheretheyusedtocauseTypeErrorsaboutpathbeingNone.
Fixes issue 700.
• Python 3.8 (as of today!) passes all tests. Fixes issue 707 and issue 714.
• Development moved from Bitbucket to GitHub.
6.15.57 Version 4.5.1 — 2018-02-10
• Nowthat4.5properlyseparatedthe [run] omit and [report] omit settings,anoldbughasbecomeapparent.
Ifyouspecifiedapackagenamefor [run] source ,thenomitpatternsweren’tmatchedinsidethatpackage. This
bug (issue 638) is now fixed.
• OnPython3.7,reportingaboutadecoratedfunctionwithnobodyotherthanadocstringwouldcrashcoverage.py
with an IndexError (issue 640). This is now fixed.
• Configurer plugins are now reported in the output of--debug=sys.
100 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.58 Version 4.5 — 2018-02-03
• Anewkindofpluginissupported: configurersareinvokedatstart-uptoallowmorecomplexconfigurationthan
the.coveragercfilecaneasilydo. See Plug-inclasses fordetails. Thissolvesthecomplexconfigurationproblem
described in issue 563.
• The fail_underoptioncannowbeafloat. Notethatyoumustspecifythe [report] precision configuration
optionforthefractionalparttobeused. ThankstoLarsHupfeldtNielsenforhelpwiththeimplementation. Fixes
issue 631.
• The include and omit options can be specified for both the[run] and [report] phases of execution. 4.4.2
introduced some incorrect interactions between those phases, where the options for one were confused for the
other. This is now corrected, fixing issue 621 and issue 622. Thanks to Daniel Hahler for seeing more clearly
than I could.
• The coverage combine commandusedtoalwaysoverwritethedatafile,evenwhennodatahadbeenreadfrom
apparently combinable files. Now, an error is raised if we thought there were files to combine, but in fact none
of them could be used. Fixes issue 629.
• The coverage combine commandcouldgetconfusedaboutpathseparatorswhencombiningdatacollectedon
Windows with data collected on Linux, as described in issue 618. This is now fixed: the result path always uses
the path separator specified in the[paths]result.
• On Windows, the HTML report could fail when source trees are deeply nested, due to attempting to create
HTML filenames longer than the 250-character maximum. Now filenames will never get much larger than 200
characters, fixing issue 627. Thanks to Alex Sandro for helping with the fix.
6.15.59 Version 4.4.2 — 2017-11-05
• Support for Python 3.7. In some cases, class and module docstrings are no longer counted in statement totals,
which could slightly change your total results.
• Specifying both --source and --include no longer silently ignores the include setting, instead it displays a
warning. Thanks, Loïc Dachary. Closes issue 265 and issue 101.
• Fixedaraceconditionwhensavingdataandmultiplethreadsaretracing(issue581). Itcouldproducea“dictio-
nary changed size during iteration” RuntimeError. I believe this mostly but not entirely fixes the race condition.
A true fix would likely be too expensive. Thanks, Peter Baughman for the debugging, and Olivier Grisel for the
fix with tests.
• Configuration values which are file paths will now apply tilde-expansion, closing issue 589.
• Now secondary config files like tox.ini and setup.cfg can be specified explicitly, and prefixed sections like[cov-
erage:run]will be read. Fixes issue 588.
• Be more flexible about the command name displayed by help, fixing issue 600. Thanks, Ben Finney.
6.15.60 Version 4.4.1 — 2017-05-14
• No code changes: just corrected packaging for Python 2.7 Linux wheels.
6.15. Change history for coverage.py 101

Coverage.py, Release 7.2.2
6.15.61 Version 4.4 — 2017-05-07
• Reports could produce the wrong file names for packages, reportingpkg.py instead of the correct pkg/
__init__.py. This is now fixed. Thanks, Dirk Thomas.
• XML reports could produce<source> and <class> lines that together didn’t specify a valid source file path.
This is now fixed. (issue 526)
• Namespace packages are no longer warned as having no code. (issue 572)
• Codethatuses sys.settrace(sys.gettrace())inafilethatwasn’tbeingcoverage-measuredwouldprevent
correct coverage measurement in following code. An example of this was running doctests programmatically.
This is now fixed. (issue 575)
• Errors printed by thecoverage command now go to stderr instead of stdout.
• Running coverage xml in a directory named with non-ASCII characters would fail under Python 2. This is
now fixed. (issue 573)
6.15.62 Version 4.4b1 — 2017-04-04
• Some warnings can now be individually disabled. Warnings that can be disabled have a short name appended.
The [run] disable_warnings settingtakesalistofthesewarningnamestodisable. Closesbothissue96and
issue 355.
• The XML report now includes attributes from version 4 of the Cobertura XML format, fixing issue 570.
• In previous versions, calling a method that used collected data would prevent further collection. For example,
save(),report(),html_report(),andotherswouldallstopcollection. Anexplicit start()wasneededtogetitgoing
again. Thisisnolongertrue. Nowyoucanusethecollecteddataandalsocontinuemeasurement. Bothissue79
and issue 448 described this problem, and have been fixed.
• Plugins can now find un-executed files if they choose, by implementing thefind_executable_files method.
Thanks, Emil Madsen.
• Minimal IronPython support. You should be able to run IronPython programs undercoverage run , though
you will still have to do the reporting phase with CPython.
• Coverage.py has long had a special hack to support CPython’s need to measure the coverage of the standard
library tests. This code was not installed by kitted versions of coverage.py. Now it is.
6.15.63 Version 4.3.4 — 2017-01-17
• Fixing 2.6 in version 4.3.3 broke other things, because the too-tricky exception wasn’t properly derived from
Exception, described in issue 556. A newb mistake; it hasn’t been a good few days.
6.15.64 Version 4.3.3 — 2017-01-17
• Python 2.6 support was broken due to a testing exception imported for the benefit of the coverage.py test suite.
Properly conditionalizing it fixed issue 554 so that Python 2.6 works again.
102 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.65 Version 4.3.2 — 2017-01-16
• Using the--skip-coveredoption on an HTML report with 100% coverage would cause a “No data to report”
error, as reported in issue 549. This is now fixed; thanks, Loïc Dachary.
• If-statements can be optimized away during compilation, for example,if 0:or if __debug__:. Coverage.py had
problemsproperlyunderstandingthesestatementswhichexistedinthesource,butnotinthecompiledbytecode.
This problem, reported in issue 522, is now fixed.
• If you specified--sourceas a directory, then coverage.py would look for importable Python files in that direc-
tory, and could identify ones that had never been executed at all. But if you specified it as a package name, that
detection wasn’t performed. Now it is, closing issue 426. Thanks to Loïc Dachary for the fix.
• If you started and stopped coverage measurement thousands of times in your process, you could crash Python
witha“FatalPythonerror: deallocatingNone”error. Thisisnowfixed. ThankstoAlexGroceforthebugreport.
• OnPyPy,measuringcoverageinsubprocessescouldproduceawarning: “Tracefunctionchanged,measurement
is likely wrong: None”. This was spurious, and has been suppressed.
• Previously, coverage.py couldn’t start on Jython, due to that implementation missing the multiprocessing mod-
ule (issue 551). This problem has now been fixed. Also, issue 322 about not being able to invoke coverage
conveniently, seems much better:jython -m coverage run myprog.py works properly.
• Let’ssayyourantheHTMLreportoverandoveragaininthesameoutputdirectory,with --skip-covered. And
imagineduetoyourheroictest-writingefforts, afilejustachievedthegoalof100%coverage. Withcoverage.py
4.3,theoldHTMLfilewiththeless-than-100%coveragewouldbeleftbehind. Thisfileisnowproperlydeleted.
6.15.66 Version 4.3.1 — 2016-12-28
• Some environments couldn’t install 4.3, as described in issue 540. This is now fixed.
• The check for conflicting--source and --include was too simple in a few different ways, breaking a few
perfectly reasonableuse cases, describedin issue 541. Thecheck hasbeen reverted whilewe re-thinkthe fix for
issue 265.
6.15.67 Version 4.3 — 2016-12-27
Special thanks toLoïc Dachary, who took an extraordinary interest in coverage.py and contributed a number of im-
provements in this release.
• Subprocesses that are measured with automatic subprocess measurement used to read in any pre-existing data
file. Thismeantdatawouldbeincorrectlycarriedforwardfromruntorun. Nowthosefilesarenotread,soeach
subprocess only writes its own data. Fixes issue 510.
• The coverage combine command will now fail if there are no data files to combine. The combine changes in
4.2meantthatmultiplecombinescouldlosedata,leavingyouwithanempty.coveragedatafile. Fixesissue525,
issue 412, issue 516, and probably issue 511.
• Coverage.pywouldn’texecutesys.excepthookwhenanexceptionhappenedinyourprogram. Nowitdoes,thanks
to Andrew Hoos. Closes issue 535.
• Branch coverage fixes:
–Branchcoveragecouldmisunderstandafinallyclauseonatryblockthatnevercontinuedontothefollowing
statement, as described in issue 493. This is now fixed. Thanks to Joe Doherty for the report and Loïc
Dachary for the fix.
–A while loop with a constant condition (while True) and a continue statement would be mis-analyzed, as
described in issue 496. This is now fixed, thanks to a bug report by Eli Skeggs and a fix by Loïc Dachary.
6.15. Change history for coverage.py 103

Coverage.py, Release 7.2.2
–While loops with constant conditions that were never executed could result in a non-zero coverage report.
Artem Dayneko reported this in issue 502, and Loïc Dachary provided the fix.
• The HTML report now supports a--skip-covered option like the other reporting commands. Thanks, Loïc
Dachary for the implementation, closing issue 433.
• Options can now be read from a tox.ini file, if any. Like setup.cfg, sections are prefixed with “coverage:”, so
[run]optionswillbereadfromthe [coverage:run]sectionoftox.ini. Implementspartofissue519. Thanks,
Stephen Finucane.
• Specifying both--source and --include no longer silently ignores the include setting, instead it fails with a
message. Thanks, Nathan Land and Loïc Dachary. Closes issue 265.
• The Coverage.combine method has a new parameter,strict=False, to support failing if there are no data
files to combine.
• When forking subprocesses, the coverage data files would have the same random number appended to the file
name. This didn’t cause problems, because the file names had the process id also, making collisions (nearly)
impossible. But it was disconcerting. This is now fixed.
• The text report now properly sizes headers when skipping some files, fixing issue 524. Thanks, Anthony Sottile
and Loïc Dachary.
• Coverage.py can now search .pex files for source, just as it can .zip and .egg. Thanks, Peter Ebden.
• Data files are now about 15% smaller.
• Improvements in the[run] debug setting:
–The “dataio” debug setting now also logs when data files are deleted during combining or erasing.
–A new debug option, “multiproc”, for logging the behavior ofconcurrency=multiprocessing.
–If you used the debug options “config” and “callers” together, you’d get a call stack printed for every line
in the multi-line config output. This is now fixed.
• Fixedanunusualbuginvolvingmultiplecodingdeclarationsaffectingcodecontainingcodeinmulti-linestrings:
issue 529.
• Coverage.py will no longer be misled into thinking that a plain file is a package when interpreting--source
options. Thanks, Cosimo Lupo.
• If you try to run a non-Python file with coverage.py, you will now get a more useful error message. Issue 514.
• Thedefaultpragmaregexchangedslightly,butthiswillonlymattertoyouifyouarederangedandusemixed-case
pragmas.
• Deal properly with non-ASCII file names in an ASCII-only world, issue 533.
• Programs that set Unicode configuration values could cause UnicodeErrors when generating HTML reports.
Pytest-cov is one example. This is now fixed.
• Prevented deprecation warnings from configparser that happened in some circumstances, closing issue 530.
• Corrected the name of the jquery.ba-throttle-debounce.js library. Thanks, Ben Finney. Closes issue 505.
• Testing against PyPy 5.6 and PyPy3 5.5.
• Switched to pytest from nose for running the coverage.py tests.
• RenamedAUTHORS.txttoCONTRIBUTORS.txt,sincethereareotherwaystocontributethanbywritingcode.
Also put the count of contributors into the author string in setup.py, though this might be too cute.
104 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.68 Version 4.2 — 2016-07-26
• Since concurrency=multiprocessingusessubprocesses,optionsspecifiedonthecoverage.pycommandline
will not be communicated down to them. Only options in the configuration file will apply to the subprocesses.
Previously, the options didn’t apply to the subprocesses, but there was no indication. Now it is an error to
use --concurrency=multiprocessing and other run-affecting options on the command line. This prevents
failures like those reported in issue 495.
• Filtering the HTML report is now faster, thanks to Ville Skyttä.
6.15.69 Version 4.2b1 — 2016-07-04
Work from the PyCon 2016 Sprints!
• BACKWARD INCOMPATIBILITY: thecoverage combine command now ignores an existing.coverage
data file. It used to include that file in its combining. This caused confusing results, and extra tox “clean” steps.
If you want the old behavior, use the newcoverage combine --append option.
• The concurrencyoptioncannowtakemultiplevalues,tosupportprogramsusingmultiprocessingandanother
library such as eventlet. This is only possible in the configuration file, not from the command line. The config-
uration file is the only way for sub-processes to all run with the same options. Fixes issue 484. Thanks to Josh
Williams for prototyping.
• Using a concurrency setting of multiprocessing now implies --parallel so that the main program is
measured similarly to the sub-processes.
• When using automatic subprocess measurement, running coverage commands would create spurious data files.
This is now fixed, thanks to diagnosis and testing by Dan Riti. Closes issue 492.
• A new configuration option,report:sort, controls what column of the text report is used to sort the rows.
Thanks to Dan Wandschneider, this closes issue 199.
• The HTML report has a more-visible indicator for which column is being sorted. Closes issue 298, thanks to
Josh Williams.
• If the HTML report cannot find the source for a file, the message now suggests using the-i flag to allow the
report to continue. Closes issue 231, thanks, Nathan Land.
• When reports are ignoring errors, there’s now a warning if a file cannot be parsed, rather than being silently
ignored. Closes issue 396. Thanks, Matthew Boehm.
• A new option forcoverage debug is available: coverage debug config shows the current configuration.
Closes issue 454, thanks to Matthew Boehm.
• Running coverage as a module (python -m coverage ) no longer shows the program name as__main__.py.
Fixes issue 478. Thanks, Scott Belden.
• Thetest_helpersmodule has been moved into a separate pip-installable package: unittest-mixins.
6.15. Change history for coverage.py 105

Coverage.py, Release 7.2.2
6.15.70 Version 4.1 — 2016-05-21
• The internal attributeReporter.file_reporterswas removed in 4.1b3. It should have come has no surprise that
there were third-party tools out there using that attribute. It has been restored, but with a deprecation warning.
6.15.71 Version 4.1b3 — 2016-05-10
• Whenrunningyourprogram,executioncanjumpfroman except X: linetosomeotherlinewhenanexception
other thanXhappens. This jump is no longer considered a branch when measuring branch coverage.
• When measuring branch coverage,yieldstatements that were never resumed were incorrectly marked as miss-
ing, as reported in issue 440. This is now fixed.
• During branch coverage of single-line callables like lambdas and generator expressions, coverage.py can now
distinguish between them never being called, or being called but not completed. Fixes issue 90, issue 460 and
issue 475.
• The HTML report now has a map of the file along the rightmost edge of the page, giving an overview of where
the missed lines are. Thanks, Dmitry Shishov.
• The HTML report now uses different monospaced fonts, favoring Consolas over Courier. Along the way, issue
472 about not properly handling one-space indents was fixed. The index page also has slightly different styling,
to try to make the clickable detail pages more apparent.
• Missing branches reported withcoverage report -m will now say->exitfor missed branches to the exit of
a function, rather than a negative number. Fixes issue 469.
• coverage --help and coverage --version now mention which tracer is installed, to help diagnose prob-
lems. The docs mention which features need the C extension. (issue 479)
• Officially support PyPy 5.1, which required no changes, just updates to the docs.
• The Coverage.report function had two parameters with non-None defaults, which have been changed.
show_missingusedtodefaulttoTrue,butnowdefaultstoNone. Ifyouhadbeencalling Coverage.reportwithout
specifyingshow_missing,you’llneedtoexplicitlysetittoTruetokeepthesamebehavior. skip_coveredusedto
default to False. It is now None, which doesn’t change the behavior. This fixes issue 485.
• It’s never been possible to pass a namespace module to one of the analysis functions, but now at least we raise a
more specific error message, rather than getting confused. (issue 456)
• Thecoverage.process_startupfunction now returns theCoverageinstance it creates, as suggested in issue 481.
• Makeasmalltweaktohowwecomparethreads,toavoidbuggycustomcomparisoncodeinthreadclasses. (issue
245)
6.15.72 Version 4.1b2 — 2016-01-23
• Problems with the new branch measurement in 4.1 beta 1 were fixed:
–Class docstrings were considered executable. Now they no longer are.
–yield from and await were considered returns from functions, since they could transfer control to the
caller. This produced unhelpful “missing branch” reports in a number of circumstances. Now they no
longer are considered returns.
–In unusual situations, a missing branch to a negative number was reported. This has been fixed, closing
issue 466.
• TheXMLreportnowproducescorrectpackagenamesformodulesfoundindirectoriesspecifiedwith source=.
Fixes issue 465.
106 Chapter 6. More information

Coverage.py, Release 7.2.2
• coverage report won’t produce trailing white space.
6.15.73 Version 4.1b1 — 2016-01-10
• Branchanalysishasbeenrewritten: itusedtobebasedonbytecode,butnowusesASTanalysis. Thishaschanged
a number of things:
–More code paths are now considered runnable, especially intry/except structures. This may mean that
coverage.py will identify more code paths as uncovered. This could either raise or lower your overall
coverage number.
–Python 3.5’sasyncand await keywords are properly supported, fixing issue 434.
–Some long-standing branch coverage bugs were fixed:
∗ issue129: functionswithonlyadocstringforabodywouldincorrectlyreportamissingbranchonthe
def line.
∗ issue 212: code in anexcept block could be incorrectly marked as a missing branch.
∗ issue 146: context managers (withstatements) in a loop ortryblock could confuse the branch mea-
surement, reporting incorrect partial branches.
∗ issue 422: in Python 3.5, an actual partial branch could be marked as complete.
• Pragmas to disable coverage measurement can now be used on decorator lines, and they will apply to the entire
function or class being decorated. This implements the feature requested in issue 131.
• Multiprocessing support is now available on Windows. Thanks, Rodrigue Cloutier.
• Files with two encoding declarations are properly supported, fixing issue 453. Thanks, Max Linke.
• Non-ascii characters in regexes in the configuration file worked in 3.7, but stopped working in 4.0. Now they
work again, closing issue 455.
• Form-feed characters would prevent accurate determination of the beginning of statements in the rest of the file.
This is now fixed, closing issue 461.
6.15.74 Version 4.0.3 — 2015-11-24
• Fixedamysteriousproblemthatmanifestedindifferentways: sometimeshangingtheprocess(issue420),some-
times making database connections fail (issue 445).
• The XML report now has correct<source> elements when using a--source= option somewhere besides the
current directory. This fixes issue 439. Thanks, Arcadiy Ivanov.
• Fixed an unusual edge case of detecting source encodings, described in issue 443.
• Help messages that mention the command to use now properly use the actual command name, which might be
different than “coverage”. Thanks to Ben Finney, this closes issue 438.
6.15. Change history for coverage.py 107

Coverage.py, Release 7.2.2
6.15.75 Version 4.0.2 — 2015-11-04
• More work on supporting unusually encoded source. Fixed issue 431.
• Files or directories with non-ASCII characters are now handled properly, fixing issue 432.
• Setting a trace function with sys.settrace was broken by a change in 4.0.1, as reported in issue 436. This is now
fixed.
• Officially support PyPy 4.0, which required no changes, just updates to the docs.
6.15.76 Version 4.0.1 — 2015-10-13
• When combining data files, unreadable files will now generate a warning instead of failing the command. This
is more in line with the older coverage.py v3.7.1 behavior, which silently ignored unreadable files. Prompted by
issue 418.
• The –skip-covered option would skip reporting on 100% covered files, but also skipped them when calculating
totalcoverage. Thiswaswrong, itshouldonlyremovelinesfromthereport, notchangethefinalanswer. Thisis
now fixed, closing issue 423.
• In 4.0, the data file recorded a summary of the system on which it was run. Combined data files would keep all
of those summaries. This could lead to enormous data files consisting of mostly repetitive useless information.
That summary is now gone, fixing issue 415. If you want summary information, get in touch, and we’ll figure
out a better way to do it.
• Test suites that mocked os.path.exists would experience strange failures, due to coverage.py using their mock
inadvertently. This is now fixed, closing issue 416.
• Importinga __init__moduleexplicitlywouldleadtoanerror: AttributeError: 'module' object has
no attribute '__path__', as reported in issue 410. This is now fixed.
• Codethatuses sys.settrace(sys.gettrace())usedtoincuramorethan2xspeedpenalty. Nowthere’sno
penalty at all. Fixes issue 397.
• Pyexpat C code will no longer be recorded as a source file, fixing issue 419.
• Thesourcekitnowcontainsallofthefilesneededtohaveacompletesourcetree,re-fixingissue137andclosing
issue 281.
6.15.77 Version 4.0 — 2015-09-20
No changes from 4.0b3
6.15.78 Version 4.0b3 — 2015-09-07
• Reporting on an unmeasured file would fail with a traceback. This is now fixed, closing issue 403.
• The Jenkins ShiningPanda plugin looks for an obsolete file name to find the HTML reports to publish, so it was
failing under coverage.py 4.0. Now we create that file if we are running under Jenkins, to keep things working
smoothly. issue 404.
• Kits used to include tests and docs, but didn’t install them anywhere, or provide all of the supporting tools to
makethem useful. Kits nolonger includetestsand docs. If youwere usingthemfrom theolderpackages, get in
touch and help me understand how.
108 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.79 Version 4.0b2 — 2015-08-22
• 4.0b1 broke--append creating new data files. This is now fixed, closing issue 392.
• py.test --cov can write empty data, then touch files due to--source, which made coverage.py mistakenly
force the data file to record lines instead of arcs. This would lead to a “Can’t combine line data with arc data”
error message. This is now fixed, and changed some method names in the CoverageData interface. Fixes issue
399.
• CoverageData.read_fileobjand CoverageData.write_fileobjreplace the.read and .write methods, and are now
properly inverses of each other.
• When using report --skip-covered , a message will now be included in the report output indicating how
manyfileswereskipped, andifallfilesareskipped,coverage.pywon’taccidentallyscoldyouforhavingnodata
to report. Thanks, Krystian Kichewko.
• A new conversion utility has been added:python -m coverage.pickle2json will convert v3.x pickle data
files to v4.x JSON data files. Thanks, Alexander Todorov. Closes issue 395.
• A new version identifier is available,coverage.version_info, a plain tuple of values similar to sys.version_info.
6.15.80 Version 4.0b1 — 2015-08-02
• Coverage.py is now licensed under the Apache 2.0 license. See NOTICE.txt for details. Closes issue 313.
• The data storage has been completely revamped. The data file is now JSON-based instead of a pickle, closing
issue 236. TheCoverageDataclass is now a public supported documented API to the data file.
• A new configuration option,[run] note , lets you set a note that will be stored in theruns section of the data
file. You can use this to annotate the data file with any information you like.
• Unrecognized configuration options will now print an error message and stop coverage.py. This should help
prevent configuration mistakes from passing silently. Finishes issue 386.
• In parallel mode,coverage erase will now delete all of the data files, fixing issue 262.
• Coverage.py now accepts a directory name forcoverage run and will run a__main__.py found there, just
like Python will. Fixes issue 252. Thanks, Dmitry Trofimov.
• The XML report now includes amissing-branches attribute. Thanks, Steve Peak. This is not a part of the
Cobertura DTD, so the XML report no longer references the DTD.
• MissingbranchesintheHTMLreportnowhaveabitmoreinformationintheright-handannotations. Hopefully
this will make their meaning clearer.
• All the reporting functions now behave the same if no data had been collected, exiting with a status code of 1.
Fixed fail_under to be applied even when the report is empty. Thanks, Ionel Cristian Măries,.
• Plugins are now initialized differently. Instead of looking for a class calledPlugin, coverage.py looks for a
function calledcoverage_init.
• Afile-tracingplugincannowasktohavebuilt-inPythonreportingbyreturning “python”fromits file_reporter()
method.
• Code that was executed withexec would be mis-attributed to the file that called it. This is now fixed, closing
issue 380.
• The ability to use item access onCoverage.config(introduced in 4.0a2) has been changed to a more explicit
Coverage.get_optionand Coverage.set_optionAPI.
• The Coverage.use_cachemethod is no longer supported.
6.15. Change history for coverage.py 109

Coverage.py, Release 7.2.2
• The private method Coverage._harvest_data is now called Coverage.get_data, and returns the
CoverageDatacontaining the collected data.
• Theprojectisconsistentlyreferredtoas“coverage.py”throughoutthecodeandthedocumentation,closingissue
275.
• Combining data files with an explicit configuration file was broken in 4.0a6, but now works again, closing issue
385.
• coverage combine now accepts files as well as directories.
• The speed is back to 3.7.1 levels, after having slowed down due to plugin support, finishing up issue 387.
6.15.81 Version 4.0a6 — 2015-06-21
• Python 3.5b2 and PyPy 2.6.0 are supported.
• The original module-level function interface to coverage.py is no longer supported. You must now create a
coverage.Coverage object, and use methods on it.
• The coverage combine command now accepts any number of directories as arguments, and will combine
all the data files from those directories. This means you don’t have to copy the files to one directory before
combining. Thanks, Christine Lytwynec. Finishes issue 354.
• Branch coverage couldn’t properly handle certain extremely long files. This is now fixed (issue 359).
• Branch coverage didn’t understand yield statements properly. Mickie Betz persisted in pursuing this despite
Ned’s pessimism. Fixes issue 308 and issue 324.
• The COVERAGE_DEBUG environment variable can be used to set the[run] debug configuration option to
control what internal operations are logged.
• HTML reports were truncated at formfeed characters. This is now fixed (issue 360). It’s always fun when the
problem is due to a bug in the Python standard library.
• Files with incorrect encoding declaration comments are no longer ignored by the reporting commands, fixing
issue 351.
• HTML reports now include a time stamp in the footer, closing issue 299. Thanks, Conrad Ho.
• HTML reports now begrudgingly use double-quotes rather than single quotes, because there are “software en-
gineers” out there writing tools that read HTML and somehow have no idea that single quotes exist. Capitulates
to the absurd issue 361. Thanks, Jon Chappell.
• The coverage annotate command now handles non-ASCII characters properly, closing issue 363. Thanks,
Leonardo Pistone.
• Drive letters on Windows were not normalized correctly, now they are. Thanks, Ionel Cristian Măries,.
• Plugin support had some bugs fixed, closing issue 374 and issue 375. Thanks, Stefan Behnel.
110 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.82 Version 4.0a5 — 2015-02-16
• Plugin support is now implemented in the C tracer instead of the Python tracer. This greatly improves the speed
of tracing projects using plugins.
• Coverage.py now always adds the current directory to sys.path, so that plugins can import files in the current
directory (issue 358).
• If theconfig_fileargument to the Coverage constructor is specified as “.coveragerc”, it is treated as if it were
True. This means setup.cfg is also examined, and a missing file is not considered an error (issue 357).
• Wildly experimental: support for measuring processes started by the multiprocessing module. To use, set
--concurrency=multiprocessing,eitheronthecommandlineorinthe.coveragercfile(issue117). Thanks,
Eduardo Schettino. Currently, this does not work on Windows.
• Anewwarningispossible,ifadesiredfileisn’tmeasuredbecauseitwasimportedbeforecoverage.pywasstarted
(issue 353).
• The coverage.process_startupfunction now will start coverage measurement only once, no matter how many
times it is called. This fixes problems due to unusual virtualenv configurations (issue 340).
• Added 3.5.0a1 to the list of supported CPython versions.
6.15.83 Version 4.0a4 — 2015-01-25
• Plugins can now provide sys_info for debugging output.
• Started plugins documentation.
• Prepared to move the docs to readthedocs.org.
6.15.84 Version 4.0a3 — 2015-01-20
• Reports now use file names with extensions. Previously, a report would describe a/b/c.py as “a/b/c”. Now it is
shown as “a/b/c.py”. This allows for better support of non-Python files, and also fixed issue 69.
• The XML report now reports each directory as a package again. This was a bad regression, I apologize. This
was reported in issue 235, which is now fixed.
• A new configuration option for the XML report:[xml] package_depth controls which directories are iden-
tified as packages in the report. Directories deeper than this depth are not reported as packages. The default is
that all directories are reported as packages. Thanks, Lex Berezhny.
• When looking for the source for a frame, check if the file exists. On Windows, .pyw files are no longer recorded
as .py files. Along the way, this fixed issue 290.
• Empty files are now reported as 100% covered in the XML report, not 0% covered (issue 345).
• Regexes in the configuration file are now compiled as soon as they are read, to provide error messages earlier
(issue 349).
6.15. Change history for coverage.py 111

Coverage.py, Release 7.2.2
6.15.85 Version 4.0a2 — 2015-01-14
• OfficiallysupportPyPy2.4,andPyPy32.4. DropsupportforCPython3.2andolderversionsofPyPy. Thecode
won’t work on CPython 3.2. It will probably still work on older versions of PyPy, but I’m not testing against
them.
• Plugins!
• The original command line switches (-x to run a program, etc) are no longer supported.
• A new option:coverage report –skip-coveredwill reduce the number of files reported by skipping files with
100% coverage. Thanks, Krystian Kichewko. This means that empty__init__.py files will be skipped, since
they are 100% covered, closing issue 315.
• Youcannowspecifythe --fail-underoptioninthe .coveragercfileasthe [report] fail_under option.
This closes issue 314.
• The COVERAGE_OPTIONS environment variable is no longer supported. It was a hack for--timid before con-
figuration files were available.
• The HTML report now has filtering. Type text into the Filter box on the index page, and only modules with that
text in the name will be shown. Thanks, Danny Allen.
• The textual report and the HTML report used to report partial branches differently for no good reason. Now
the text report’s “missing branches” column is a “partial branches” column so that both reports show the same
numbers. This closes issue 342.
• If you specify a--rcfile that cannot be read, you will get an error message. Fixes issue 343.
• The --debugswitch can now be used on any command.
• Youcannowprogrammaticallyadjusttheconfigurationofcoverage.pybysettingitemson Coverage.configafter
construction.
• A module run with-m can be used as the argument to--source, fixing issue 328. Thanks, Buck Evan.
• The regex for matching exclusion pragmas has been fixed to allow more kinds of white space, fixing issue 334.
• Made some PyPy-specific tweaks to improve speed under PyPy. Thanks, Alex Gaynor.
• In some cases, with a source file missing a final newline, coverage.py would count statements incorrectly. This
is now fixed, closing issue 293.
• Thestatus.datfilethatHTMLreportsusetoavoidre-creatingfilesthathaven’tchangedisnowaJSONfileinstead
of a pickle file. This obviates issue 287 and issue 237.
6.15.86 Version 4.0a1 — 2014-09-27
• Python versions supported are now CPython 2.6, 2.7, 3.2, 3.3, and 3.4, and PyPy 2.2.
• Gevent, eventlet, and greenlet are now supported, closing issue 149. Theconcurrency setting specifies the
concurrency library in use. Huge thanks to Peter Portante for initial implementation, and to Joe Jevnik for the
final insight that completed the work.
• Options are now also read from a setup.cfg file, if any. Sections are prefixed with “coverage:”, so the[run]
options will be read from the[coverage:run] section of setup.cfg. Finishes issue 304.
• The report -m command can now show missing branches when reporting on branch coverage. Thanks, Steve
Leonard. Closes issue 230.
• The XML report now contains a <source> element, fixing issue 94. Thanks Stan Hu.
112 Chapter 6. More information

Coverage.py, Release 7.2.2
• The class defined in the coverage module is now calledCoverage instead of coverage, though the old name
still works, for backward compatibility.
• The fail-undervalueisnowroundedthesameasreportedresults, preventingparadoxicalresults, fixingissue
284.
• The XML report will now create the output directory if need be, fixing issue 285. Thanks, Chris Rose.
• HTML reports no longer raise UnicodeDecodeError if a Python file has un-decodable characters, fixing issue
303 and issue 331.
• Theannotate commandwill nowannotate allfiles, not justones relativeto thecurrent directory, fixingissue 57.
• ThecoveragemodulenolongercausesdeprecationwarningsonPython3.4byimportingtheimpmodule,fixing
issue 305.
• Encoding declarations in source files are only considered if they are truly comments. Thanks, Anthony Sottile.
6.15.87 Version 3.7.1 — 2013-12-13
• Improved the speed of HTML report generation by about 20%.
• Fixed the mechanism for finding OS-installed static files for the HTML report so that it will actually find OS-
installed static files.
6.15.88 Version 3.7 — 2013-10-06
• Added the--debugswitch tocoverage run . It accepts a list of options indicating the type of internal activity
to log to stderr.
• Improved the branch coverage facility, fixing issue 92 and issue 175.
• Running code withcoverage run -m now behaves more like Python does, setting sys.path properly, which
fixes issue 207 and issue 242.
• Coverage.py can now run .pyc files directly, closing issue 264.
• Coverage.py properly supports .pyw files, fixing issue 261.
• Omitting files within a tree specified with thesource option would cause them to be incorrectly marked as
un-executed, as described in issue 218. This is now fixed.
• When specifying paths to alias together during data combining, you can now specify relative paths, fixing issue
267.
• Most file paths can now be specified with username expansion (~/src, or~build/src, for example), and with
environment variable expansion (build/$BUILDNUM/src).
• TryingtocreateanXMLreportwithnofilestoreporton, wouldcauseaZeroDivisionError,butnolongerdoes,
fixing issue 250.
• When running a threaded program under the Python tracer, coverage.py no longer issues a spurious warning
about the trace function changing: “Trace function changed, measurement is likely wrong: None.” This fixes
issue 164.
• Static files necessary for HTML reports are found in system-installed places, to ease OS-level packaging of
coverage.py. Closes issue 259.
• Sourcefileswithencodingdeclarations,butablankfirstline,werenotdecodedproperly. Nowtheyare. Thanks,
Roger Hu.
• The source kit now includes the__main__.py file in the root coverage directory, fixing issue 255.
6.15. Change history for coverage.py 113

Coverage.py, Release 7.2.2
6.15.89 Version 3.6 — 2013-01-05
• Added a page to the docs about troublesome situations, closing issue 226, and added some info to the TODO
file, closing issue 227.
6.15.90 Version 3.6b3 — 2012-12-29
• Beta 2 broke the nose plugin. It’s fixed again, closing issue 224.
6.15.91 Version 3.6b2 — 2012-12-23
• Coverage.py runs on Python 2.3 and 2.4 again. It was broken in 3.6b1.
• The C extension is optionally compiled using a different more widely-used technique, taking another stab at
fixing issue 80 once and for all.
• Combining data files would create entries for phantom files if used withsource and path aliases. It no longer
does.
• debug sys now shows the configuration file path that was read.
• Ifanoddly-behavedpackageclaimsthatcodecamefromanempty-stringfilename,coverage.pynolongerasso-
ciates it with the directory name, fixing issue 221.
6.15.92 Version 3.6b1 — 2012-11-28
• Wildcards in include= and omit= arguments were not handled properly in reporting functions, though they
were when running. Now they are handled uniformly, closing issue 143 and issue 163.NOTE: it is possible
that your configurations may now be incorrect. If you useinclude or omit during reporting, whether on the
commandline,throughtheAPI,orinaconfigurationfile,pleasecheckcarefullythatyouwerenotrelyingonthe
old broken behavior.
• The report, html, and xml commands now accept a--fail-under switch that indicates in the exit status
whether the coverage percentage was less than a particular value. Closes issue 139.
• The reporting functions coverage.report(), coverage.html_report(), and coverage.xml_report() now all return a
float, the total percentage covered measurement.
• TheHTMLreport’stitlecannowbesetintheconfigurationfile,withthe --titleswitchonthecommandline,
or via the API.
• Configuration files now support substitution of environment variables, using syntax like${WORD}. Closes issue
97.
• Embarrassingly, the[xml] output= setting in the .coveragerc file simply didn’t work. Now it does.
• TheXMLreportnowconsistentlyusesfilenamesforthefilenameattribute,ratherthansometimesusingmodule
names. Fixes issue 67. Thanks, Marcus Cobden.
• Coverage percentage metrics are now computed slightly differently under branch coverage. This means that
completely un-executed files will now correctly have 0% coverage, fixing issue 156. This also means that your
total coverage numbers will generally now be lower if you are measuring branch coverage.
• When installing, now in addition to creating a “coverage” command, two new aliases are also installed. A
“coverage2”or“coverage3”commandwillbecreated, dependingonwhetheryouareinstallinginPython2.xor
3.x. A “coverage-X.Y” command will also be created corresponding to your specific version of Python. Closes
issue 111.
114 Chapter 6. More information

Coverage.py, Release 7.2.2
• Thecoverage.pyinstallernolongertriestobootstrapsetuptoolsorDistribute. Youmusthaveoneoftheminstalled
first, as issue 202 recommended.
• The coverage.py kit now includes docs (closing issue 137) and tests.
• On Windows, files are now reported in their correct case, fixing issue 89 and issue 203.
• If a file is missing during reporting, the path shown in the error message is now correct, rather than an incorrect
path in the current directory. Fixes issue 60.
• Running an HTML report in Python 3 in the same directory as an old Python 2 HTML report would fail with a
UnicodeDecodeError. This issue (issue 193) is now fixed.
• Fixed yet another error trying to parse non-Python files as Python, this time an IndentationError, closing issue
82 for the fourth time...
• Ifcoverage xmlfails because there is no data to report, it used to create a zero-length XML file. Now it doesn’t,
fixing issue 210.
• Jython files now work with the--sourceoption, fixing issue 100.
• Running coverage.py under a debugger is unlikely to work, but it shouldn’t fail with “TypeError: ‘NoneType’
object is not iterable”. Fixes issue 201.
• On some Linux distributions, when installed with the OS package manager, coverage.py would report its own
code as part of the results. Now it won’t, fixing issue 214, though this will take some time to be repackaged by
the operating systems.
• Docstrings for the legacy singleton methods are more helpful. Thanks Marius Gedminas. Closes issue 205.
• The pydoc tool can now show documentation for the classcoverage.coverage. Closes issue 206.
• Added a page to the docs about contributing to coverage.py, closing issue 171.
• When coverage.py ended unsuccessfully, it may have reported odd errors like'NoneType' object has no
attribute 'isabs'. It no longer does, so kiss issue 153 goodbye.
6.15.93 Version 3.5.3 — 2012-09-29
• LinenumbersintheHTMLreportlineupbetterwiththesourcelines,fixingissue197,thanksMariusGedminas.
• When specifying a directory as the source= option, the directory itself no longer needs to have a__init__.py
file, though its sub-directories do, to be considered as source files.
• Files encoded as UTF-8 with a BOM are now properly handled, fixing issue 179. Thanks, Pablo Carballo.
• Fixed more cases of non-Python files being reported as Python source, and then not being able to parse them as
Python. Closes issue 82 (again). Thanks, Julian Berman.
• Fixed memory leaks under Python 3, thanks, Brett Cannon. Closes issue 147.
• Optimized .pyo files may not have been handled correctly, issue 195. Thanks, Marius Gedminas.
• Certain unusually named file paths could have been mangled during reporting, issue 194. Thanks, Marius Ged-
minas.
• Try to do a better job of the impossible task of detecting when we can’t build the C extension, fixing issue 183.
• Testing is now done with tox, thanks, Marc Abramowitz.
6.15. Change history for coverage.py 115

Coverage.py, Release 7.2.2
6.15.94 Version 3.5.2 — 2012-05-04
No changes since 3.5.2.b1
6.15.95 Version 3.5.2b1 — 2012-04-29
• The HTML report has slightly tweaked controls: the buttons at the top of the page are color-coded to the source
lines they affect.
• CustomCSScanbeappliedtotheHTMLreportbyspecifyingaCSSfileasthe extra_cssconfigurationvalue
in the[html] section.
• Sourcefileswith customencodingsdeclaredina commentatthetop arenowproperlyhandledduring reporting
on Python 2. Python 3 always handled them properly. This fixes issue 157.
• Backup files left behind by editors are no longer collected by the source= option, fixing issue 168.
• Ifafiledoesn’tparseproperlyasPython,wedon’treportitasanerrorifthefilenameseemslikemaybeitwasn’t
meant to be Python. This is a pragmatic fix for issue 82.
• The -mswitch oncoverage report , which includes missing line numbers in the summary report, can now be
specified asshow_missingin the config file. Closes issue 173.
• Whenrunningamodulewith coverage run -m <modulename> ,certaindetailsoftheexecutionenvironment
weren’t the same as forpython -m <modulename> . This had the unfortunate side-effect of makingcoverage
run -m unittest discover not work if you had tests in a directory named “test”. This fixes issue 155 and
issue 142.
• Now the exit status of your product code is properly used as the process status when runningpython -m
coverage run ... . Thanks, JT Olds.
• When installing into PyPy, we no longer attempt (and fail) to compile the C tracer function, closing issue 166.
6.15.96 Version 3.5.1 — 2011-09-23
• The [paths] feature unfortunately didn’t work in real world situations where you wanted to, you know, report
on the combined data. Now all paths stored in the combined file are canonicalized properly.
6.15.97 Version 3.5.1b1 — 2011-08-28
• When combining data files from parallel runs, you can now instruct coverage.py about which directories are
equivalentondifferentmachines. A [paths]sectionintheconfigurationfilelistspathsthataretobeconsidered
equivalent. Finishes issue 17.
• for-else constructs are understood better, and don’t cause erroneous partial branch warnings. Fixes issue 122.
• Branch coverage forwithstatements is improved, fixing issue 128.
• The number of partial branches reported on the HTML summary page was different than the number reported
on the individual file pages. This is now fixed.
• An explicit include directive to measure files in the Python installation wouldn’t work because of the standard
library exclusion. Now the include directive takes precedence, and the files will be measured. Fixes issue 138.
• TheHTMLreportnowhandlesUnicodecharactersinPythonsourcefilesproperly. Thisfixesissue124andissue
144. Thanks, Devin Jeanpierre.
116 Chapter 6. More information

Coverage.py, Release 7.2.2
• In order to help the core developers measure the test coverage of the standard library, Brandon Rhodes devised
an aggressive hack to trick Python into running some coverage.py code before anything else in the process. See
the coverage/fullcoverage directory if you are interested.
6.15.98 Version 3.5 — 2011-06-29
• The HTML report hotkeys now behave slightly differently when the current chunk isn’t visible at all: a chunk
on the screen will be selected, instead of the old behavior of jumping to the literal next chunk. The hotkeys now
work in Google Chrome. Thanks, Guido van Rossum.
6.15.99 Version 3.5b1 — 2011-06-05
• TheHTMLreportnowhashotkeys. Try n, s, m, x, b, p,and contheoverviewpagetochangethecolumnsorting.
On a file page,r, m, x, andp toggle the run, missing, excluded, and partial line markings. You can navigate the
highlighted sections of code by using thej and k keys for next and previous. The1 (one) key jumps to the first
highlighted section in the file, and0(zero) scrolls to the top of the file.
• The --omitand --includeswitchesnowinterprettheirvaluesmoreusefully. Ifthevaluestartswithawildcard
character, it is used as-is. If it does not, it is interpreted relative to the current directory. Closes issue 121.
• Partial branch warnings can now be pragma’d away. The configuration optionpartial_branches is a list
of regular expressions. Lines matching any of those expressions will never be marked as a partial branch. In
addition,there’sabuilt-inlistofregularexpressionsmarkingstatementswhichshouldneverbemarkedaspartial.
This list includeswhile True: , while 1: , if 1: , andif 0: .
• The coverage()constructoracceptssinglestringsforthe omit=and include=arguments,adaptingtoacom-
mon error in programmatic use.
• Modules can now be run directly usingcoverage run -m modulename , to mirror Python’s-m flag. Closes
issue 95, thanks, Brandon Rhodes.
• coverage run didn’t emulate Python accurately in one small detail: the current directory inserted intosys.
pathwas relative rather than absolute. This is now fixed.
• HTMLreportingisnowincremental: arecordiskeptofthedatathatproducedtheHTMLreports,andonlyfiles
whose data has changed will be generated. This should make most HTML reporting faster.
• Pathological code execution could disable the trace function behind our backs, leading to incorrect code mea-
surement. Now if this happens, coverage.py will issue a warning, at least alerting you to the problem. Closes
issue 93. Thanks to Marius Gedminas for the idea.
• The C-based trace function now behaves properly when saved and restored withsys.gettrace() and sys.
settrace(). This fixes issue 125 and issue 123. Thanks, Devin Jeanpierre.
• Source files are now opened with Python 3.2’stokenize.open() where possible, to get the best handling of
Python source files with encodings. Closes issue 107, thanks, Brett Cannon.
• Syntax errors in supposed Python files can now be ignored during reporting with the-i switch just like other
source errors. Closes issue 115.
• Installation from source now succeeds on machines without a C compiler, closing issue 80.
• Coverage.py can now be run directly from a working tree by specifying the directory name to python:python
coverage_py_working_dir run ... . Thanks, Brett Cannon.
• A little bit of Jython support:coverage runcan now measure Jython execution by adapting when $py.class files
are traced. Thanks, Adi Roiban. Jython still doesn’t provide the Python libraries needed to make coverage
reporting work, unfortunately.
6.15. Change history for coverage.py 117

Coverage.py, Release 7.2.2
• Internally, files are now closed explicitly, fixing issue 104. Thanks, Brett Cannon.
6.15.100 Version 3.4 — 2010-09-19
• The XML report is now sorted by package name, fixing issue 88.
• Programs that exited withsys.exit() with no argument weren’t handled properly, producing a coverage.py
stack trace. That is now fixed.
6.15.101 Version 3.4b2 — 2010-09-06
• Completelyun-executedfilescannowbeincludedincoverageresults,reportedas0%covered. Thisonlyhappens
if the –source option is specified, since coverage.py needs guidance about where to look for source files.
• The XML report output now properly includes a percentage for branch coverage, fixing issue 65 and issue 81.
• Coveragepercentagesarenowdisplayeduniformlyacrossreportingmethods. Previously,differentreportscould
round percentages differently. Also, percentages are only reported as 0% or 100% if they are truly 0 or 100, and
are rounded otherwise. Fixes issue 41 and issue 70.
• The precision of reported coverage percentages can be set with the[report] precision config file setting.
Completes issue 16.
• Threadsderivedfrom threading.Threadwithanoverridden runmethodwouldreportnocoverageforthe run
method. This is now fixed, closing issue 85.
6.15.102 Version 3.4b1 — 2010-08-21
• BACKWARDINCOMPATIBILITY:the --omitand --includeswitchesnowtakefilepatternsratherthanfile
prefixes, closing issue 34 and issue 36.
• BACKWARD INCOMPATIBILITY: theomit_prefixesargument is gone throughout coverage.py, replaced with
omit,alistoffilenamepatternssuitablefor fnmatch. Aparallelargument includecontrolswhatfilesareincluded.
• The run command now has a--source switch, a list of directories or module names. If provided, coverage.py
will only measure execution in those source files.
• Variouswarningsareprintedtostderrforproblemsencounteredduringdatameasurement: ifa --sourcemodule
has no Python source to measure, or is never encountered at all, or if no data is collected.
• The reporting commands (report, annotate, html, and xml) now have an--include switch to restrict reporting
to modules matching those file patterns, similar to the existing--omit switch. Thanks, Zooko.
• The run command now supports--include and --omit to control what modules it measures. This can speed
execution and reduce the amount of data during reporting. Thanks Zooko.
• Since coverage.py 3.1, using the Python trace function has been slower than it needs to be. A cache of tracing
decisions was broken, but has now been fixed.
• Python 2.7 and 3.2 have introduced new opcodes that are now supported.
• Python files with no statements, for example, empty__init__.py files, are now reported as having zero state-
ments instead of one. Fixes issue 1.
• Reportsnowhaveacolumnofmissedlinecountsratherthanexecutedlinecounts,sincedevelopersshouldfocus
onreducingthemissedlinestozero,ratherthanincreasingtheexecutedlinestovaryingtargets. Oncesuggested,
this seemed blindingly obvious.
118 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.105 Version 3.2 — 2009-12-05
• Added a--version option on the command line.
6.15.106 Version 3.2b4 — 2009-12-01
• Branch coverage improvements:
–The XML report now includes branch information.
• Click-to-sortHTMLreportcolumnsarenowpersistedinacookie. Viewingareportwillsortitfirstthewayyou
last had a coverage report sorted. Thanks, Chris Adams.
• On Python 3.x, setuptools has been replaced by Distribute.
6.15.107 Version 3.2b3 — 2009-11-23
• Fixed a memory leak in the C tracer that was introduced in 3.2b1.
• Branch coverage improvements:
–Branches to excluded code are ignored.
• The table of contents in the HTML report is now sortable: click the headers on any column. Thanks, Chris
Adams.
6.15.108 Version 3.2b2 — 2009-11-19
• Branch coverage improvements:
–Classes are no longer incorrectly marked as branches: issue 32.
–“except” clauses with types are no longer incorrectly marked as branches: issue 35.
• Fixed some problems syntax coloring sources with line continuations and source with tabs: issue 30 and issue
31.
• The –omit option now works much better than before, fixing issue 14 and issue 33. Thanks, Danek Duvall.
6.15.109 Version 3.2b1 — 2009-11-10
• Branch coverage!
• XML reporting has file paths that let Cobertura find the source code.
• The tracer code has changed, it’s a few percent faster.
• Some exceptions reported by the command line interface have been cleaned up so that tracebacks inside cover-
age.py aren’t shown. Fixes issue 23.
120 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.110 Version 3.1 — 2009-10-04
• Source code can now be read from eggs. Thanks, Ross Lawley. Fixes issue 25.
6.15.111 Version 3.1b1 — 2009-09-27
• Python 3.1 is now supported.
• Coverage.py has a new command line syntax with sub-commands. This expands the possibilities for adding
featuresandoptionsinthefuture. Theoldsyntaxisstillsupported. Try“coveragehelp”toseethenewcommands.
Thanks to Ben Finney for early help.
• Added an experimental “coverage xml” command for producing coverage reports in a Cobertura-compatible
XML format. Thanks, Bill Hart.
• Added the –timid option to enable a simpler slower trace function that works for DecoratorTools projects, in-
cluding TurboGears. Fixed issue 12 and issue 13.
• HTML reports show modules from other directories. Fixed issue 11.
• HTML reports now display syntax-colored Python source.
• Programs that change directory will still write .coverage files in the directory where execution started. Fixed
issue 24.
• Added a “coverage debug” command for getting diagnostic information about the coverage.py installation.
6.15.112 Version 3.0.1 — 2009-07-07
• Removed the recursion limit in the tracer function. Previously, code that ran more than 500 frames deep would
crash. Fixed issue 9.
• Fixedabizarreprobleminvolvingpyexpat,wherebylinesfollowingXMLparserinvocationscouldbeoverlooked.
Fixed issue 10.
• On Python 2.3, coverage.py could mis-measure code with exceptions being raised. This is now fixed.
• Thecoverage.pycodeitselfwillnownotbemeasuredbycoverage.py,andnocoverage.pymoduleswillbemen-
tioned in the nose –with-cover plug-in. Fixed issue 8.
• When running source files, coverage.py now opens them in universal newline mode just like Python does. This
lets it run Windows files on Mac, for example.
6.15.113 Version 3.0 — 2009-06-13
• Fixed the way the Python library was ignored. Too much code was being excluded the old way.
• Tabs are now properly converted in HTML reports. Previously indentation was lost. Fixed issue 6.
• Nested modules now get a proper flat_rootname. Thanks, Christian Heimes.
6.15. Change history for coverage.py 121

Coverage.py, Release 7.2.2
6.15.114 Version 3.0b3 — 2009-05-16
• Added parameters to coverage.__init__ for options that had been set on the coverage object itself.
• Added clear_exclude() and get_exclude_list() methods for programmatic manipulation of the exclude regexes.
• Added coverage.load() to read previously-saved data from the data file.
• Improvedthefindingofcodefiles. Forexample,.pycfilesthathavebeeninstalledaftercompilingarenowlocated
correctly. Thanks, Detlev Offenbach.
• When using the object API (that is, constructing a coverage() object), data is no longer saved automatically
on process exit. You can re-enable it with the auto_data=True parameter on the coverage() constructor. The
module-level interface still uses automatic saving.
6.15.115 Version 3.0b — 2009-04-30
HTML reporting, and continued refactoring.
• HTMLreportsandannotationofsourcefiles: usethenew-b(browser)switch. ThankstoGeorgeSongforcode,
inspiration and guidance.
• CodeinthePythonstandardlibraryisnotmeasuredbydefault. Ifyouneedtomeasurestandardlibrarycode,use
the -L command-line switch during execution, or the cover_pylib=True argument to the coverage() constructor.
• Sourceannotationintoadirectory(-a-d)behavesdifferently. Theannotatedfilesarenamedwiththeirhierarchy
flattenedsothatsame-namedfilesfromdifferentdirectoriesnolongercollide. Also,onlyfilesinthecurrenttree
are included.
• coverage.annotate_file is no longer available.
• Programs executed with -x now behave more as they should, for example, __file__ has the correct value.
• .coverage data files have a new pickle-based format designed for better extensibility.
• Removed the undocumented cache_file argument to coverage.usecache().
6.15.116 Version 3.0b1 — 2009-03-07
Major overhaul.
• Coverage.py is now a package rather than a module. Functionality has been split into classes.
• The trace function is implemented in C for speed. Coverage.py runs are now much faster. Thanks to David
Christian for productive micro-sprints and other encouragement.
• Executable lines are identified by reading the line number tables in the compiled code, removing a great deal of
complicated analysis code.
• Precisely which lines are considered executable has changed in some cases. Therefore, your coverage stats may
also change slightly.
• The singleton coverage object is only created if the module-level functions are used. This maintains the old
interface while allowing better programmatic use of coverage.py.
• The minimum supported Python version is 2.3.
122 Chapter 6. More information

Coverage.py, Release 7.2.2
6.15.117 Version 2.85 — 2008-09-14
• Add support for finding source files in eggs. Don’t check for morf’s being instances of ModuleType, instead use
duck typing so that pseudo-modules can participate. Thanks, Imri Goldberg.
• Useos.realpathaspartofthefixingoffilenamessothatsymlinkswon’tconfusethings. Thanks,PatrickMezard.
6.15.118 Version 2.80 — 2008-05-25
• Open files in rU mode to avoid line ending craziness. Thanks, Edward Loper.
6.15.119 Version 2.78 — 2007-09-30
• Don’ttrytopredictwhetherafileisPythonsourcebasedontheextension. Extension-lessfilesareoftenPythons
scripts. Instead, simply parse the file and catch the syntax errors. Hat tip to Ben Finney.
6.15.120 Version 2.77 — 2007-07-29
• Better packaging.
6.15.121 Version 2.76 — 2007-07-23
• Now Python 2.5 isreallyfully supported: the body of the new with statement is counted as executable.
6.15.122 Version 2.75 — 2007-07-22
• Python 2.5 now fully supported. The method of dealing with multi-line statements is now less sensitive to the
exactlinethatPythonreportsduringexecution. Passstatementsarehandledspeciallysothattheirdisappearance
during execution won’t throw off the measurement.
6.15.123 Version 2.7 — 2007-07-21
• “#pragma: nocover” is excluded by default.
• Properly ignore docstrings and other constant expressions that appear in the middle of a function, a problem
reported by Tim Leslie.
• coverage.erase() shouldn’t clobber the exclude regex. Change how parallel mode is invoked, and fix erase() so
that it erases the cache when called programmatically.
• In reports, ignore code executed from strings, since we can’t do anything useful with it anyway.
• Better file handling on Linux, thanks Guillaume Chazarain.
• Better shell support on Windows, thanks Noel O’Boyle.
• Python 2.2 support maintained, thanks Catherine Proulx.
• Minor changes to avoid lint warnings.
6.15. Change history for coverage.py 123

Coverage.py, Release 7.2.2
6.15.124 Version 2.6 — 2006-08-23
• Applied Joseph Tate’s patch for function decorators.
• Applied Sigve Tjora and Mark van der Wal’s fixes for argument handling.
• Applied Geoff Bache’s parallel mode patch.
• Refactorings to improve testability. Fixes to command-line logic for parallel mode and collect.
6.15.125 Version 2.5 — 2005-12-04
• Call threading.settrace so that all threads are measured. Thanks Martin Fuzzey.
• Add a file argument to report so that reports can be captured to a different destination.
• Coverage.py can now measure itself.
• Adapted Greg Rogers’ patch for using relative file names, and sorting and omitting files to report on.
6.15.126 Version 2.2 — 2004-12-31
• Allow for keyword arguments in the module global functions. Thanks, Allen.
6.15.127 Version 2.1 — 2004-12-14
• Return ‘analysis’ to its original behavior and add ‘analysis2’. Add a global for ‘annotate’, and factor it, adding
‘annotate_file’.
6.15.128 Version 2.0 — 2004-12-12
Significant code changes.
• Finding executable statements has been rewritten so that docstrings and other quirks of Python execution aren’t
mistakenly identified as missing lines.
• Lines can be excluded from consideration, even entire suites of lines.
• The file system cache of covered lines can be disabled programmatically.
• Modernized the code.
6.15.129 Earlier History
2001-12-04 GDR Created.
2001-12-06 GDR Added command-line interface and source code annotation.
2001-12-09 GDR Moved design and interface to separate documents.
2001-12-10 GDR Open cache file as binary on Windows. Allow simultaneous -e and -x, or -a and -r.
2001-12-12 GDR Added command-line help. Cache analysis so that it only needs to be done once when you specify
-a and -r.
2001-12-13 GDR Improved speed while recording. Portable between Python 1.5.2 and 2.1.1.
2002-01-03 GDR Module-level functions work correctly.
124 Chapter 6. More information

Coverage.py, Release 7.2.2
2002-01-07 GDR Update sys.path when running a file with the -x option, so that it matches the value the program
would get if it were run on its own.
6.16 Sleepy Snake
Coverage.py’s mascot is Sleepy Snake, drawn by Ben Batchelder. Ben’s art can be found on Instagram and at artof-
batch.com. Some details of Sleepy’s creation are on Ned’s blog.
6.16. Sleepy Snake 125

Coverage.py, Release 7.2.2
126 Chapter 6. More information

Coverage.py, Release 7.2.2
lines()(coverage.CoverageData method), 67
lines()(coverage.FileReporter method), 61
load() (coverage.Coverage method), 52
loads()(coverage.CoverageData method), 68
M
measured_contexts() (coverage.CoverageData
method), 68
measured_files() (coverage.CoverageData method),

missing_arc_description() (coverage.FileReporter
method), 63
module
coverage, 55
coverage.exceptions, 55
coverage.numbits, 72
coverage.plugin, 56
N
no_branch_lines() (coverage.FileReporter method),

num_in_numbits() (in module coverage.numbits), 72
numbits_any_intersection() (in module cover-
age.numbits), 72
numbits_intersection() (in module cover-
age.numbits), 72
numbits_to_nums() (in module coverage.numbits), 72
numbits_union()(in module coverage.numbits), 73
nums_to_numbits() (in module coverage.numbits), 73
P
process_startup() (in module coverage), 56
purge_files()(coverage.CoverageData method), 68
R
read() (coverage.CoverageData method), 68
register_sqlite_functions() (in module cover-
age.numbits), 73
relative_filename() (coverage.FileReporter
method), 61
report() (coverage.Coverage method), 52
S
save() (coverage.Coverage method), 53
set_context()(coverage.CoverageData method), 68
set_option()(coverage.Coverage method), 53
set_query_context() (coverage.CoverageData
method), 69
set_query_contexts() (coverage.CoverageData
method), 69
source() (coverage.FileReporter method), 61
source_filename() (coverage.FileTracer method), 60
source_token_lines() (coverage.FileReporter
method), 63
start() (coverage.Coverage method), 54
stop() (coverage.Coverage method), 54
switch_context() (coverage.Coverage method), 54
sys_info() (coverage.CoverageData class method), 69
sys_info() (coverage.CoveragePlugin method), 59
T
touch_file()(coverage.CoverageData method), 69
touch_files() (coverage.CoverageData method), 69
translate_arcs() (coverage.FileReporter method), 62
translate_lines() (coverage.FileReporter method),

U
update() (coverage.CoverageData method), 70
V
version_info(in module coverage), 55
W
write() (coverage.CoverageData method), 70
X
xml_report()(coverage.Coverage method), 54
130 Index