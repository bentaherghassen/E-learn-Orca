from app import app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the database file if it doesn't exist
    app.run(debug=True)


#if __name__ == "__main__":
    #app.run()