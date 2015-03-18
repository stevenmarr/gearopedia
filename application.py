from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug import secure_filename

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
	category = session.query(GearCategories).filter_by(id = category_id).one()
	if request.method == 'POST':
		models = session.query(GearModels).filter_by(category=category).all()
		for model in models:
			session.delete(model)
			session.commit()
		session.delete(category)
		session.commit()
		flash('Category %s deleted'% category.name)
		return redirect(url_for('DefaultGearCategories'))
	else:
		return render_template('delete_category.html', category=category)

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
		file = request.files['file']
		if file:
			
			filename = secure_filename(file.filename)
			#new_model.manual = file.read()
			file.save(new_model.manual, filename)
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
	model = session.query(GearModels).filter_by(id=model_id).one()
	if request.method == 'POST':
		form = AddModelForm(request.form)
		form.populate_obj(model)
		session.add(model)
		session.commit()
		flash('Model %s edited' % model.name)
		return redirect(url_for('ViewModels', category_id=model.category_id))
	else:
		form = AddModelForm(obj = model)
		return render_template('edit_model.html', 
								form=form, 
								model=model,
								category = model.category)

@app.route('/delete_model/<int:model_id>/', methods=['GET','POST'])
def DeleteModel(model_id):
	model = session.query(GearModels).filter_by(id=model_id).one()
	if request.method == 'POST':
		session.delete(model)
		session.commit()
		flash('Model %s deleted'% model.name)
		return redirect(url_for('ViewModels', category_id=model.category_id))
	else:
		return render_template('delete_model.html', model=model)	
@app.route('/json/')
def JSON():
	
if __name__ == '__main__':
	app.secret_key = 'super-secret-key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)
