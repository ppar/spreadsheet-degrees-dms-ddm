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

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(39))`


#### (string) `form_deg2ddm_rounded_w`
_Returns a string representing the decimal degrees in `(A2)` in DDM (Degrees, Decimal Minutes) format, minutes rounded to `(B2)` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg;7.380"


`IF(ISBLANK((A2)); (A2); IF((A2) = CHAR(45); (A2); CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); IF((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) < 10; 0; REPT(CHAR(32); 0)); IF((B2) > 0; CONCATENATE((FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(46); REPT(CHAR(48); MAX(0; ((B2)-LEN(ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0))))); ROUND(POWER(10;(B2))*((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) - (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)));0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))); CHAR(39))))`

#### (string) `form_deg2dms_int`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds) format, seconds truncated to their integer value_

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22'

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(32); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(34))`

#### (string) `form_deg2dms_rounded`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds)  format, seconds rounded to `(C2)` digits. Blank inputs are intepreted as zero._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(32); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(34))`

#### (string) `form_deg2dms_rounded_w`
_Returns a string representing the decimal degrees in `(A2)` in DMS (Degrees, Minutes, Seconds) format, seconds rounded to `(C2)` digits. Blank and "-" inputs are returned as-is. Minutes and seconds are zero-padded to 2 digits._

- (-10,123&deg;, 3, 3) => -10&deg; 7" 22.800'

`IF(ISBLANK((A2)); (A2); IF((A2) = CHAR(45); (A2); CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); IF((60*(ABS((A2))-(FLOOR(ABS((A2));1)))) < 10; 0; REPT(CHAR(32); 0)); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(32); IF((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) < 10; 0; REPT(CHAR(32); 0)); IF((C2) > 0; CONCATENATE(FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(46); REPT(CHAR(48); MAX(0; ((C2)-LEN(ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0))))); ROUND(POWER(10;(C2))*((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))) - FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1));0)); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1)); CHAR(34))))`

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

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (60*(ABS((A2))-(FLOOR(ABS((A2));1)))); CHAR(39))`

#### (string) `form_deg2ddm_int`
_Decimal degrees to DDM (Degrees, Decimal Minutes) with integer minutes (NOTE: loss of precision)_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39))`

#### (string) `form_deg2dms_unrounded`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with unrounded decimal seconds_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(32); (60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)))); CHAR(34))`

#### (string) `form_deg2dms_int`
_Decimal degrees to DMS (Degrees, Minutes, Seconds) with integer seconds (NOTE: loss of precision)_

`CONCATENATE(IF(SIGN((A2))=-1;CHAR(45);CHAR(32)); (FLOOR(ABS((A2));1)); CHAR(100); CHAR(32); (FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1)); CHAR(39); CHAR(32); FLOOR((60*((60*(ABS((A2))-(FLOOR(ABS((A2));1))))-(FLOOR((60*(ABS((A2))-(FLOOR(ABS((A2));1))));1))));1); CHAR(34))`

## Formulas (fractions to degrees)
### Inputs

- Degrees: `(D2)`
- Minutes: `(E2)`
- Seconds: `(F2)`


### (number) `form_dms2deg`
_Returns the decimal degrees value corresponding to the input DMS components `(D2)`, `(E2)`, `(F2)`_

`((D2)+((E2)/60)+((F2)/3600))`


