from dbsetup import db, app
import templates


if __name__ == '__main__':
    db.create_all()
    app.run()
