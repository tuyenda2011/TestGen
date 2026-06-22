# TÀI LIỆU CỐT LÕI (Rút gọn từ pytest_cov_official.pdf)

> **Tổng quan**: Giữ lại 40 trang, lọc bỏ 8 trang dư thừa (changelog, index, license...).

pytest-cov
Release 7.1.0
pytest-cov contributors
Apr 24, 2026

CONTENTS
1 Overview 3
1.1 Installation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.2 Usage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.3 Documentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.4 Coverage Data File . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.5 Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.6 Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.7 Acknowledgements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
2 Configuration 7
2.1 Caveats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
3 Reporting 9
4 Debuggers and PyCharm 11
5 Distributed testing (xdist) 13
5.1 “load” mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
5.2 “each” mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
6 Subprocess support 15
7 Contexts 17
8 Tox 19
9 Plugin coverage 21
10 Markers and fixtures 23
10.1 Markers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
10.2 Fixtures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
11 Changelog 25
11.1 7.1.0 (2026-03-21) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
11.2 7.0.0 (2025-09-09) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
11.3 6.3.0 (2025-09-06) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
11.4 6.2.1 (2025-06-12) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
11.5 6.2.0 (2025-06-11) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
11.6 6.1.1 (2025-04-05) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
11.7 6.1.0 (2025-04-01) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
11.8 6.0.0 (2024-10-29) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
i

pytest-cov, Release 7.1.0
Contents:

pytest-cov, Release 7.1.0

CHAPTER
ONE
OVERVIEW
docs
tests
package
Thispluginprovidescoveragefunctionalityasapytestplugin. Comparedtojustusing coverage run thisplugindoes
some extras:
• Automatic erasing and combination of .coverage files and default reporting.
• Support for detailed coverage contexts (add --cov-context=test to have the full test name including
parametrization as the context).
• Xdist support: you can use all of pytest-xdist’s features including remote interpreters and still get coverage.
• Consistent pytest behavior. If you runcoverage run -m pytest you will have slightly differentsys.path
(CWD will be in it, unlike when runningpytest).
Allfeaturesofferedbythecoveragepackageshouldwork,eitherthroughpytest-cov’scommandlineoptionsorthrough
coverage’s config file.
• Free software: MIT license
1.1 Installation
Install with pip:
pip install pytest -cov
For distributed testing support install pytest-xdist:
pip install pytest -xdist
1.1.1 Upgrading from pytest-cov 6.3
pytest-cov 6.3and older were using a.pth file to enable coverage measurements in subprocesses. This was removed
in pytest-cov 7- use coverage’s patch options to enable subprocess measurements.

pytest-cov, Release 7.1.0
1.1.2 Uninstalling
Uninstall with pip:
pip uninstall pytest -cov
Under certain scenarios a stray.pthfile may be left around in site-packages.
• pytest-cov 2.0 may leave a pytest-cov.pth if you installed without wheels (easy_install, setup.py
installetc).
• pytest-cov 1.8 or olderwill leave ainit_cov_core.pth.
1.2 Usage
pytest --cov=myproj tests /
Would produce a report like:
-------------------- coverage: ... ---------------------
Name Stmts Miss Cover
----------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 %
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %
1.3 Documentation
https://pytest-cov.readthedocs.io/en/latest/
1.4 Coverage Data File
The data file is erased at the beginning of testing to ensure clean data for each test run. If you need to combine the
coverageofseveraltestrunsyoucanusethe --cov-appendoptiontoappendthiscoveragedatatocoveragedatafrom
previous test runs.
The data file is left at the end of testing so that it is possible to use normal coverage tools to examine it.
1.5 Limitations
For distributed testing the workers must have the pytest-cov package installed. This is needed since the plugin must be
registered through setuptools for pytest to start the plugin on the worker.
1.6 Security
ToreportasecurityvulnerabilitypleaseusetheTideliftsecuritycontact. Tideliftwillcoordinatethefixanddisclosure.
4 Chapter 1. Overview

pytest-cov, Release 7.1.0
1.7 Acknowledgements
Whilst this plugin has been built fresh from the ground up it has been influenced by the work done on pytest-coverage
(Ross Lawley, James Mills, Holger Krekel) and nose-cover (Jason Pellerin) which are other coverage plugins.
Ned Batchelder for coverage and its ability to combine the coverage results of parallel runs.
Holger Krekel for pytest with its distributed testing support.
Jason Pellerin for nose.
Michael Foord for unittest2.
No doubt others have contributed to these tools as well.
1.7. Acknowledgements 5

pytest-cov, Release 7.1.0
6 Chapter 1. Overview

