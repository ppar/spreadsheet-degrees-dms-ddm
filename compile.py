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
    # Inputs
    "degrees_dec": '(A2)',
    "minutes_rounding": '(B2)',
    "seconds_rounding": '(C2)',

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
    "form_ddm_rounded":   'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec_rounded}; ${chr_min})',
    "form_ddm_unrounded": 'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_dec}; ${chr_min})',
    "form_ddm_int":       'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min})',

    "form_dms_rounded":   'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec_rounded}; ${chr_sec})',
    "form_dms_unrounded": 'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_dec}; ${chr_sec})',
    "form_dms_int":       'CONCATENATE(${degrees_int}; ${chr_degree}; ${chr_space}; ${minutes_int}; ${chr_min}; ${chr_space}; ${seconds_int}; ${chr_sec})',

    # Helpers for the CSV templates
    "csv_line":           '"=${form_ddm_rounded}","=${form_ddm_unrounded}","=${form_ddm_int}","=${form_dms_rounded}","=${form_dms_unrounded}","=${form_dms_int}"',
    "csv_head":           'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int',
    
    "csv_debug_head":     'DDM_Round,DDM_URound,DDM_Int,DMS_Round,DMS_URound,DMS_Int,degrees_int,chr_degree,chr_space,minutes_int,chr_min,chr_space,seconds_dec_rounded,chr_sec,seconds_rounding,seconds_int,chr_comma,seconds_decimals_padding,seconds_decimals_raw,seconds_decimals_padding_len',
    "csv_debug_line":     '"=${form_ddm_rounded}","=${form_ddm_unrounded}","=${form_ddm_int}","=${form_dms_rounded}","=${form_dms_unrounded}","=${form_dms_int}","=${degrees_int}","=${chr_degree}","=${chr_space}","=${minutes_int}","=${chr_min}","=${chr_space}","=${seconds_dec_rounded}","=${chr_sec}","=${seconds_rounding}","=${seconds_int}","=${chr_comma}","=${seconds_decimals_padding}","=${seconds_decimals_raw}","=${seconds_decimals_padding_len}"'
}

# README.md document
README_MD = \
'''# 10,123&deg; => 10&deg; 7" 22,8'

_Spreadsheet formulas for converting decimal degrees to DMS (degrees minutes seconds) and DDM 
(degrees decimal minutes)_

This page contains formulas for spreadsheet programs for converting angles in decimal degrees to
 fractional (degrees + minutes + seconds and degrees + decimal minutes) formats. 

Background: [https://en.wikipedia.org/wiki/Geographic coordinate conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)

## Usage

Simply copy and paste the formulas from below, or use the `demo.csv` file, or use `./compile.py` 
to roll your own. Modify the input cells as necessary.

The formulas use three input cells (`${degrees_dec}`, `${minutes_rounding}` and  `${seconds_rounding}`) 
for the decimal degrees, number of decimals in the  produced minutes and seconds, respectively

## Code

The formulas are compiled by the `compile.py` script, where they are also found in human-readable 
form. 

To generage the  `README.md` file you're reading now, run `./compile.py -readme`. To generate 
the CSV file, run `./compile.py -csv`. It should work on Python 2 and 3 without 3rd party libraries.
The CSV files are generated with ASCII formatting, while the README.md uses UNICODE characters 
for the degree sign and non-breaking space. 

## Bugs
The `form_dms_rounded` formula causes a "Formula overflow" error in OpenOffice.org 4.1.5

## Formulas
### Inputs

- Decimal degrees: `${degrees_dec}`
- Nr. of decimals to round minutes to: `${minutes_rounding}`
- Nr. of decimals to round seconds to: `${seconds_rounding}`

### Rounded values

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with rounded minutes
- (-10,123&deg;, 3, 3) => -10&deg;7.380"

`${form_ddm_rounded}`


####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

`${form_dms_int}`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with rounded seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`${form_dms_rounded}`

### Unrounded / raw values

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes
`${form_ddm_unrounded}`

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes (NOTE: loss of precision)
`${form_ddm_int}`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds
`${form_dms_unrounded}`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds (NOTE: loss of precision)
`${form_dms_int}`
'''

# CSV document
CSV = \
'''Decimal_degr,Min_rounding,Sec_rounding,CMP_DDM_Round,CMP_DMS_Int,CMP,DMS_Round,${csv_head}
-10.123,3,3,0,0,0,${csv_line}

'''

# CSV document with debug info
CSV_DEBUG = \
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
if len(sys.argv) < 2 or sys.argv[1] == '-readme':
    t = {}
    t.update(TEMPLATE_CHARS_UTF)
    t.update(TEMPLATE_FORMULAS)
    print(render(README_MD, t))

elif sys.argv[1] == '-csv':
    t = {}
    t.update(TEMPLATE_CHARS_ASCII)
    t.update(TEMPLATE_FORMULAS)
    print(render(CSV, t))

elif sys.argv[1] == '-csv-debug':
    t = {}
    t.update(TEMPLATE_CHARS_ASCII)
    t.update(TEMPLATE_FORMULAS)
    print(render(CSV_DEBUG, t))

else:
    print("Unknown argument " + sys.argv[1])
    sys.exit(1)
    
