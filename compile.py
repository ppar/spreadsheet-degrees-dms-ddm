#!/usr/bin/env python

from __future__ import print_function
from string import Template
import sys

# Characters
TEMPLATE_CHARS_UTF = {
    "chr_degree": 'CHAR(176)',   # degree sign
    "chr_space":  'CHAR(160)',   # non-breaking space
    "chr_min":    'CHAR(39)',    # '
    "chr_sec":    'CHAR(34)',    # "
    "chr_dot":    'CHAR(44)',    # .
    "chr_minus":  'CHAR(45)',    # -
    "chr_comma":  'CHAR(46)',    # ,
    "chr_zero":   'CHAR(48)',    # 0
}

# Characters
TEMPLATE_CHARS_ASCII = {
    "chr_degree": 'CHAR(100)',   # d
    "chr_space":  'CHAR(32)',    # regular space
    "chr_min":    'CHAR(39)',    # '
    "chr_sec":    'CHAR(34)',    # "
    "chr_dot":    'CHAR(44)',    # .
    "chr_minus":  'CHAR(45)',    # -
    "chr_comma":  'CHAR(46)',    # ,
    "chr_zero":   'CHAR(48)',    # 0
}

TEMPLATE_INPUTS = {
    "in_deg_dec":   '(A2)',      # Decimal degrees
    "in_round_min": '(B2)',      # Rounding for minutes
    "in_round_sec": '(C2)',      # Rounding for seconds

    "in_cpt_deg": '(D2)',        # Component: degrees
    "in_cpt_min": '(E2)',        # Component: minutes
    "in_cpt_sec": '(F2)',        # Component: seconds
}

TEMPLATE_COMPUTE = {
    # Sign
    "sign":        'IF(SIGN(${in_deg_dec})=-1;${chr_minus};${chr_space})',
    
    # Conversions
    "degrees_int": '(FLOOR(ABS(${in_deg_dec});1))',    
    "minutes_dec": '(60*(ABS(${in_deg_dec})-${degrees_int}))',
    "minutes_int": '(FLOOR(${minutes_dec};1))',
    "seconds_dec": '(60*(${minutes_dec}-${minutes_int}))',
    "seconds_int": 'FLOOR(${seconds_dec};1)',

    # - rounding
    "minutes_decimals_raw":         'ROUND(POWER(10;${in_round_min})*(${minutes_dec} - ${minutes_int});0)',
    "minutes_decimals_padding_len": '(${in_round_min}-LEN(${minutes_decimals_raw}))',
    "minutes_decimals_padding":     'REPT(${chr_zero}; MAX(0; ${minutes_decimals_padding_len}))',
    "minutes_dec_rounded":          'IF(${in_round_min} > 0; CONCATENATE(${minutes_int}; ${chr_comma}; ${minutes_decimals_padding}; ${minutes_decimals_raw}); ${minutes_int})',
    "minutes_padding":              'IF(${minutes_dec} < 10; 0; REPT(CHAR(32); 0))',

    # - rounding
    "seconds_decimals_raw":         'ROUND(POWER(10;${in_round_sec})*(${seconds_dec} - ${seconds_int});0)',
    "seconds_decimals_padding_len": '(${in_round_sec}-LEN(${seconds_decimals_raw}))',
    "seconds_decimals_padding":     'REPT(${chr_zero}; MAX(0; ${seconds_decimals_padding_len}))',
    "seconds_dec_rounded":          'IF(${in_round_sec} > 0; CONCATENATE(${seconds_int}; ${chr_comma}; ${seconds_decimals_padding}; ${seconds_decimals_raw}); ${seconds_int})',
    "seconds_padding":              'IF(${seconds_dec} < 10; 0; REPT(CHAR(32); 0))',
}
    
