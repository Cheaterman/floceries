from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xa0h\xec%I7\x80q\xe2T\xa4@\xdb\xa5Yl\xec\x18\xc2\x9f^\\t>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///floceries.db'
db = SQLAlchemy(app)


class GroceryItem(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/item/add', methods=('GET', 'POST'))
def item_add():
    if request.method == 'POST':
        db.session.add(GroceryItem(name=request.form['name']))
        db.session.commit()
        flash('The item "{.form[name]}" has been added.'.format(request))
        return redirect(url_for('item_list'))

    return render_template('item_add.html')


@app.route('/item/list')
def item_list():
    return render_template('item_list.html', items=GroceryItem.query)


@app.route('/api/item')
def api_item_list():
    return jsonify([
        {'id': item.id, 'name': item.name}
        for item in GroceryItem.query
    ])


@app.route('/api/item/add', methods=['POST'])
def api_item_add():
    db.session.add(GroceryItem(name=request.json['name']))
    db.session.commit()
    return ''


@app.route('/api/item/delete', methods=['POST'])
def api_item_delete():
    db.session.delete(GroceryItem.query.get(request.json['id']))
    db.session.commit()
    return ''


@app.route('/item/delete/<int:id>')
def item_delete(id):
    item = GroceryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('The item "{.name}" has been removed.'.format(item))

    return redirect(url_for('item_list'))
