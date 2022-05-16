# openxtasks

# PREQUISITES:

You need to install required libraries via:
```
pip3 install -r requirements.txt
```
# USAGE:

There are 4 scripts total in the project:

- `test_unit.py` - unit test made with pytest that tests both tasks, to run it via cmd:
```
python3 -m pytest test_unit.py
```
- `task1.py` - task1 from the pdf file with tasks, it downloads the sellers data and shows it in gui
- `task1_view.py` - a subscript used in `task1.py` via importing to get the view of downloaded data, can be used independendtly using pre-downloaded data included in github, run it via cmd:
```
python3 task1_view.py
```
- `find-available-slot.py` - second task from pdf, it shows the soonest available date from the list in given directory for a given amount of time for a given amount of people, to run it via cmd:
```
python3 find-available-slot.py [--calendars DIRECTORY] [--duration-in-minutes MINUTES ] [--minimum_people MINIMUM_PEOPLE] 
```
all of the args are required and they serve:

  - `calendars-teams` `--DIRECTORY`specifies directory with calendars in .txt file
  - `duration-in-minutes` `--MINUTES` specifies how many free minutes is script looking for
  - `minimum_people` `--MINIMUM_PEOPLE` specifies the least amount of available people the script will look for

 ###### Filip Zygmuntowicz 2022