TEMPLATE_OUTPUTS = {
    # Final formulas
    "form_deg2ddm_rounded":   'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec_rounded}; ${chr_min})',
    "form_deg2ddm_rounded_p": 'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_padding}; ${minutes_dec_rounded}; ${chr_min})',
    "form_deg2ddm_rounded_w": 'IF(ISBLANK(${in_deg_dec}); ${in_deg_dec}; IF(${in_deg_dec} = ${chr_minus}; ${in_deg_dec}; ${form_deg2ddm_rounded_p}))',
    "form_deg2ddm_unrounded": 'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec}; ${chr_min})',
    "form_deg2ddm_int":       'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min})',
    
    "form_deg2dms_rounded":   'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec_rounded}; ${chr_sec})',
    "form_deg2dms_rounded_p": 'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_padding}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_padding}; ${seconds_dec_rounded}; ${chr_sec})',
    "form_deg2dms_rounded_w": 'IF(ISBLANK(${in_deg_dec}); ${in_deg_dec}; IF(${in_deg_dec} = ${chr_minus}; ${in_deg_dec}; ${form_deg2dms_rounded_p}))',
    "form_deg2dms_unrounded": 'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec}; ${chr_sec})',
    "form_deg2dms_int":       'CONCATENATE(${sign}; ${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_int}; ${chr_sec})',

    "form_dms2deg":           '(${in_cpt_deg}+(${in_cpt_min}/60)+(${in_cpt_sec}/3600))',

    # Component values
    "cpt_degrees_int": '(SIGN(${in_deg_dec})*${degrees_int})',
    "cpt_minutes_dec": '(SIGN(${in_deg_dec})*${minutes_dec})',
    "cpt_minutes_int": '(SIGN(${in_deg_dec})*${minutes_int})',
    "cpt_seconds_dec": '(SIGN(${in_deg_dec})*${seconds_dec})',

    # Helpers for the CSV templates
    "csv_line":           '"=${form_deg2ddm_rounded}","=${form_deg2ddm_unrounded}","=${form_deg2ddm_int}","=${form_deg2dms_rounded}","=${form_deg2dms_unrounded}","=${form_deg2dms_int}"',
    "csv_head":           'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int',
    
    "csv_debug_head":     'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int,degrees_int,chr_degree,chr_space,minutes_int,chr_min,chr_space,seconds_dec_rounded,chr_sec,in_round_sec,seconds_int,chr_comma,seconds_decimals_padding,seconds_decimals_raw,seconds_decimals_padding_len',
    "csv_debug_line":     '"=${form_deg2ddm_rounded}","=${form_deg2ddm_unrounded}","=${form_deg2ddm_int}","=${form_deg2dms_rounded}","=${form_deg2dms_unrounded}","=${form_deg2dms_int}","=${degrees_int}","=${chr_degree}","=${chr_space}","=${minutes_int}","=${chr_min}","=${chr_space}","=${seconds_dec_rounded}","=${chr_sec}","=${in_round_sec}","=${seconds_int}","=${chr_comma}","=${seconds_decimals_padding}","=${seconds_decimals_raw}","=${seconds_decimals_padding_len}"',
}

# README.md document
TEXT_README_MD = '''\
# 10,123&deg; => 10&deg; 07" 22,800'

This page contains formulas for spreadsheet programs for converting angles in decimal degrees to
 fractional (degrees + minutes + seconds and degrees + decimal minutes) formats. 

Background: [https://en.wikipedia.org/wiki/Geographic coordinate conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)

## Bugs & Caveats
- The `form_deg2dms_rounded` formula causes a "Formula overflow" error in OpenOffice.org 4.1.5
- Some inputs cause a _"FLOOR requires both arguments to be positive or negative"_ error, probably some float rounding issue:
    - 4.1
    - 3.9
    - 12.95
- The whole thing is hastily put together and not thoroughly tested

## Usage

Simply copy and paste the formulas from below, or use one of the included files. Modify the
input cells as necessary. Each formula is self-contained and only depends on (one or more of) 
the input fields.

Use `./compile.py -f ...  -i ... -i ...` to print out a single formula with custom input fields.

The decimal -> DDM / DMS formulas use three input cells (`${in_deg_dec}`, `${in_round_min}` 
and  `${in_round_sec}`) for the decimal degrees, number of decimals in the  produced minutes 
and seconds, respectively. The trivial DMS -> decimal formula uses `${in_cpt_deg}`, `${in_cpt_min}` and
`${in_cpt_sec}` for degrees, minutes and seconds. 

Import options for CSV: 
- Separated by: comma
- Text delimiter: "

### Files

With Unicode values in `CHAR()` calls (for spaces and the degree sign):

- [README.md](README.md) (this file)
- [demo-unicode.csv](demo-unicode.csv)
- [debug-unicode.csv](debug-unicode.csv)

With ASCII values in `CHAR()` calls (for spaces and the degree sign):

- [formulas-ascii.md](formulas-ascii.md)
- [demo-ascii.csv](demo-ascii.csv)
- [debug-ascii.csv](debug-ascii.csv)

### `compile.py`

The formulas and the README.md you're reading now are generated by the `compile.py`script,
where the former are also found in human-readable form. It should work on Python 2.7+
without 3rd party libraries. 

```text
${compile_py_usage}
```
'''

