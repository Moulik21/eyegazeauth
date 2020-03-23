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

  Week ending Friday, March 6, 2020
---------------------------------------
  - Added 4-point picture point selection functionality for user's custom images. - Keenan Kua
  - Integrating the new UI with the PAM, there were issues due to GTK not allowing GUI applications to run with setuid.  - Calin Chirvase
  - Adressed common false-positives associated with face and eye detection. -Daniel Bishara
  - Implemented pupil detection and tracking using blob detection algorithm. Has a threshold tuning slider to set blob threshold on the fly. Need to fine tune threhold tetsing to get more consistent results under various lighting conditions. - Moulik Gaglani
  - Integrated 4-point picture point selection and 9-grid set password into one program. Created authentication side for 9-grid set password. - Jiyu Liu
  - Continued to work on translating research paper's method on tracking pupil. Overall progression was slow, but found potential alternative methods (Blob detection).
  Will continue to translate the research paper to compare for acurracy.
  Assisted Moulik with implementing blob detection - Paul

  Week ending Friday, March 13, 2020
---------------------------------------
  - Added sizers to password setup UI for compatability between Linux and Windows. - Keenan Kua
  - Implemented PAM support for wx python program; child process will now forefit its root privledges. - Daniel Bishara
  - Created setup.sh, ideally this will eventually be a one-off script that will perform all necessary setup for environment such as moving files into the correct locations, downloading necessary packages, ensuring correct file permissions etc. I plan to make this more sophisticated next week - Daniel Bishara
  - Add sizers for login and add basic picture points login with grid logic (no hashing yet) - Keenan Kua
  - Work on creating backgground process to handle root privilages, a new issue is that we can not take advantage of the PassLib library in C, must use another library like OpenSSL. Another concern is how to safely transfer password hash between Python script and C PAM. - Calin Chirvase
  - Added password hashing to picture points login and login page opens in one window instead of multiple windows - Jiyu Liu
 
 Week ending Friday, March 20, 2020
---------------------------------------
- Small Update to setup to make pamuser owner of the passwords.txt - Daniel Bishara
- Worked on improving accuracy of eye tracking, and also worked on gaze direction - Daniel and Paul
- Add progress dots feedback to picture points select login screen via custom title bar - Keenan Kua
- Pupil detection more consistent using old keypoints and old area of the pupil detected in the last frame. Only works for 1 of the eyes, need to differeniate different eyes and make pupil consistent for both eyes - Moulik Gaglani

 Week ending Friday, March 27, 2020
---------------------------------------
- Add login progress dots for 9-grid - Keenan Kua
- Eye tracking stuff: Added forward direction(now all 9 grids are accounted for). Keep track of past frames and only return a result when most frames agree.  Daniel Bishara
