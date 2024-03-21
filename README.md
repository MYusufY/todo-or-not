[![image.png](https://i.postimg.cc/W3HvnfNj/image.png)](https://postimg.cc/dkrpQ6ZS)

![PyPI - Version](https://img.shields.io/pypi/v/todo-or-not)
[![Coverage Status](https://coveralls.io/repos/github/Start-Out/todo-or-not/badge.svg?branch=dev/staging&kill_cache=1)](https://coveralls.io/github/Start-Out/todo-or-not?branch=dev/staging&kill_cache=1)
![PyPI - Downloads](https://img.shields.io/pypi/dm/todo-or-not)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/todo-or-not)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - License](https://img.shields.io/pypi/l/todo-or-not?color=purple)

> TODO or not to do, that is the question

TODO Or Not (todoon) is, in essence, a simple tool that checks your project for TODO's and FIXME's. You can also
integrate this tool into your GitHub workflow via actions, and automate generating issues from the discovered TODO's and
FIXME's.

[Get the GitHub App](https://github.com/apps/todo-or-not)

[Try it out! (see on PyPi)](https://pypi.org/project/todo-or-not/)

```bash
pip install todo-or-not
```

## Table of Contents

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Examples](#examples)
- [Usage](#usage)
   * [CLI: `todoignore-util`](#cli-todoignore-util)
      + [Usage](#usage-1)
      + [Examples](#examples-1)
   * [CLI: `todoon`](#cli-todoon)
      + [Usage](#usage-2)
         - [Arguments](#arguments)
         - [Options](#options)
         - [Feedback](#feedback)
   * [Examples](#examples-2)
   * [Environment Variables](#environment-variables)
   * [.todo-ignore](#todo-ignore)
   * [Issues](#issues)
- [Settings](#settings)
   * [Localization](#localization)

<!-- TOC end -->

## Examples

Check out [this example code](https://github.com/Start-Out/todo-or-not/blob/main/example.py) and
the [issues that it yielded](https://github.com/Start-Out/todo-or-not/issues?q=is%3Aissue+author%3Aapp%2Ftodo-or-not+label%3Aexample+)!

```py
##########################
# Example usage of todoon
##########################

def an_unfinished_function():
    # TODO Finish documenting todo-or-not
    print("Hello, I'm not quite done, there's more to do!")
    print("Look at all these things I have to do!")
    a = 1 + 1
    b = a * 2
    print("Okay I'm done!")


def a_broken_function():
    # This line might not show up in the generated issue because it's too far away
    #  from the line that triggered the issue.
    # The search for pertinent lines will stop when it hits a line break or the
    #  maximum number of lines, set by PERTINENT_LINE_LIMIT
    a = [
        1, 1, 2, 3
    ]
    b = sum(a)
    c = b * len(a)
    return c / 0  # FIXME I just don't know why this doesn't work!
    # Notice that this line will be collected

    # But this one won't, because there's some whitespace between it and the trigger!


def a_skipping_example():
    # Since the line below has `# todoon` in it, the checker will give it a pass even though it has the magic words!
    print("Sometimes you really have to write TODO or FIXME, like this!")  # todoon


def a_very_pretty_example():
    # TODO Titled Issue! | In this format, you can define a title and a body! Also labels like #example or #enhancement
    print("Check this out!")
```

## Usage

### CLI: `todoignore-util`

#### Usage

```bash
'''

  Small utility for generating a .todo-ignore file

'''

Arguments:
  SOURCES...  (default) [with -p] Files whose contents will be added to the
              .todo-ignore file.
              
                        [with -t] Lines of text to be added to the .todo-
                        ignore file.  [required]

Options:
  -c, --create / -u, --update     Whether to create a new .todo-ignore file or
                                  update an existing one  [default: create]
  -t, --source-text / -p, --source-paths
                                  Whether to treat SOURCES as text or as file
                                  paths.  [default: source-text]
  --help                          Show this message and exit.
```

#### Examples

> Combining common ignore files into an existing .todo-ignore file. If any files don't exist, they will simply be
> ignored gracefully.
>
> ```bash
> todoignore-util -up .gitignore .prettierignore
> ```

> Writing a new .todo-ignore file that contains all hidden folders (those which start with '.') to the .todo-ignore.
>
> TODO untested
> 
> ```bash
> todoignore-util $( ls -a | grep "^\.[^.]" )
> ```

### CLI: `todoon`

#### Usage

[[Generated by Typer, thanks Typer!](https://github.com/tiangolo/typer)]

```bash
'''

  Checks files for occurrences of TODO or FIXME and reports them for use with
  automation or other development operations.

'''

Arguments:
  [FILES]...  If specified, only these [FILES] will be scanned for TODOs and
              FIXMEs. Otherwise, all files in the current working directory
              except for those specified in .todo-ignore will be scanned.

Options:
  -p, --print / -i, --issue  Whether to print the discovered TODOs and FIXMEs
                             to stderr or to try an generate GitHub issues
                             [default: print]
  -s, --silent               If specified, todoon will not exit with an error
                             code even when TODOs and/or FIXMEs are detected
  -f, --force                If specified, the .todo-ignore file will not be
                             used. NOT RECOMMENDED
  -v, --verbose              If specified, todoon will not to print lengthy or
                             numerous messages (like each encoding failure)
  --help                     Show this message and exit. 
```

##### Arguments

[FILES]
: This optional argument allows you to specify which files todoon should scan. When left blank, todoon will scan every
file in the working directory that is not filtered out by the .todo-ignore

##### Options

--mode PRINT
: The default configuration, will print the discovered issues to stderr

--mode ISSUE
: Will generate issues and submit them via the [gh cli](https://cli.github.com/), with checks (see [Issues](#issues))

--silent
: Do not exit with a non-zero exit code, even if TODOs and/or FIXMEs are found

--force
: Run todo_check without a .todo-ignore. NOT RECOMMENDED! There could be a lot of files in there.

--verbose
: Print everything while running todoon, this will print each encoding error and which file it concerns.

--ni FILENAME
: Copy the contents of other files into a **N**EW [.todo-ignore](#todo-ignore), this option must be specified for each.
e.g. `--ni .gitignore --ni .prettierignore`

--xi FILENAME
: Copy the contents of other files into a E**X**ISTING [.todo-ignore](#todo-ignore), this option must be specified for
each. e.g. `--ni .gitignore --xi .prettierignore`

If a file discovered by `todoon` is not of a supported
encoding [see [SUPPORTED_ENCODINGS_TODO_CHECK](todo_or_not/localize.py) for most up-to-date list] it will be skipped.
The number of skipped files is summarized at the end of the run.

##### Feedback

todoon will summarize the run in stderr when it completes, it will also update a number of environment variables during
and after the run:

- `$TODOON_STATUS`
    - `starting`
    - `parsing-todo-ignore` (if applicable)
    - `collecting-targets` (if no targets specified)
    - `collecting-issues` (if mode is "issue")
    - `scanning-files`
- `$TODOON_PROGRESS`
    - starting at status `scanning-files`, this variable is updated to a percentage (e.g. '18.7') which reflects the
      number of targets scanned of all targets found
- `$TODOON_FILES_SCANNED`
- `$TODOON_TODOS_FOUND`
- `$TODOON_FIXMES_FOUND`
- `$TODOON_ENCODING_ERRORS`
- `$TODOON_ISSUES_GENERATED`
- `$TODOON_DUPLICATE_ISSUES_AVOIDED`

### Examples

> Find ALL issues in the current working directory (including any hidden folders/files) and exit non-zero if any are
> found
>
> ```bash
> todoon --force
> ```

> Show the issues the files "a.txt", "b.txt", and all the files that are under the directory "c/" without failing
>
> ```bash
> todoon --silent a.txt b.txt c/
> ```

> Generate all the issues found in the project that haven't already been generated (
> assumes [issues environment](#issues) is set up correctly and a .todo-ignore is in place)
>
> ```bash
> gh auth login 
> todoon --silent --mode issue 
> ```

### Environment Variables

MAXIMUM_ISSUES_GENERATED
: _default: 8_ <br> If in ISSUE mode, will exit the todo_check after a certain number of issues have been generated.

PERTINENT_LINE_LIMIT
: _default: 8_ <br> The greatest number of surrounding lines (in each direction) that will be collected in the body of
an issue generated in ISSUE mode (fewer may be gathered if they are broken up by blank lines)

### .todo-ignore

A plaintext file in a supported encoding.
This file specifies which files and directories that todo_check doesn't need to walk through or analyze.
It follows the same syntax as a .gitignore file.

Supported encodings:

* UTF-8
* UTF-16

[see [SUPPORTED_ENCODINGS_TODOIGNORE](todo_or_not/localize.py) for most up-to-date list]

### Issues

Issues are generated up to a limit (see [Environment Variables](#environment-variables)) and contain the line which
contains the TODO or FIXME and up to `$MAXIMUM_ISSUES_GENERATED` of the preceding and following lines.
See [Examples](#examples) for a good representation of how these look.

Issue generation is best supported from GitHub actions, the YAML included in this repository generates the necessary
credentials and keeps them safe for you, so it's the most recommended option. However, if you wish to run this
elsewhere, you must supply valid values to each of the following environment variables:

- GITHUB_REF_NAME
- GITHUB_REPOSITORY
- GITHUB_TRIGGERING_ACTOR

## Settings

### Localization

Try out your todoon in your language! In the environment that you're running `todoon` in, set the environment variable "
REGION" to your ISO code (see below). For example, on Windows (PowerShell): `$env:REGION="ko_kr"`

Currently supported:

* bu_mm - Burmese
* en_us - English (US)
* ko_kr - Korean

Don't see your language? Want to do a quick localization? Please feel free to contribute!