CHAPTER
TWO
CONFIGURATION
This plugin provides a clean minimal set of command line options that are added to pytest. For further control of
coverage use a coverage config file.
CLI options:
--cov [SOURCE]
Path or package name to measure during execution (multi-allowed). Use--cov= to not do any source filtering
and record everything.
--cov-reset
Reset cov sources accumulated in options so far.
--cov-report TYPE
Type of report to generate: term, term-missing, annotate, html, xml, json, markdown, markdown-append, lcov
(multi-allowed). term, term-missing may be followed by “:skip-covered”. annotate, html, xml, json, mark-
down,markdown-appendandlcovmaybefollowedby“:DEST”whereDESTspecifiestheoutputlocation. Use
--cov-report=to not generate any output.
--cov-config PATH
Config file for coverage. Default:.coveragerc
--no-cov-on-fail
Do not report coverage if test run fails. Default: False
--no-cov
Disable coverage report completely (useful for debuggers). Default: False
--cov-fail-under MIN
Fail if the total coverage is less than MIN.
--cov-append
Do not delete coverage but append to current. Default: False
--cov-branch
Enable branch coverage. Can also be specified in the coverage config file[run] section.
--cov-precision COV_PRECISION
Override the reporting precision. Can also be specified in the coverage config file[report] section.
--cov-context CONTEXT
Dynamic contexts to use. “test” for now.

pytest-cov, Release 7.1.0
/inf⌢-circleNote
Important Note
This plugin overrides theparallel option of coverage. Unless you also run coverage without pytest-cov it’s
pointless to set those options in your.coveragerc.
If you use the--cov=somethingoption (with a value) then coverage’ssourceoption will also get overridden. If
you have multiple sources it might be easier to set those in.coveragercand always use--cov(without a value)
instead of having a long command line with--cov=pkg1 --cov=pkg2 --cov=pkg3 ... .
If you use the--cov-branch option then coverage’sbranch option will also get overridden.
If you wish to always run pytest-cov with pytest, you can useaddopts under thepytest or tool:pytest section of
your setup.cfg, or thetool.pytest.ini_options section of yourpyproject.tomlfile.
For example, insetup.cfg:
[tool:pytest]
addopts = -- cov=<project-name> -- cov-report html
Or forpyproject.toml:
[tool.pytest.ini_options]
addopts = "--cov=<project-name> --cov-report html"
/inf⌢-circleNote
Important Note
The --cov option has an optional argument. If it’s your last option in addopts it might eat the next CLI argument,
make sure to force it to take a blank value if that’s what you wanted by using--cov= (essentially the same as
--cov="").
2.1 Caveats
An unfortunate consequence of coverage.py’s history is that.coveragerc is a magic name: it’s the default file but it
also means “try to also lookup coverage configuration intox.inior setup.cfg”.
In practical terms this means that if you have multiple configuration files around (tox.ini, pyproject.toml or
setup.cfg) you might need to use--cov-config to make coverage use the correct configuration file.
Also,ifyouchangetheworkingdirectoryandalsousesubprocessesinatestyoumightalsoneedtouse --cov-config
to make pytest-cov use the expected configuration file in the subprocess.
8 Chapter 2. Configuration

CHAPTER
THREE
REPORTING
It is possible to generate any combination of the reports for a single test run.
The available reports are terminal (with or without missing line numbers shown), HTML, XML, JSON, Markdown
(either in ‘write’ or ‘append’ mode to file), LCOV and annotated source code.
The default is terminal report without line numbers:
pytest --cov=myproj tests /
-------------------- coverage: platform linux2, python 2.6.4 -final-0 --------------------
˓→-
Name Stmts Miss Cover
----------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 %
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %
The terminal report with line numbers:
pytest --cov-report=term-missing --cov=myproj tests /
-------------------- coverage: platform linux2, python 2.6.4 -final-0 --------------------
˓→-
Name Stmts Miss Cover Missing
--------------------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 % 24-26, 99, 149, 233 -236, 297 -298, 369 -370
myproj/feature4286 94 7 92 % 183-188, 197
--------------------------------------------------
TOTAL 353 20 94 %
The terminal report with skip covered:
pytest --cov-report term:skip -covered --cov=myproj tests /
-------------------- coverage: platform linux2, python 2.6.4 -final-0 --------------------
˓→-
Name Stmts Miss Cover
----------------------------------------
myproj/myproj 257 13 94 %

