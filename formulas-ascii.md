
## Formulas (degrees to fractions)
### Inputs

For decimal degrees => fractions conversion:

- Decimal degrees: `(A2)`
- Nr. of decimals to round minutes to: `(B2)`
- Nr. of decimals to round seconds to: `(C2)`

### Rounded values

Use these if you need the DDM or DMS representation as a human-readable string in a single cell.

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with rounded minutes
- (-10,123&deg;, 3, 3) => -10&deg;7.380"

_Returns a string representing the decimal degrees in `(A2)` in DDM format, minutes rounded to `(B2)` digits_

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(34))`


#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

_Returns a string representing the decimal degrees in `(A2)` in DMS format, seconds truncated to their integer value_

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(32); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(39))`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with rounded seconds
- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

_Returns a string representing the decimal degrees in `(A2)` in DMS format, seconds rounded to `(C2)` digits_

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(32); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(39))`

### Component values

Use these if you need the numerical values in individual cells. 

#### DDM
##### (int) Degrees:

_Returns a number representing the integer degree component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR(ABS((A2));1)))`

##### (decimal) Minutes:

_Returns a number representing the decimal minute component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(60*(ABS((A2))-(FLOOR(ABS((A2));1)))))`

#### DMS 
##### (int) Degrees:

_Returns a number representing the integer degree component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR(ABS((A2));1)))`

##### (int) Minutes:

_Returns a number representing the integer minute component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))`

##### (decimal) Seconds:

_Returns a number representing the decimal seconds component of the decimal degree value in `(A2)`_

`(SIGN((A2))*(60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))))`

### Unrounded / raw values

Included for completeness, not necessarily useful.

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with unrounded minutes
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (60*(ABS((A2))-(FLOOR(ABS((A2));1)))); CHAR(34))`

#### (string) Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes 

- NOTE: loss of precision

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34))`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds
`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(32); (60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))); CHAR(39))`

#### (string) Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds 

- NOTE: loss of precision

`CONCATENATE((SIGN((A2))*(FLOOR(ABS((A2));1))); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(34); CHAR(32); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(39))`

## Formulas (fractions to degrees)
### Inputs

- Degrees: `(D2)`
- Minutes: `(E2)`
- Seconds: `(F2)`


### (number) Decimal degrees
`((D2) + (60*(E2)) + (3600*(F2)))`


