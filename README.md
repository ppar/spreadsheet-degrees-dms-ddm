# 10,123&deg; => 10&deg; 7" 22,8'

_Spreadsheet formulas for converting decimal degrees to DMS (degrees minutes seconds) and DDM 
(degrees decimal minutes)_

This page contains formulas for spreadsheet programs for converting angles in decimal degrees to
 fractional (degrees + minutes + seconds and degrees + decimal minutes) formats. 

Background: [https://en.wikipedia.org/wiki/Geographic coordinate conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)

## Usage

Simply copy and paste the formulas from below, or use the `demo.csv` file, or use `./compile.py` 
to roll your own. Modify the input cells as necessary.

The formulas use three input cells (`(A2)`, `(B2)` and  `(C2)`) 
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

- Decimal degrees: `(A2)`
- Nr. of decimals to round minutes to: `(B2)`
- Nr. of decimals to round seconds to: `(C2)`

### Rounded values

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with rounded minutes
- (-10,123&deg;, 3, 3) => -10&deg;7.380"

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(34))`


####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(160); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(39))`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with rounded seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(160); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(39))`

### Unrounded / raw values

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (60*(ABS((A2))-(FLOOR(ABS((A2));1)))); CHAR(34))`

####  Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes (NOTE: loss of precision)
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34))`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(160); (60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))); CHAR(39))`

####  Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds (NOTE: loss of precision)
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(176); CHAR(160); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(160); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(39))`

