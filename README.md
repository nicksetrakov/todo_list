# todo_list

## Installation
Python3 must be already installed

```shell
git clone https://github.com/nicksetrakov/todo_list
cd todo_list
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pthon manage.py migrate
python manage.py populate_fake_data
python manage.py runserver
```