from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, CatalogItem
app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories/')
def homepage():
    categories = session.query(Category).all()
    items = session.query(CatalogItem).order_by(CatalogItem.id.desc()).limit(3)
    return render_template('homepage.html', categories=categories, items=items)

@app.route('/categories/new/')
def createCategory():
    return 'create a new category'

@app.route('/categories/<int:category_id>/update/', methods=['GET', 'POST'])
def updateCategory(category_id):
    categories = session.query(Category)
    selected_category = categories.filter_by(id=category_id)
    if not selected_category.one_or_none():
        abort(404)
    elif request.method == 'POST':
        category = request.form.get('category') or selected_category.one_or_none().category
        selected_category.update({'category': category})
        session.commit()
        return redirect(url_for('showCategory', category_id=selected_category.one_or_none().id))
    else:
        return render_template('update-category.html', categories=categories, selected_category=selected_category.one_or_none())

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categories = session.query(Category)
    selected_category = categories.filter_by(id=category_id)
    if not selected_category.one_or_none():
        abort(404)
    elif request.method == 'POST':
        category_items = session.query(CatalogItem).filter_by(id=category_id).all()
        if len(category_items):
            abort(400)
        selected_category.delete()
        session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('delete-category.html', categories=categories.all(), selected_category=selected_category.one_or_none())

@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showCategory(category_id):
    categories = session.query(Category)
    category = categories.filter_by(id=category_id).one_or_none()
    if not category:
        abort(404)
    category_items = session.query(CatalogItem).filter_by(category=category).all()
    return render_template('category-items.html', categories=categories.all(), selected_category=category, category_items=category_items)

@app.route('/items/new/', methods=['GET', 'POST'])
def createItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        item_name = request.form.get('item_name') or abort(400)
        description = request.form.get('description')
        category = request.form.get('category') or abort(400)
        category_id = session.query(Category.id).filter_by(category=category).one_or_none()
        if not category_id:
            new_category = Category(category=category)
            session.add(new_category)
            session.commit()
            category_id = new_category.id
        new_item = CatalogItem(item_name=item_name, description=description, category_id=category_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('showItem', item_id=new_item.id))
    else:
        return render_template('new-item.html', categories=categories)

@app.route('/items/<int:item_id>/update/', methods=['GET', 'POST'])
def updateItem(item_id):
    categories = session.query(Category).all()
    selected_item = session.query(CatalogItem).filter_by(id=item_id)
    if not selected_item.one_or_none():
        abort(404)
    elif request.method == 'POST':
        item_name = request.form.get('item_name') or selected_item.one_or_none().item_name
        description = request.form.get('description')
        category = request.form.get('category') or selected_item.one_or_none().category
        category_id = session.query(Category.id).filter_by(category=category).one_or_none()
        if not category_id:
            new_category = Category(category=category)
            session.add(new_category)
            session.commit()
            category_id = new_category.id
        selected_item.update({'item_name': item_name, 'description': description, 'category_id': category_id})
        session.commit()
        return redirect(url_for('showItem', item_id=selected_item.one_or_none().id))
    else:
        return render_template('update-item.html', categories=categories, selected_item=selected_item.one_or_none())

@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    categories = session.query(Category).all()
    selected_item = session.query(CatalogItem).filter_by(id=item_id)
    if not selected_item.one_or_none():
        abort(404)
    elif request.method == 'POST':
        selected_item.delete()
        session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('delete-item.html', categories=categories, selected_item=selected_item.one_or_none())

@app.route('/items/<int:item_id>/')
def showItem(item_id):
    categories = session.query(Category).all()
    selected_item = session.query(CatalogItem).filter_by(id=item_id).one_or_none()
    if not selected_item:
        abort(404)
    return render_template('show-item.html', categories=categories, selected_item=selected_item)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)