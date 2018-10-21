from werkzeug.serving import WSGIRequestHandler


def upload_static():
	import flask_s3
	from app import create_app
	app = create_app()
	flask_s3.create_all(app)


def run_app():
	from app import create_app

	app = create_app()

	WSGIRequestHandler.protocol_version = "HTTP/1.1"
	app.run(host='0.0.0.0', port=25565, debug=True)


if __name__ == '__main__':
	run_app()
	#upload_static()
