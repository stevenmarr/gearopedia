from gearopedia import app

if __name__ == "__main__":
	app.config.from_object('config')
	app.run(host='0.0.0.0', port=8080, debug=True)
