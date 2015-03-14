from flask import Flask, render_template, url_for, request, redirect, flash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import GearCategories, GearModels, Base

from forms import AddCategoryForm, AddModelForm

app = Flask(__name__)
engine = create_engine('sqlite:///gear_wiki.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def DefaultGearCategories():
	categories = session.query(GearCategories).all()
	return render_template('default.html', categories=categories)

@app.route('/add_category/', methods=['GET','POST'])
def AddGearCategory():
	if request.method == 'POST':
		form = AddCategoryForm(request.form)
		if not form.validate():
			return render_template('add_category.html', form=form)
		new_category = GearCategories(name = form.name.data)
		session.add(new_category)
		session.commit()
		flash('New category added')
		return redirect(url_for('DefaultGearCategories'))
	else:
		form = AddCategoryForm()
		return render_template('add_category.html', form=form)

@app.route('/delete_category/<int:category_id>/', methods=['GET','POST'])
def DeleteGearCategory(category_id):
	pass

@app.route('/view_items/<int:category_id>/')
def ViewModels(category_id):
	models = session.query(GearModels).filter_by(category_id=category_id).all()
	return render_template('view_models.html', 
							models=models,
							category_id=category_id)

@app.route('/add_item/<int:category_id>/', methods=['GET','POST'])
def AddModel(category_id):
	category = session.query(GearCategories).filter_by(id=category_id).one()
	if request.method == 'POST':
		form = AddModelForm(request.form)
		if not form.validate():
			return render_template('add_model.html', form=form, category=category)
		new_model = GearModels()
		form.populate_obj(new_model)
		new_model.category = category
		session.add(new_model)
		session.commit()
		flash('New model created')
		return redirect(url_for('DefaultGearCategories'))
	else:
		form = AddModelForm()
		
		return render_template('add_model.html', form=form, category=category)
	pass

@app.route('/edit_model/<int:model_id>/', methods=['GET','POST'])
def EditModel(model_id):
	pass

@app.route('/delete_model/<int:model_id>/', methods=['GET','POST'])
def DeleteModel(model_id):
	pass

if __name__ == '__main__':
	app.secret_key = 'super-secret-key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)
