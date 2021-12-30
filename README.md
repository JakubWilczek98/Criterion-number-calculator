The program is intended for calculation of criterial number like:
* Reynolds number, 
* Nusselt number,
* Grashof number,
* Prandtl number.

Program operation is based on the 5th chepter of Polish book WIESŁAW PUDLIK - EXCHANGE AND HEAT EXCHANGERS (ang. WIESŁAW PUDLIK - EXCHANGE AND HEAT EXCHANGERS) and thermodynamic tables for water and dry air. Program is designed to solve four different flow issues (cases 1-4).

The executive part of application is created using python. Data base is created using mySQL. Web interface is created using Flask. 

Files:
* Main file (main.py)
* Cases files: 
    * case_1.py
    * case_2.py
    * case_3.py
    * case_4.py
* Data base creator file (data_base_create.py) 
* File for intepolation of datasets. (data_interpolation.py)
* Thermodynamic tables,
    * dry_air.csv - basic table,
    * dry_air_interpolated.csv - interpolated table,
    * water.csv - basic table,
    * water_interpolated.csv - interpolated table.
* In templates folder are located all html files.

