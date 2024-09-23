from Website import create_app

app = create_app()

if __name__ == '__main__':
    #run a flask application
    app.run(debug=True)