#!/usr/bin/env python

from __future__ import print_function
from string import Template
import sys

# Characters
TEMPLATE_CHARS_UTF = {
    "chr_degree": 'CHAR(176)',  # degree sign
    "chr_space": 'CHAR(160)',   # non-breaking space
    "chr_min": 'CHAR(34)',      # "
    "chr_sec": 'CHAR(39)',      # '
    "chr_dot": 'CHAR(44)',      # .
    "chr_comma": 'CHAR(46)',    # ,
    "chr_zero": 'CHAR(48)',     # 0
}

# Characters
TEMPLATE_CHARS_ASCII = {
    "chr_degree": 'CHAR(100)',  # d
    "chr_space": 'CHAR(32)',    # regular space
    "chr_min": 'CHAR(34)',      # "
    "chr_sec": 'CHAR(39)',      # '
    "chr_dot": 'CHAR(44)',      # .
    "chr_comma": 'CHAR(46)',    # ,
    "chr_zero": 'CHAR(48)',     # 0
}

TEMPLATE_FORMULAS = {
    # Inputs: deg => deg/min/sec
    "degrees_dec": '(A2)',
    "minutes_rounding": '(B2)',
    "seconds_rounding": '(C2)',

    # Inpits: deg/min/sec => deg
    "in_deg": '(D2)',
    "in_min": '(E2)',
    "in_sec": '(F2)',
    
    # Conversions
    "degrees_int_abs": '(FLOOR(ABS(${degrees_dec});1))',
    "degrees_int": '(SIGN(${degrees_dec})*${degrees_int_abs})',

    "minutes_dec": '(60*(ABS(${degrees_dec})-${degrees_int_abs}))',
    "minutes_int": '(FLOOR(${minutes_dec};1))',

    # - rounding
    "minutes_decimals_raw": 'ROUND(POWER(10;${minutes_rounding})*(${minutes_dec} - ${minutes_int});0)',
    "minutes_decimals_padding_len": '(${minutes_rounding}-LEN(${minutes_decimals_raw}))',
    "minutes_decimals_padding": 'REPT(${chr_zero}; MAX(0; ${minutes_decimals_padding_len}))',
    "minutes_dec_rounded": 'IF(${minutes_rounding} > 0; CONCATENATE(${minutes_int}; ${chr_comma}; ${minutes_decimals_padding}; ${minutes_decimals_raw}); ${minutes_int})',

    "seconds_dec": '(60*(${minutes_dec}-${minutes_int}))',
    "seconds_int": 'FLOOR(${seconds_dec};1)',

    # - rounding
    "seconds_decimals_raw": 'ROUND(POWER(10;${seconds_rounding})*(${seconds_dec} - ${seconds_int});0)',
    "seconds_decimals_padding_len": '(${seconds_rounding}-LEN(${seconds_decimals_raw}))',
    "seconds_decimals_padding": 'REPT(${chr_zero}; MAX(0; ${seconds_decimals_padding_len}))',
    "seconds_dec_rounded": 'IF(${seconds_rounding} > 0; CONCATENATE(${seconds_int}; ${chr_comma}; ${seconds_decimals_padding}; ${seconds_decimals_raw}); ${seconds_int})',

    # Final formulas
    "form_deg2ddm_rounded":   'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec_rounded}; ${chr_min})',
    "form_deg2ddm_unrounded": 'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec}; ${chr_min})',
    "form_deg2ddm_int":       'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min})',

    "form_deg2dms_rounded":   'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec_rounded}; ${chr_sec})',
    "form_deg2dms_unrounded": 'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec}; ${chr_sec})',
    "form_deg2dms_int":       'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_int}; ${chr_sec})',

    "form_dms2deg":           '(${in_deg} + (60*${in_min}) + (3600*${in_sec}))',
    
    # Helpers for the CSV templates
    "csv_line":           '"=${form_deg2ddm_rounded}","=${form_deg2ddm_unrounded}","=${form_deg2ddm_int}","=${form_deg2dms_rounded}","=${form_deg2dms_unrounded}","=${form_deg2dms_int}"',
    "csv_head":           'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int',
    
    "csv_debug_head":     'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int,degrees_int,chr_degree,chr_space,minutes_int,chr_min,chr_space,seconds_dec_rounded,chr_sec,seconds_rounding,seconds_int,chr_comma,seconds_decimals_padding,seconds_decimals_raw,seconds_decimals_padding_len',
    "csv_debug_line":     '"=${form_deg2ddm_rounded}","=${form_deg2ddm_unrounded}","=${form_deg2ddm_int}","=${form_deg2dms_rounded}","=${form_deg2dms_unrounded}","=${form_deg2dms_int}","=${degrees_int}","=${chr_degree}","=${chr_space}","=${minutes_int}","=${chr_min}","=${chr_space}","=${seconds_dec_rounded}","=${chr_sec}","=${seconds_rounding}","=${seconds_int}","=${chr_comma}","=${seconds_decimals_padding}","=${seconds_decimals_raw}","=${seconds_decimals_padding_len}"',
}