pytest-cov, Release 7.1.0
(continued from previous page)
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %
1 files skipped due to complete coverage .
You can useskip-coveredwith term-missing as well. e.g.--cov-report term-missing:skip-covered
Ifanyreportingoptionsareusedthenthedefault( --cov-report=term)isnotaddedautomatically. Forexamplethis
would not show any terminal output:
pytest --cov-report html
--cov-report xml
--cov-report json
--cov-report markdown
--cov-report markdown-append:cov-append.md
--cov-report lcov
--cov-report annotate
--cov=myproj tests/
You can specify output paths for reports. The output location for the XML, JSON, Markdown and LCOV report is a
file. Where as the output location for the HTML and annotated source code reports are directories:
pytest --cov-report html:cov_html
--cov-report xml:cov.xml
--cov-report json:cov.json
--cov-report markdown:cov.md
--cov-report markdown-append:cov-append.md
--cov-report lcov:cov.info
--cov-report annotate:cov_annotate
--cov=myproj tests/
Example for GitHub Actions withmarkdown-append:
pytest --cov-report markdown-append:$GITHUB_STEP_SUMMARY
--cov=myproj tests/
To disable the defaultterm report provide an empty report:
pytest --cov-report = --cov=myproj tests/
This mode can be especially useful on continuous integration servers, where a coverage file is needed for subsequent
processing,butnolocalreportneedstobeviewed. Forexample,testsrunonGitHubActionscouldproducea.coverage
file for use with Coveralls.
10 Chapter 3. Reporting

CHAPTER
FOUR
DEBUGGERS AND PYCHARM
(or other IDEs)
When it comes to TDD one obviously would like to debug tests. Debuggers in Python use mostly the sys.settrace
functiontogainaccesstocontext. Coverageusesthesametechniquetogetaccesstothelinesexecuted. Coveragedoes
not playwell withother tracerssimultaneously running. Thismanifests itselfin behaviourthat PyCharm mightnot hit
a breakpoint no matter what the user does, or encountering an error like this:
PYDEV DEBUGGER WARNING:
sys.settrace() should not be used when the debugger is being used .
This may cause the debugger to stop working correctly .
Sinceitiscommonpracticetohavecoverageconfigurationinthepytest.inifileandpytestdoesnotsupportremoveopts
or similar the–no-covflag can disable coverage completely.
At the reporting part a warning message will show on screen:
Coverage disabled via --no-cov switch!

pytest-cov, Release 7.1.0
12 Chapter 4. Debuggers and PyCharm

CHAPTER
FIVE
DISTRIBUTED TESTING (XDIST)
5.1 “load” mode
Distributedtestingwithdistmodesetto“load”willreportonthecombinedcoverageofallworkers. Theworkersmay
bespreadoutoveranynumberofhostsandeachworkermaybelocatedanywhereonthefilesystem. Eachworkerwill
have its subprocesses measured.
Running distributed testing with dist mode set to load:
pytest --cov=myproj -n 2 tests /
Shows a terminal report:
-------------------- coverage: platform linux2, python 2.6.4 -final-0 --------------------
˓→-
Name Stmts Miss Cover
----------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 %
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %
Again but spread over different hosts and different directories:
pytest --cov=myproj --dist load
--tx ssh =memedough@host1//chdir=testenv1
--tx ssh =memedough@host2//chdir=/tmp/testenv2//python=/tmp/env1/bin/python
--rsyncdir myproj --rsyncdir tests --rsync examples
tests/
Shows a terminal report:
-------------------- coverage: platform linux2, python 2.6.4 -final-0 --------------------
˓→-
Name Stmts Miss Cover
----------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 %
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %

pytest-cov, Release 7.1.0
5.2 “each” mode
Distributed testing with dist mode set to each will report on the combined coverage of all workers. Since each worker
is running all tests this allows generating a combined coverage report for multiple environments.
Running distributed testing with dist mode set to each:
pytest --cov=myproj --dist each
--tx popen //chdir=/tmp/testenv3//python=/usr/local/python27/bin/python
--tx ssh =memedough@host2//chdir=/tmp/testenv4//python=/tmp/env2/bin/python
--rsyncdir myproj --rsyncdir tests --rsync examples
tests/
Shows a terminal report:
---------------------------------------- coverage ---------------------------------------
˓→-
platform linux2, python 2.6.5 -final-0
platform linux2, python 2.7.0 -final-0
Name Stmts Miss Cover
----------------------------------------
myproj/__init__ 2 0 100 %
myproj/myproj 257 13 94 %
myproj/feature4286 94 7 92 %
----------------------------------------
TOTAL 353 20 94 %
14 Chapter 5. Distributed testing (xdist)

CHAPTER
SIX
SUBPROCESS SUPPORT
Subprocess support was removed in pytest-cov 7.0 due to various complexities resulting from coverage’s own subpro-
cess support. To migrate you should change your coverage config to have at least this:
[run]
patch = subprocess
Or if you use pyproject.toml:
[tool.coverage.run]
patch = ["subprocess"]
Note that if you enable the subprocess patch thenparallel = true is automatically set.
If it still doesn’t produce the same coverage as before you may need to enable more patches, see the coverage config
and subprocess documentation.

pytest-cov, Release 7.1.0
16 Chapter 6. Subprocess support

