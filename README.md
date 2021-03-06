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

The decimal -> DDM / DMS formulas use three input cells (`(A2)`, `(B2)` 
and  `(C2)`) for the decimal degrees, number of decimals in the  produced minutes 
and seconds, respectively. The trivial DMS -> decimal formula uses `(D2)`, `(E2)` and
`(F2)` for degrees, minutes and seconds. 

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

Valid arguments for -f|--formula: 
    cpt_degrees_int
    cpt_minutes_dec
    cpt_minutes_int
    cpt_seconds_dec
    csv_debug_head
    csv_debug_line
    csv_head
    csv_line
    form_deg2ddm_int
    form_deg2ddm_rounded
    form_deg2ddm_rounded_p
    form_deg2ddm_rounded_w
    form_deg2ddm_unrounded
    form_deg2dms_int
    form_deg2dms_rounded
    form_deg2dms_rounded_p
    form_deg2dms_rounded_w
    form_deg2dms_unrounded
    form_dms2deg

Valid arguments and default values for -i|--input: 
    in_cpt_deg=(D2)
    in_cpt_min=(E2)
    in_cpt_sec=(F2)
    in_deg_dec=(A2)
    in_round_min=(B2)
    in_round_sec=(C2)

Example:
    Compile the "form_deg2dms_rounded_w" formula with input 
    from mytable::E4 and rounding set to 0 digits:

    ./compile.py -f form_deg2dms_rounded_w -i in_deg_dec=mytable::E4 \
        -i in_round_min=0 -i in_round_sec=0


```

## Formulas (degrees to fractions)
### Inputs

For decimal degrees => fractions conversion:

- Decimal degrees: `(A2)`
- Nr. of decimals to round minutes to: `(B2)`
- Nr. of decimals to round seconds to: `(C2)`

### Rounded values

Use these if you need the DDM or DMS representation as a human-readable string in a single cell.

#### (string) `form_deg2ddm_rounded`
_Returns a string representing the decimal degrees in `(A2)` in DDM (Degrees, Decimal Minutes) format, minutes rounded to `(B2)` digits. Blank inputs are interpreted as zero._

- (-10,123&deg;, 3, 3) => -10&deg;7.380"

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(39))`


#### (string) `form_deg2ddm_rounded_w`
_Returns a string representing the decimal degrees in `(A2)` in DDM (Degrees, Decimal Minutes) format, minutes rounded to `(B2)` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg;7.380"


`IF(ISBLANK((A2)); (A2); IF((A2) = CHAR(45); (A2); CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); IF((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) < 10; 0; REPT(CHAR(32); 0)); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(39))))`

#### (string) `form_deg2dms_int`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds) format, seconds truncated to their integer value_

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(160); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(34))`

#### (string) `form_deg2dms_rounded`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds)  format, seconds rounded to `(C2)` digits. Blank inputs are intepreted as zero._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(160); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(34))`

#### (string) `form_deg2dms_rounded_w`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds) format, seconds rounded to `(C2)` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`IF(ISBLANK((A2)); (A2); IF((A2) = CHAR(45); (A2); CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); IF((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) < 10; 0; REPT(CHAR(32); 0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(160); IF((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) < 10; 0; REPT(CHAR(32); 0)); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(34))))`

### Component values

Use these if you need to populate individual cells with the numerical component values

#### DDM

##### (int) `cpt_degrees_int`
_Returns a number representing the integer degree component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR(ABS((A2));1)))`

##### (decimal) `cpt_minutes_dec`
_Returns a number representing the decimal minute component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(60*(ABS((A2))-(FLOOR(ABS((A2));1)))))`

#### DMS 

##### (int) `cpt_degrees_int`
_Returns a number representing the integer degree component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR(ABS((A2));1)))`

##### (int) `cpt_minutes_int`
_Returns a number representing the integer minute component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))`

##### (decimal) `cpt_seconds_dec`

_Returns a number representing the decimal seconds component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))))`

### Unrounded / raw values

Included for completeness, not necessarily useful.

#### (string) `form_deg2ddm_unrounded`
_Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (60*(ABS((A2))-(FLOOR(ABS((A2));1)))); CHAR(39))`

#### (string) `form_deg2ddm_int`
_Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes (NOTE: loss of precision)_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39))`

#### (string) `form_deg2dms_unrounded`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(160); (60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))); CHAR(34))`

#### (string) `form_deg2dms_int`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds (NOTE: loss of precision)_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(160)); (FLOOR(ABS((A2));1)); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(160); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(34))`

## Formulas (fractions to degrees)
### Inputs

- Degrees: `(D2)`
- Minutes: `(E2)`
- Seconds: `(F2)`


### (number) `form_dms2deg`
_Returns the decimal degrees value corresponding to the input DMS components `(D2)`, `(E2)`, `(F2)`_

`((D2)+((E2)/60)+((F2)/3600))`


