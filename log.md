# Place to keep weekly updates to this project #
<!--
Template
--------------------------------------------------------------------------
TYPE     : BUG/FEATURE
NAME     : Circle drawing is broken
OWNER    : Keenan
PRIORITY : High
ESTIMATE : 1 hour
ISSUE    : The first click should specify the center of the circle, with
           a drag for the radius. This is not the case in the current
           implementation.
--------------------------------------------------------------------------
-->
Week ending Friday, February 7, 2020
---------------------------------------
  - Developed concept art for UI interface - Keenan Kua
  - Created pygame button for testing sudo authentication - Jiyu Liu
  - Developed PAM module for sudo authentication - Calin Chirvase, Daniel Bishara

Week ending Friday, February 14, 2020
---------------------------------------
  - Created picture points password form, including preset image choices and ability to choose a custom image. - Keenan Kua
  - Fixed PAM exploit, work on implementing login authentication instead of sudo. (Encountered problems on login implementation) - Daniel Bishara, Calin Chirvase
  
  Week ending Friday, February 29, 2020
---------------------------------------
  - Added PAM to the login page. Also fixed a known bug where forked processes always return -1 in pam log in pages - Daniel Bishara
  - Added 4-point selection feature for the sample images. Has popup instructions, the ability to redo, popup confirmation, and graphical indication of selected points. - Keenan Kua
  - Added password hashing and storing (text password) and a login page that checks the hash with the inputed password. Encountered issues when trying to combine features made by others into one complete program (whether it was different syntax, different python version, etc.). - Calin Chirvase
  - Implemented password setting user interface using the 9 grid in a picture pin interface. Also collected and organized sample pictures to use for the grid of 9. - Jiyu Liu
