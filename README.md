# Purpose
This repository exists to implement the Detective coding challenge given to me by _redacted_.

# How to Use
## Prerequisites
This software has been manually tested on Python {2.7, 3.4, 3.5, 3.6}. Versions before Python 2.7 are *not* supported.

Additionally you should have `setuptools` installed, for more information on installing setuptools [read the docs.](https://packaging.python.org/installing/#install-pip-setuptools-and-wheel).

## Installing:
If you run the command `python setup.py install`, the package will be installed and the command line option added to
your current path. I would recommend doing this in a virtualenv for ease of uninstall, but that is not required.

## Using the Command
### Help
To invoke the documentation on the new command run `detective -h`.

### Running against input
To run a single file, run the command `detective <path-to-valid-json>` and this will output the results in a
file `<original filename>_out.json`. 

For example: `detective example1.json` creates `./example1_out.json`.

The program also supports variadic arguments for input files allowing for batch processing. You can either manually list files or use the wildcard syntax.

For example:

`detective example1.json example2.json example3.json`

or

`detective example*.json`

All filenames must be next to each other in the argument list and there cannot be an optional argument specified in the list of files.

E.g. `detective example1.json -p example2.json` is a parse error.

### Specifying output
You can change the output directory to an *existing* directory using the `-o` option. By default, the directory of the input file will be used.

### Formatting output
Optionally, you can supply the `-p` flag to pretty-print the JSON in the output file.

## Running Tests:
Run `python setup.py test`.

# Problem Specification
## Assumptions
* All witness testimony is valid input data. "These witnesses are trustworthy"
* Event labels are unique
    * In real life, a suspect could `[['yell', 'run', 'yell']]`, but we will assume this would be marked
`[['yell1', 'run', 'yell2']]`
* Testimony is not mergeable if no unification allows for a shorter set of testimony
    * Practically this is equivalent to the output of the algorithm being the same as the original input

## The Problem
Given ordered lists of testimony, for example:
```python
[
    ["shouting", "fight", "fleeing"],
    ["fight", "gunshot", "panic", "fleeing"],
    ["anger", "shouting"],
]
```
the application should merge these into the longest possible timeline of events. 

In this case:
```python
["anger", "shouting", "fight", "gunshot", "panic", "fleeing"]
```

We are only interested in absolutely correct orderings of events. If there is any degree of ambiguity, it should be resolved by returning all possible timelines. For example:
```python
[
    ["shadowy figure", "demands", "scream", "siren"],
    ["shadowy figure", "pointed gun", "scream"],
]
```
should emit
```python
[
    ["shadowy figure", "demands", "scream", "siren"],
    ["shadowy figure", "pointed gun", "scream", "siren"],
]
```

If there is no possible merge of the input, the original input should be returned unmodified. For exampe:
```python
[
    ["argument", "stuff", "pointing"],
    ["press brief", "scandal", "pointing"],
    ["bribe", "coverup"],
]
```
should emit itself.

