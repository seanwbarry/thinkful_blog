import os
from flask.ext.script import Manager

from blog import app
from blog.database import session, Entry

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    content = """somesome wordssome wordssome wordssome wordssome words words"""

    for i in range(25):
        entry = Entry(
            title="Test Entry #{}".format(i),
            content=content
        )
        session.add(entry)
    session.commit()


    
    

    
if __name__ == "__main__":
    manager.run()
    
