##############################################################################
CHANGE LOG
Author: Jaerock Kwon
------------------------------------------------------------------------------
12/01/2017: version 1.0.0 starts!!
12/01/2017

1. Change robot name: mirvehicle

2. mirvehicle_control.yaml
  Change joint1_ --> back_left_
  Change joint2_ --> back_right_

3. cont.cc at src/mirvehicle/src
  Change 'catvehicle/cont.hh' --> 'mirvehicle/cont.hh'

4. objectStopper.cc at src/mirvehicle/src
  Change topic names has 'c','a','t' to 'm','i','r'.

5. Create 'Scripts' folder and move all .py to it.

6. Change 'catvehicle' to 'mirvehicle' in all the .py files.

7. 'cmdvel2gazebo.py'
  Change joint1_ --> back_left_
  Change joint2_ --> back_right_


------------------------------------------------------------------------------
12/02/2017: Redesign with the structure of ROBOT_description and ROBOT_gazebo


------------------------------------------------------------------------------