TEXT_FORMULAS_MD = '''\
## Formulas (degrees to fractions)
### Inputs

For decimal degrees => fractions conversion:

- Decimal degrees: `${in_deg_dec}`
- Nr. of decimals to round minutes to: `${in_round_min}`
- Nr. of decimals to round seconds to: `${in_round_sec}`

### Rounded values

Use these if you need the DDM or DMS representation as a human-readable string in a single cell.

#### (string) `form_deg2ddm_rounded`
_Returns a string representing the decimal degrees in `${in_deg_dec}` in DDM (Degrees, Decimal Minutes) format, minutes rounded to `${in_round_min}` digits. Blank inputs are interpreted as zero._

- (-10,123&deg;, 3, 3) => -10&deg;7.380"

`${form_deg2ddm_rounded}`


#### (string) `form_deg2ddm_rounded_w`
_Returns a string representing the decimal degrees in `${in_deg_dec}` in DDM (Degrees, Decimal Minutes) format, minutes rounded to `${in_round_min}` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg;7.380"


`${form_deg2ddm_rounded_w}`

#### (string) `form_deg2dms_int`
_Returns a string representing the decimal degrees in `${in_deg_dec}` in DMS (Degrees, Minutes, Seconds) format, seconds truncated to their integer value_

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

`${form_deg2dms_int}`

#### (string) `form_deg2dms_rounded`
_Returns a string representing the decimal degrees in `${in_deg_dec}` in DMS (Degrees, Minutes, Seconds)  format, seconds rounded to `${in_round_sec}` digits. Blank inputs are intepreted as zero._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`${form_deg2dms_rounded}`

#### (string) `form_deg2dms_rounded_w`
_Returns a string representing the decimal degrees in `${in_deg_dec}` in DMS (Degrees, Minutes, Seconds) format, seconds rounded to `${in_round_sec}` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`${form_deg2dms_rounded_w}`

### Component values

Use these if you need to populate individual cells with the numerical component values

#### DDM

##### (int) `cpt_degrees_int`
_Returns a number representing the integer degree component of the decimal degree value in `${in_deg_dec}`_

`${cpt_degrees_int}`

##### (decimal) `cpt_minutes_dec`
_Returns a number representing the decimal minute component of the decimal degree value in `${in_deg_dec}`_

`${cpt_minutes_dec}`

#### DMS 

##### (int) `cpt_degrees_int`
_Returns a number representing the integer degree component of the decimal degree value in `${in_deg_dec}`_

`${cpt_degrees_int}`

##### (int) `cpt_minutes_int`
_Returns a number representing the integer minute component of the decimal degree value in `${in_deg_dec}`_

`${cpt_minutes_int}`

##### (decimal) `cpt_seconds_dec`

_Returns a number representing the decimal seconds component of the decimal degree value in `${in_deg_dec}`_

`${cpt_seconds_dec}`

### Unrounded / raw values

Included for completeness, not necessarily useful.

#### (string) `form_deg2ddm_unrounded`
_Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes_

`${form_deg2ddm_unrounded}`

#### (string) `form_deg2ddm_int`
_Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes (NOTE: loss of precision)_

`${form_deg2ddm_int}`

#### (string) `form_deg2dms_unrounded`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds_

`${form_deg2dms_unrounded}`

#### (string) `form_deg2dms_int`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds (NOTE: loss of precision)_

`${form_deg2dms_int}`

## Formulas (fractions to degrees)
### Inputs

- Degrees: `${in_cpt_deg}`
- Minutes: `${in_cpt_min}`
- Seconds: `${in_cpt_sec}`


### (number) `form_dms2deg`
_Returns the decimal degrees value corresponding to the input DMS components `${in_cpt_deg}`, `${in_cpt_min}`, `${in_cpt_sec}`_

`${form_dms2deg}`

'''

# CSV document
TEXT_DEMO_CSV = '''\
Decimal_degr,Min_rounding,Sec_rounding,CMP_DDM_Round,CMP_DMS_Int,CMP,${csv_head}
-10.123,4,4,"-10d 7.3800m","-10d 7m 22s","-10d 7m 22.8000s",${csv_line}
'''

