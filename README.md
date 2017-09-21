# pox

This package provides convenient ways to handle Origin objects.

## Low-Level
### pox.theme
By getting and setting the theme, you can change the style of an Origin object. 

Example:
1. Initialize the theme of Origin object, which is _1st column_ of the _1st worksheet_ in a workbook named _Book1_
```
import PyOrigin as po
import pox.theme

col = po.Pages('Book1')[0][0]
t = pox.theme.Theme(col)
```
2. Inspect the available settings if you are not certain about them
```
>>> t.Root
{'InternalData': '6',
 'Data': '\x01ƀ\x08',
 'NumericDisplay': '0',
 'Formula': '',
 'LongName': '',
 'Format': '6',
 'Display': '0',
 'Width': '6.7000000000000002',
 'CustomFormat': '',
 'Comment': '',
 'Digits': '0',
 'ShortName': 'A',
 'Unit': '',
 'DisplayAsText': '0',
 'Designation': '0'}
```
3. To apply new styles to the Origin object, you can either
  * change settings one by one and apply() at the end to update
```
t.Root.Width = 18
t.Root.LongName = 'Height from Ground'
t.apply()
```
  * assign settings to _Root_
```
t.Root = {'Width':18, 'LongName':'Height from Ground'}
```
## High-Level
