$ export FLASK_CONFIG=development
$ export FLASK_APP=run.py
$ flask run
 * Serving Flask app "run"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


 $ flask db init
 $ flask db migrate
 $ flask db upgrade


 $ flask shell
>>> from app.models import Employee
>>> from app import db
>>> admin = Employee(email="admin@admin.com",username="admin",password="admin2017",is_admin=True)
>>> db.session.add(admin)
>>> db.session.commit()