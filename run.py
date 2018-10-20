from werkzeug.serving import WSGIRequestHandler

if __name__ == '__main__':
	from app import create_app
	app = create_app()

	WSGIRequestHandler.protocol_version = "HTTP/1.1"
	app.run(host='0.0.0.0', port=25565, debug=True)