# CSV document with debug info
TEXT_DEBUG_CSV = '''\
Decimal_degr,Min_rounding,Sec_rounding,${csv_debug_head}
-10.123,3,3,${csv_debug_line}
'''

USAGE = '''\
Usage:
    ./compile.py <-t|--text> <text name> [options...]
    ./compile.py <-f|--formula> <formula name> [options...]
    ./compile.py <-h|--help>

Modes:
    -t|--text <text name>:       Prints out the named text
    -f|--formula <formula name>: Prints out the named output formula

Options:
    -c|--charset <ascii|unicode>
         Choose ASCII or Unicode values for CHAR() calls (default: ascii)
    -i|--input input_name=input_value
         Override values for input parameters (spreadsheet cell names or
         static values)

Valid arguments for -t|--text:
    README.md, formulas.md, demo.csv, debug.csv

Valid arguments for -f|--formula: ${formula_names}

Valid arguments and default values for -i|--input: ${input_names}

Example:
    Compile the "form_deg2dms_rounded_w" formula with input 
    from mytable::E4 and rounding set to 0 digits:

    ./compile.py -f form_deg2dms_rounded_w -i in_deg_dec=mytable::E4 \\
        -i in_round_min=0 -i in_round_sec=0

'''

# Renderer
def render(text, templates):
    new_text = Template(text).substitute(**templates)
    if text == new_text:
        return text
    return render(new_text, templates)

# Abort w/ error
def die(error):
    print(error + " (try -h|--help)")
    sys.exit(1)

# Abort w/ help message
def get_usage():
    tpl = {
        "formula_names": "",
        "input_names": ""
    }
    for key in sorted(TEMPLATE_OUTPUTS.keys()):
        tpl["formula_names"] += "\n    {}".format(key)
    for key in sorted(TEMPLATE_INPUTS.keys()):
        tpl["input_names"] += "\n    {}={}".format(key, TEMPLATE_INPUTS[key])
        
    return render(USAGE, tpl)
    
# Main
def main():

    templates = TEMPLATE_COMPUTE
    templates.update(TEMPLATE_CHARS_ASCII)
    templates.update(TEMPLATE_INPUTS)
    templates.update(TEMPLATE_OUTPUTS)

    mode = ""
    next_arg = ""
    for arg in sys.argv[1:]:
        if arg in ["-h", "--help"]:
            print(get_usage())
            sys.exit(0)
            
        if next_arg in ["-t", "--text", "-f", "--formula"]:
            mode = next_arg
            mode_arg = arg
            next_arg = ""
            continue
        if next_arg in ["-c", "--charset"]:
            if arg == "unicode":
                templates.update(TEMPLATE_CHARS_UTF)
            elif arg == "ascii":
                templates.update(TEMPLATE_CHARS_ASCII)
            else:
                die("Unknown charset {}".format(arg))
            next_arg = ""
            continue
        if next_arg in ['-i', '--input']:
            try:
                input_name, input_value = arg.split("=", 1)
            except ValueError:
                die("Missing/malformed argument to --input")
            
            templates[input_name] = input_value
            next_arg = ""
            continue
        if arg in ["-t", "--text", "-f", "--formula", "-c", "--charset", '-i', '--input']:
            next_arg = arg
            continue
        else:
            die("Unknown parameter {}".format(arg))
    if next_arg != "":
        die("Missing argument to {}".format(next_arg))
            
    # Mode
    if mode in ["-t", "--text"]:
        if mode_arg == 'README.md':
            templates.update({
                "compile_py_usage": get_usage()
            })
            print(render(TEXT_README_MD, templates))
            print(render(TEXT_FORMULAS_MD, templates))
        elif mode_arg == 'formulas.md':
            print(render(TEXT_FORMULAS_MD, templates))
        elif mode_arg == 'demo.csv':
            print(render(TEXT_DEMO_CSV, templates))
        elif mode_arg == 'debug.csv':
            print(render(TEXT_DEBUG_CSV, templates))
        else:
            die("Unknown text name: {}".format(mode_arg))
        return
    if mode in ["-f", "--formula"]:
        print(render("${" + mode_arg + "}", templates))
        return
    
    die("Unknown/missing mode argument")

main()
