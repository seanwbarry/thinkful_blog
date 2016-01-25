from flask import render_template, request, redirect, url_for, Markup, flash

from flask.ext.login import login_user, login_required, current_user, logout_user

from werkzeug.security import check_password_hash

from blog import app
from .database import session, Entry, User

@app.route("/", methods=["GET", "POST"])
@app.route("/page/<int:page>", methods=["GET", "POST"])
def entries(page=1, paginate_value=10):
    """if request.form['paginate_value']:
        PAGINATE_BY=request.form
    if PAGINATE_BY:
        PAGINATE_BY=PAGINATE_BY
    print(PAGINATE_BY)
    """
    """
    if request.method == 'GET':
        print('in the get')
        PAGINATE_BY=10
    elif request.method == 'POST':
        print('in the post')
        test = request.form['pageinate_value']
        test = int(test)
        PAGINATE_BY=test
    """
    
    PAGINATE_BY = paginate_value
    
    print('in the get')
    PAGINATE_BY = 10
    test = request.args.get('paginate_value')
    if test:
        test = int(test)
        PAGINATE_BY=test

    page_index = page - 1

    print('being executed')

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count-1) / PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
                            entries = entries,
                            has_next = has_next,
                            has_prev = has_prev,
                            page = page,
                            total_pages = total_pages,
                            test_html = '<strong>&the html string</strong>'
    )

"""
@app.route("/page/<int:page>", methods=["POST"])
def entries_2(page):
    #PAGINATE_BY=request.args.get()
    test = request.form['paginate_value']
    
    print('being executed 2')
    print(test)
    return render_template("entries.html")
"""


@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_edit_entry.html", 
                            page_title="Add Entry",
                            show_delete=False)
    
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<int:id>")
def view_single_entry(id):
    fields = session.query(Entry)
    print(fields)
    entry = session.query(Entry).get(id)
    print(entry)
    print('asdf')
    
    return render_template("entry.html",
                            entry = entry
    )

@app.route("/entry/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    if entry.author==current_user:
        entry_title = entry.title
        entry_content = entry.content
        return render_template("add_edit_entry.html", 
                                page_title="Edit Entry",
                                entry_title=entry_title,
                                entry_content = entry_content,
                                entry_id = entry.id,
                                show_delete=True)
    else:
        flash("wrong user!","danger")
        return redirect(url_for("entries"))
    
@app.route("/entry/<int:id>/edit", methods=["POST"])
@login_required
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    if entry.author==current_user:
        entry.title=request.form["title"]
        entry.content=request.form["content"]
        session.commit()
        return redirect(url_for("entries"))
    else:
        flash("wrong user!","danger")
        return redirect(url_for("entries"))
        
@app.route("/entry/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry_post(id):
    entry = session.query(Entry).get(id)
    if entry.author==current_user:
        session.delete(entry)
        session.commit()
        return redirect(url_for("entries"))
    else:
        flash("wrong user!","danger")
        return redirect(url_for("entries"))
        
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
        
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("entries"))