# README.md document
TEXT_README_MD = \
'''# 10,123&deg; => 10&deg; 7" 22,8'

_Spreadsheet formulas for converting decimal degrees to DMS (degrees minutes seconds) and DDM 
(degrees decimal minutes)_

This page contains formulas for spreadsheet programs for converting angles in decimal degrees to
 fractional (degrees + minutes + seconds and degrees + decimal minutes) formats. 

Background: [https://en.wikipedia.org/wiki/Geographic coordinate conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)

## Usage

Simply copy and paste the formulas from below, or use one of the included files. Modify the
input cells as necessary. Each formula is self-contained and only depends on (one or more of) 
the input fields.

The decimal -> DDM / DMS formulas use three input cells (`${degrees_dec}`, `${minutes_rounding}` 
and  `${seconds_rounding}`) for the decimal degrees, number of decimals in the  produced minutes 
and seconds, respectively. The trivial DMS -> decimal formula uses `${in_deg}`, `${in_min}` and
`${in_sec}` for degrees, minutes and seconds. 

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

## Code

The formulas and the README.md you're reading now are generated by the `compile.py`script,
where the former are also found in human-readable form. It should work on Python 2 
and 3 without 3rd party libraries. See the Makefile for arguments. 

## Bugs
The `form_deg2dms_rounded` formula causes a "Formula overflow" error in OpenOffice.org 4.1.5
'''

TEXT_FORMULAS_MD = \
'''
## Formulas (degrees to fractions)
### Inputs

For decimal degrees => fractions conversion:

- Decimal degrees: `${degrees_dec}`
- Nr. of decimals to round minutes to: `${minutes_rounding}`
- Nr. of decimals to round seconds to: `${seconds_rounding}`

### Rounded values

Use these if you need the DDM or DMS representation as a human-readable string in a single cell.

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with rounded minutes
- (-10,123&deg;, 3, 3) => -10&deg;7.380"

_Returns a string representing the decimal degrees in `${degrees_dec}` in DDM format, minutes rounded to `${minutes_rounding}` digits_

`${form_deg2ddm_rounded}`


#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

_Returns a string representing the decimal degrees in `${degrees_dec}` in DMS format, seconds truncated to their integer value_

`${form_deg2dms_int}`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with rounded seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

_Returns a string representing the decimal degrees in `${degrees_dec}` in DMS format, seconds rounded to `${seconds_rounding}` digits_

`${form_deg2dms_rounded}`

### Component values

Use these if you need the numerical values in individual cells. 

#### DDM
##### (int) Degrees:

_Returns a number representing the integer degree component of the decimal degree value in `${degrees_dec}`_

`${degrees_int}`

##### (decimal) Minutes:

_Returns a number representing the decimal minute component of the decimal degree value in `${degrees_dec}`_

`(SIGN(${degrees_dec})*${minutes_dec})`

#### DMS 
##### (int) Degrees:

_Returns a number representing the integer degree component of the decimal degree value in `${degrees_dec}`_

`${degrees_int}`

##### (int) Minutes:

_Returns a number representing the integer minute component of the decimal degree value in `${degrees_dec}`_

`(SIGN(${degrees_dec})*${minutes_int})`

##### (decimal) Seconds:

_Returns a number representing the decimal seconds component of the decimal degree value in `${degrees_dec}`_

`(SIGN(${degrees_dec})*${seconds_dec})`

### Unrounded / raw values

Included for completeness, not necessarily useful.

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes
`${form_deg2ddm_unrounded}`

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes 

- NOTE: loss of precision

`${form_deg2ddm_int}`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds
`${form_deg2dms_unrounded}`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds 

- NOTE: loss of precision

`${form_deg2dms_int}`

## Formulas (fractions to degrees)
### Inputs

- Degrees: `${in_deg}`
- Minutes: `${in_min}`
- Seconds: `${in_sec}`


### (number) Decimal degrees
`${form_dms2deg}`

'''

# CSV document
TEXT_DEMO_CSV = \
'''Decimal_degr,Min_rounding,Sec_rounding,CMP_DDM_Round,CMP_DMS_Int,CMP,DMS_Round,${csv_head}
-10.123,4,4,"-10d 7.3800m","-10d 7m 22s","-10d 7m 22.8000s",${csv_line}

'''

# CSV document with debug info
TEXT_DEBUG_CSV = \
'''Decimal_degr,Min_rounding,Sec_rounding,${csv_debug_head}
-10.123,3,3,${csv_debug_line}
'''

# Renderer
def render(text, templates):
    new_text = Template(text).substitute(**templates)
    if text == new_text:
        return text
    return render(new_text, templates)
    
# Main
if len(sys.argv) < 2 or sys.argv[1] == 'README.md':
    t = {}
    t.update(TEMPLATE_CHARS_UTF)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_README_MD, t))
    print(render(TEXT_FORMULAS_MD, t))

elif sys.argv[1] == 'formulas-ascii.md':
    t = {}
    t.update(TEMPLATE_CHARS_ASCII)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_FORMULAS_MD, t))

elif sys.argv[1] == 'demo-ascii.csv':
    t = {}
    t.update(TEMPLATE_CHARS_ASCII)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_DEMO_CSV, t))

elif sys.argv[1] == 'demo-unicode.csv':
    t = {}
    t.update(TEMPLATE_CHARS_UTF)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_DEMO_CSV, t))

elif sys.argv[1] == 'debug-ascii.csv':
    t = {}
    t.update(TEMPLATE_CHARS_ASCII)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_DEBUG_CSV, t))

elif sys.argv[1] == 'debug-unicode.csv':
    t = {}
    t.update(TEMPLATE_CHARS_UTF)
    t.update(TEMPLATE_FORMULAS)
    print(render(TEXT_DEBUG_CSV, t))

else:
    print("Unknown argument " + sys.argv[1])
    sys.exit(1)
    