CHAPTER
SEVEN
CONTEXTS
Coverage.py 5.0 can record separate coverage data for different contexts during one run of a test suite. Pytest-cov can
use this feature to record coverage data for each test individually, with the--cov-context=testoption.
Thecontextnamerecordedinthecoverage.pydatabaseisthepytesttestid,andthephaseofexecution,oneof“setup”,
“run”, or “teardown”. These two are separated with a pipe symbol. You might see contexts like:
test_functions.py::test_addition|run
test_fancy.py::test_parametrized[1-101]|setup
test_oldschool.py::RegressionTests::test_error|run
Note that parameterized tests include the values of the parameters in the test id, and each set of parameter values is
recorded as a separate test.
To view contexts when using--cov-report=html, add this to your.coveragerc:
[html]
show_contexts = True
TheHTMLreportwillincludeanannotationoneachcoveredline, indicatingthenumberofcontextsthatexecutedthe
line. Clicking the annotation displays a list of the contexts.

pytest-cov, Release 7.1.0
18 Chapter 7. Contexts

CHAPTER
EIGHT
TOX
When using tox you can have ultra-compact configuration - you can have all of it intox.ini:
[tox]
envlist = ...
[tool:pytest]
...
[coverage:paths]
...
[coverage:run]
...
[coverage:report]
..
[testenv]
commands = ...
Anusualproblemusershaveisthatpytest-covwillerasethepreviouscoveragedatabydefault,thusifyouruntoxwith
multiple environments you’ll get incomplete coverage at the end.
Topreventthisproblemyouneedtouse --cov-append. It’sstillrecommendedtocleanthepreviouscoveragedatato
have consistent output. Atox.inilike this should be enough for sequential runs:
[tox]
envlist = clean,py27,py36,...
[testenv]
commands = pytest --cov --cov-append --cov-report=term-missing ...
deps =
pytest
pytest-cov
[testenv:clean]
deps = coverage
skip_install = true
commands = coverage erase
For parallel runs we need to set some dependencies and have an extra report env like so:

pytest-cov, Release 7.1.0
[tox]
envlist = clean,py27,py36,report
[testenv]
commands = pytest --cov --cov-append --cov-report=term-missing
deps =
pytest
pytest-cov
depends =
{py27,py36}: clean
report: py27,py36
[testenv:report]
deps = coverage
skip_install = true
commands =
coverage report
coverage html
[testenv:clean]
deps = coverage
skip_install = true
commands = coverage erase
Dependingonyourprojectlayoutyoumightneedextraconfiguration,seetheworkingexamplesathttps://github.com/
pytest-dev/pytest-cov/tree/master/examples for two common layouts.
20 Chapter 8. Tox

CHAPTER
NINE
PLUGIN COVERAGE
Getting coverage on pytest plugins is a very particular situation. Because of how pytest implements plugins (using se-
tuptoolsentrypoints)itdoesn’tallowcontrollingtheorderinwhichthepluginsload. Seepytest/issues/935fortechnical
details.
Currently there is no way to measure your pytest plugin if you use pytest-cov. You should change your test invo-
cations to usecoverage run -m pytest ... instead.

pytest-cov, Release 7.1.0
22 Chapter 9. Plugin coverage

CHAPTER
TEN
MARKERS AND FIXTURES
There are some builtin markers and fixtures inpytest-cov.
10.1 Markers
10.1.1 no_cover
Eg:
@pytest.mark.no_cover
def test_foobar ():
# do some stuff that needs coverage disabled
/exclamati⌢n-triangleWarning
Caveat
Note that subprocess coverage will also be disabled.
10.2 Fixtures
10.2.1 no_cover
Eg:
def test_foobar (no_cover):
# same as the marker ...
10.2.2 cov
For reasons that no one can remember there is acov fixture that provides access to the underlying Coverage instance.
Somesaythisisadisguisedfoot-gunandshouldberemoved,andsomethinkmysteriesmakelifemoreinterestingand
it should be left alone.

pytest-cov, Release 7.1.0
24 Chapter 10. Markers and fixtures

