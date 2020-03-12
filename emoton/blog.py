from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from emoton.auth import login_required
from emoton.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, val, created, author_id, username'
        ' FROM tone p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        val = request.form['toneValue']
        print(val)
        error = None

        if not val:
            error = 'Value is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tone (val, author_id)'
                ' VALUES (?, ?)',
                (val, g.user['id'])
            )
            db.commit()
            #return redirect(url_for('blog.index'))
            return redirect(request.referrer) 

    #return render_template('blog/create.html')
    return redirect(request.referrer) 