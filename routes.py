from flask import Flask, request, jsonify
from models import db, User, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

def setup_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to FlexDrive API!"})

    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        new_user = User(name=data["name"], email=data["email"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        if user and check_password_hash(user.password, data["password"]):
            login_user(user)
            return jsonify({"message": "Login successful"})
        return jsonify({"message": "Invalid credentials"}), 401

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully"})

    @app.route("/book_taxi", methods=["POST"])
    @login_required
    def book_taxi():
        data = request.json
        new_booking = Booking(
            user_id=current_user.id,
            pickup_location=data["pickup"],
            dropoff_location=data["dropoff"],
            fare=data["fare"],
            status="pending"
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Taxi booked successfully", "booking_id": new_booking.id})

    @app.route("/my_bookings", methods=["GET"])
    @login_required
    def my_bookings():
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return jsonify([{"id": b.id, "pickup": b.pickup_location, "dropoff": b.dropoff_location, "fare": b.fare, "status": b.status} for b in bookings])

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        user_message = data.get("message").lower()

        responses = {
            "hello": "Hi there! How can I assist you?",
            "how to book a taxi": "You can book a taxi by entering your pickup and drop-off locations and clicking 'Book Now'.",
            "thank you": "You're welcome! Have a great day!",
        }

        bot_response = responses.get(user_message, "Sorry, I didn't understand that.")
        return jsonify({"response": bot_response})
