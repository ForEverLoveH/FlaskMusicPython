
from flask_script import Manager
from utils.fuctions import create_app

from flask_migrate import Migrate,MigrateCommand

from myapp.models import db,Music,User
app=create_app()
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)



if __name__=='__main__':  # 程序运行接口
    manager.run()