pytest-cov, Release 7.1.0
11.3 6.3.0 (2025-09-06)
• Added support for markdown reports. Contributed by Marcos Boger in #712 and #714.
• Fixed some formatting issues in docs. Anonymous contribution in #706.
11.4 6.2.1 (2025-06-12)
• Added a version requirement for pytest’s pluggy dependency (1.2.0, released 2023-06-21) that has the required
new-style hookwrapper API.
• Removed deprecated license classifier (packaging).
• Disabled coverage warnings in two more situations where they have no value:
–“module-not-measured” in workers
–“already-imported” in subprocesses
11.5 6.2.0 (2025-06-11)
• The plugin now adds 3 rules in the filter warnings configuration to prevent common coverage warnings being
raised as obscure errors:
default:unclosed database in < sqlite3.Connection object at: ResourceWarning
once::PytestCovWarning
once::CoverageWarning
This fixes most of the bad interactions that are occurring on pytest 8.4 withfilterwarnings=error.
The plugin will check if there already matching rules for the 3 categories ( ResourceWarning,
PytestCovWarning, CoverageWarning) and message (unclosed database in <sqlite3.Connection
object at ) before adding the filters.
Thismeansyoucanhavethisinyourpytestconfigurationforcompleteoblivion(notrecommended,ifthatisnot
clear):
filterwarnings = [
"error",
"ignore:unclosed database in <sqlite3.Connection object at:ResourceWarning",
"ignore::PytestCovWarning",
"ignore::CoverageWarning",
]
11.6 6.1.1 (2025-04-05)
• Fixed breakage that occurs when--cov-contextand theno_covermarker are used together.
11.7 6.1.0 (2025-04-01)
• Change terminal output to use full width lines for the coverage header. Contributed by Tsvika Shapira in #678.
• Removed unnecessary CovFailUnderWarning. Fixes #675.
• Fixed the term report not using the precision specified via--cov-precision.
26 Chapter 11. Changelog

pytest-cov, Release 7.1.0
11.8 6.0.0 (2024-10-29)
• Updated various documentation inaccuracies, especially on subprocess handling.
• Changed fail under checks to use the precision set in the coverage configuration. Now it will perform the check
just likecoverage report would.
• Added a--cov-precisioncli option that can override the value set in your coverage configuration.
• Dropped support for now EOL Python 3.8.
11.9 5.0.0 (2024-03-24)
• Removed support for xdist rsync (now deprecated). Contributed by Matthias Reichenbach in #623.
• Switched docs theme to Furo.
• VariouslegacyPythoncleanupandCIimprovements. ContributedbyChristianClaussandHugovanKemenade
in #630, #631, #632 and #633.
• Added apyproject.toml example in the docs. Contributed by Dawn James in #626.
• Modernized project’s pre-commit hooks to use ruff. Initial POC contributed by Christian Clauss in #584.
• Dropped support for Python 3.7.
11.10 4.1.0 (2023-05-24)
• Updated CI with new Pythons and dependencies.
• Removed rsyncdir support. This makes pytest-cov compatible with xdist 3.0. Contributed by Sorin Sbarnea in
#558.
• Optimized summary generation to not be performed if no reporting is active (for example, when
--cov-report='' is used without--cov-fail-under). Contributed by Jonathan Stewmon in #589.
• Added support for JSON reporting. Contributed by Matthew Gamble in #582.
• Refactored code to use f-strings. Contributed by Mark Mayo in #572.
• Fixed a skip in the test suite for some old xdist. Contributed by a bunch of people in #565.
• Dropped support for Python 3.6.
11.11 4.0.0 (2022-09-28)
Note that this release drops support for multiprocessing.
• –cov-fail-underno longer causespytest –collect-onlyto fail Contributed by Zac Hatfield-Dodds in #511.
• Dropped support for multiprocessing (mostly because issue 82408). This feature was mostly working but very
broken in certain scenarios and made the test suite very flaky and slow.
There is builtin multiprocessing support in coverage and you can migrate to that. All you need is this in your
.coveragerc:
[run]
concurrency = multiprocessing
parallel = true
sigterm = true
11.8. 6.0.0 (2024-10-29) 27

pytest-cov, Release 7.1.0
• Fixed deprecation insetup.py by trying to import setuptools before distutils. Contributed by Ben Greiner in
#545.
• Removed undesirable new lines that were displayed while reporting was disabled. Contributed by Delgan in
#540.
• Documentation fixes. Contributed by Andre Brisco in #543 and Colin O’Dell in #525.
• Added support for LCOV output format via–cov-report=lcov. Only works with coverage 6.3+. Contributed by
Christian Fetzer in #536.
• Modernized pytest hook implementation. Contributed by Bruno Oliveira in #549 and Ronny Pfannschmidt in
#550.
11.12 3.0.0 (2021-10-04)
Note that this release drops support for Python 2.7 and Python 3.5.
• Added support for Python 3.10 and updated various test dependencies. Contributed by Hugo van Kemenade in
#500.
• Switched from Travis CI to GitHub Actions. Contributed by Hugo van Kemenade in #494 and #495.
• Add a--cov-reset CLI option. Contributed by Danilo Šegan in #459.
• Improved validation of--cov-fail-under CLI option. Contributed by ... Ronny Pfannschmidt’s desire for
skark in #480.
• Dropped Python 2.7 support. Contributed by Thomas Grainger in #488.
• Updated trove classifiers. Contributed by Michał Bielawski in #481.
• Reverted change fortoml requirement. Contributed by Thomas Grainger in #477.
11.13 2.12.1 (2021-06-01)
• Changed thetoml requirement to be always be directly required (instead of being required through a coverage
extra). This fixes issues with pip-compile (pip-tools#1300). Contributed by Sorin Sbarnea in #472.
• Documented show_contexts. Contributed by Brian Rutledge in #473.
11.14 2.12.0 (2021-05-14)
• Added coverage’stoml extra to install requirements in setup.py. Contributed by Christian Riedel in #410.
• Fixed pytest_cov.__version__ to have the right value (string with version instead of a string including
__version__ = ).
• Fixed license classifier insetup.py. Contributed by Chris Sreesangkom in #467.
• Fixedcommits sincebadge. Contributed by Terence Honles in #470.
11.15 2.11.1 (2021-01-20)
• Fixed support for newer setuptools (v42+). Contributed by Michał Górny in #451.
28 Chapter 11. Changelog

pytest-cov, Release 7.1.0
11.16 2.11.0 (2021-01-18)
• Bumpedminimumcoveragerequirementto5.2.1. Thispreventsreportingissues. ContributedbyMateusBerardo
de Souza Terra in #433.
• Improvedsampleprojects(fromtheexamplesdirectory)tosupportrunning tox-epyXY .Nowtheexampleconfig-
ures a suffixed coverage data file, and that makes the cleanup environment unnecessary. Contributed by Ganden
Schaffner in #435.
• Removed the emptyconsole_scriptsentrypoint that confused some Gentoo build script. I didn’t ask why it was
so broken cause I didn’t want to ruin my day. Contributed by Michał Górny in #434.
• Fixed the missing coverage context when using subprocesses. Contributed by Bernát Gábor in #443.
• Updated the config section in the docs. Contributed by Pamela McA’Nulty in #429.
• Migrated CI to travis-ci.com (from .org).
11.17 2.10.1 (2020-08-14)
• Support for pytest-xdist 2.0, which breaks compatibility withpytest-xdist before 1.22.3 (from 2017).
Contributed by Zac Hatfield-Dodds in #412.
• Fixed theLocalPath has no attribute startswith failure that occurred when using thepytester plu-
gin in inline mode.
11.18 2.10.0 (2020-06-12)
• Improved the--no-cov warning. Now it’s only shown if--no-cov is present before--cov.
• Removed legacy pytest support. Changedsetup.py so thatpytest>=4.6 is required.
11.19 2.9.0 (2020-05-22)
• Fixed RemovedInPytest4Warningwhen using Pytest 3.10. Contributed by Michael Manganiello in #354.
• Madepyteststartupfasterwhenpluginnotactivebylazy-importing. ContributedbyAndersHovmöllerin#339.
• Various CI improvements. Contributed by Daniel Hahler in #363 and #364.
• Various Python support updates (drop EOL 3.4, test against 3.8 final). Contributed by Hugo van Kemenade in
#336 and #367.
• Changed --cov-append to always enabledata_suffix (a coverage setting). Contributed by Harm Geerts in
#387.
• Changed --cov-appendto handle loading previous data better (fixes various path aliasing issues).
• Various other testing improvements, github issue templates, example updates.
• Fixedinternalfailuresthatarecausedbyteststhatchangethecurrentworkingdirectorybyensuringaconsistent
working directory when coverage is called. See #306 and coveragepy#881
11.20 2.8.1 (2019-10-05)
• Fixed#348-regressionwhenonlycertainreports(htmlorxml)areusedthen --cov-fail-underalwaysfails.
11.16. 2.11.0 (2021-01-18) 29

pytest-cov, Release 7.1.0
11.21 2.8.0 (2019-10-04)
• Fixed RecursionErrorthat can occur when using cleanup_on_signal or cleanup_on_sigterm. See: #294. The
2.7.x releases of pytest-cov should be considered broken regarding aforementioned cleanup API.
• Added compatibility with future xdist release that deprecates some internals (match pytest-xdist master/worker
terminology). Contributed by Thomas Grainger in #321
• Fixedbreakagethatoccurswhenmultiplereportingoptionsareused. ContributedbyThomasGraingerin#338.
• Changed internals to use a stub instead ofos.devnull. Contributed by Thomas Grainger in #332.
• Added support for Coverage 5.0. Contributed by Ned Batchelder in #319.
• Added support for float values in--cov-fail-under. Contributed by Martín Gaitán in #311.
• Variousdocumentationfixes. ContributedbyJuanjoBazán,AndrewMurrayandAlbertTugushevin#298,#299
and #307.
• Various testing improvements. Contributed by Ned Batchelder, Daniel Hahler, Ionel Cristian Măries, and Hugo
van Kemenade in #313, #314, #315, #316, #325, #326, #334 and #335.
• Added the--cov-context CLI options that enables coverage contexts. Only works with coverage 5.0+. Con-
tributed by Ned Batchelder in #345.
11.22 2.7.1 (2019-05-03)
• Fixed source distribution manifest so that garbage ain’t included in the tarball.
11.23 2.7.0 (2019-05-03)
• Fixed AttributeError: 'NoneType' object has no attribute 'configure_node' error when
--no-covis used. Contributed by Alexander Shadchin in #263.
• Various testing and CI improvements. Contributed by Daniel Hahler in #255, #266, #272, #271 and #269.
• Improved pytest_cov.embed.cleanup_on_sigterm to be reentrant (signal deliveries while signal handling
is running won’t break stuff).
• Added pytest_cov.embed.cleanup_on_signalfor customized cleanup.
• Improved cleanup code and fixed various issues with leftover data files. All contributed in #265 or #262.
• Improved examples. Now there are two examples for the common project layouts, complete with working cov-
erage configuration. The examples have CI testing. Contributed in #267.
• Improved help text for CLI options.
11.24 2.6.1 (2019-01-07)
• Added support for Pytest 4.1. Contributed by Daniel Hahler and in #253 and #230.
• Various test and docs fixes. Contributed by Daniel Hahler in #224 and #223.
• Fixed the “Module already imported” issue (#211). Contributed by Daniel Hahler in #228.
30 Chapter 11. Changelog

pytest-cov, Release 7.1.0
11.25 2.6.0 (2018-09-03)
• Dropped support for Python 3 < 3.4, Pytest < 3.5 and Coverage < 4.4.
• Fixed some documentation formatting. Contributed by Jean Jordaan and Julian.
• Added an example withaddoptsin documentation. Contributed by Samuel Giffard in #195.
• Fixed TypeError: 'NoneType' object is not iterable in certain xdist configurations. Contributed
by Jeremy Bowman in #213.
• Added ano_cover marker and fixture. Fixes #78.
• Fixed brokenno_cover check when running doctests. Contributed by Terence Honles in #200.
• Fixed various issues with path normalization in reports (when combining coverage data from parallel mode).
Fixes #130. Contributed by Ryan Hiebert & Ionel Cristian Măries, in #178.
• Report generation failures don’t raise exceptions anymore. A warning will be logged instead. Fixes #161.
• Fixed multiprocessing issue on Windows (empty env vars are not passed). Fixes #165.
11.26 2.5.1 (2017-05-11)
• Fixed xdist breakage (regression in2.5.0). Fixes #157.
• Allow setting customdata_file name in .coveragerc. Fixes #145. Contributed by Jannis Leidel & Ionel
Cristian Măries, in #156.
11.27 2.5.0 (2017-05-09)
• Always show a summary when--cov-fail-under is used. Contributed by Francis Niu in PR#141.
• Added --cov-branchoption. Fixes #85.
• Improve exception handling in subprocess setup. Fixes #144.
• Fixed handling when--cov is used multiple times. Fixes #151.
11.28 2.4.0 (2016-10-10)
• Added a “disarm” option:--no-cov. It will disable coverage measurements. Contributed by Zoltan Kozma in
PR#135.
WARNING:Donotputthisinyourconfigurationfiles,it’smeanttobeanone-offforsituationswhereyou
want to disable coverage from command line.
• Fixed broken exception handling on.pthfile. See #136.
11.29 2.3.1 (2016-08-07)
• Fixed regression causing spurious errors when xdist was used. See #124.
• Fixed DeprecationWarning about incorrectaddoptionuse. Contributed by Florian Bruhin in PR#127.
• Fixed deprecated use of funcarg fixture API. Contributed by Daniel Hahler in PR#125.
11.25. 2.6.0 (2018-09-03) 31

pytest-cov, Release 7.1.0
11.30 2.3.0 (2016-07-05)
• Add support for specifying output location for html, xml, and annotate report. Contributed by Patrick Lannigan
in PR#113.
• Fix bug hiding test failure when cov-fail-under failed.
• Forcoverage>=4.0,matchthedefaultbehaviourof coveragereport anderrorifcoveragefailstofindthesource
instead of just printing a warning. Contributed by David Szotten in PR#116.
• Fixed bug occurred when bare--cov parameter was used with xdist. Contributed by Michael Elovskikh in
PR#120.
• Addsupportfor skip_coveredandadded --cov-report=term-skip-coveredcommandlineoptions. Con-
tributed by Saurabh Kumar in PR#115.
11.31 2.2.1 (2016-01-30)
• Fixed incorrect merging of coverage data when xdist was used and coverage was>= 4.0 .
11.32 2.2.0 (2015-10-04)
• Added support for changing working directory in tests. Previously changing working directory would disable
coverage measurements in suprocesses.
• Fixed broken handling for--cov-report=annotate.
11.33 2.1.0 (2015-08-23)
• Added support forcoverage 4.0b2.
• Added the--cov-appendcommand line options. Contributed by Christian Ledermann in PR#80.
11.34 2.0.0 (2015-07-28)
• Added --cov-fail-under, akin to the newfail_under option incoverage-4.0(automatically activated if
there’s a[report] fail_under = ... in .coveragerc).
• Changed --cov-report=term to automatically upgrade to--cov-report=term-missing if there’s[run]
show_missing = True in .coveragerc.
• Changed --cov so it can be used with no path argument (in which case the source settings from.coveragerc
will be used instead).
• Fixed.pthinstallation to work in all cases (install, easy_install, wheels, develop etc).
• Fixed.pthuninstallation to work for wheel installs.
• Support for coverage 4.0.
• Data file suffixing changed to use coverage’sdata_suffix=True option (instead of the custom suffixing).
• Avoid warning about missing coverage data (just likecoverage.control.process_startup).
• Fixeda racecondition whenrunningwith xdist(allthe workerstried tocombinethe files). It’s possiblethat this
issue is not present inpytest-cov 1.8.X.
32 Chapter 11. Changelog

pytest-cov, Release 7.1.0
11.35 1.8.2 (2014-11-06)
• N/A
11.35. 1.8.2 (2014-11-06) 33

pytest-cov, Release 7.1.0
• Alexander Shadchin - https://github.com/shadchin
• Thomas Grainger - https://graingert.co.uk
• Juanjo Bazán - https://github.com/xuanxu
• Andrew Murray - https://github.com/radarhere
• Ned Batchelder - https://nedbatchelder.com/
• Albert Tugushev - https://github.com/atugushev
• Martín Gaitán - https://github.com/mgaitan
• Hugo van Kemenade - https://github.com/hugovk
• Michael Manganiello - https://github.com/adamantike
• Anders Hovmöller - https://github.com/boxed
• Zac Hatfield-Dodds - https://zhd.dev
• Mateus Berardo de Souza Terra - https://github.com/MatTerra
• Ganden Schaffner - https://github.com/gschaffner
• Michał Górny - https://github.com/mgorny
• Bernát Gábor - https://github.com/gaborbernat
• Pamela McA’Nulty - https://github.com/PamelaM
• Christian Riedel - https://github.com/Cielquan
• Chris Sreesangkom - https://github.com/csreesan
• Sorin Sbarnea - https://github.com/ssbarnea
• Brian Rutledge - https://github.com/bhrutledge
• Danilo Šegan - https://github.com/dsegan
• Michał Bielawski - https://github.com/D3X
• Zac Hatfield-Dodds - https://github.com/Zac-HD
• Ben Greiner - https://github.com/bnavigator
• Delgan - https://github.com/Delgan
• Andre Brisco - https://github.com/abrisco
• Colin O’Dell - https://github.com/colinodell
• Ronny Pfannschmidt - https://github.com/RonnyPfannschmidt
• Christian Fetzer - https://github.com/fetzerch
• Jonathan Stewmon - https://github.com/jstewmon
• Matthew Gamble - https://github.com/mwgamble
• Christian Clauss - https://github.com/cclauss
• Dawn James - https://github.com/dawngerpony
• Tsvika Shapira - https://github.com/tsvikas
• Marcos Boger - https://github.com/marcosboger
• Ofek Lev - https://github.com/ofek
36 Chapter 12. Authors

pytest-cov, Release 7.1.0
• Art Pelling - https://github.com/artpelling
• Markéta Machová - https://github.com/MeggyCal

pytest-cov, Release 7.1.0
38 Chapter 12. Authors

pytest-cov, Release 7.1.0
40 Chapter 13. Releasing

pytest-cov, Release 7.1.0
Now you can make your changes locally.
4. When you’re done making changes run all the checks and docs builder with one command:
tox
5. Commit your changes and push your branch to GitHub:
git add .
git commit -m "Your detailed description of your changes."
git push origin name -of-your-bugfix-or-feature
6. Submit a pull request through the GitHub website.
14.4.1 Pull Request Guidelines
If you need some code review or feedback while you’re developing the code just make the pull request.
For merging, you should:
1. Include passing tests (runtox).
2. Update documentation when there’s new API, functionality etc.
3. Add a note toCHANGELOG.rst about the changes.
4. Add yourself toAUTHORS.rst.
14.4.2 Tips
To run a subset of tests:
tox -e envname -- pytest -k test_myfeature
To run all the test environments inparallel:
tox -p auto
42 Chapter 14. Contributing

pytest-cov, Release 7.1.0
44 Chapter 15. Indices and tables