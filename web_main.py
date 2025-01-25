from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask.views import MethodView
from flask_material import Material
from wtforms import Form, SubmitField, StringField
from wtforms.fields.simple import PasswordField, EmailField

from main import User
from Event_informations.event import Events
from ticket import Ticket
from seat import Seat
from card import Card

app = Flask(__name__)
Material(app)


class HomePage(MethodView):
    def get(self):
        return render_template("home.html")


class AboutPage(MethodView):

    def get(self):
        return render_template("about.html")


class UpcomingEvents(MethodView):

    def get(self):
        event_bill = Events(artist_name="Bill Frisell", id=1)
        event_cinematic = Events(artist_name="Cinematic Orchestra", id=5)
        infob = event_bill.get_bio(remove_name="Bill+Frisell")
        infoc = event_cinematic.get_bio(remove_name="+noredirect/Cinematic+Orchestra")

        return render_template("upcoming.html", infob=infob, infoc=infoc)


class SignUpForm(Form):
    name = StringField(label="First name ", default='')
    surname = StringField(label="Last Name", default='')
    password = PasswordField(label="Password")
    confirm_password = PasswordField(label="Confirm Password")
    email = EmailField(label="Email")
    button = SubmitField(label="sign up")


class SignInForm(Form):
    password = PasswordField(label="Password")
    email = EmailField(label="Email")


class VotePage(MethodView):

    def get(self):
        sign_inform = SignInForm()
        event_bruno = Events(artist_name="Bruno Mars", id=3)
        info_bruno = event_bruno.get_bio(remove_name="Bruno+Mars")
        votes_bruno = event_bruno.get_vote()
        event_masego = Events(artist_name="Masego", id=2)
        info_masego = event_masego.get_bio(remove_name="masego")
        votes_masego = event_masego.get_vote()
        event_alfa = Events(artist_name="Alfa Mist", id=4)
        info_alfa = event_alfa.get_bio("Alfa+Mist")
        votes_alfa = event_alfa.get_vote()

        return render_template("vote.html", sign_inform=sign_inform,
                               info_bruno=info_bruno
                               , votes_bruno=votes_bruno,
                               info_masego=info_masego,
                               votes_masego=votes_masego,
                               info_alfa=info_alfa,
                               votes_alfa=votes_alfa)

    def post(self):
        sign_inform = SignInForm(request.form)
        password = sign_inform.password.data
        email = sign_inform.email.data

        action = request.form.get("action")
        # data = request.form.get('data')
        event_alfa = Events(artist_name="Alfa Mist", id=4)
        event_bruno = Events(artist_name="Bruno Mars", id=3)
        event_masego = Events(artist_name="Masego", id=2)

        user = User(name="", surname="", email=email, password=password)
        if not user.check_db():
            message = "You have to make a profile first!Then come back and complete your voting!"

        else:
            if user.check_db()[0][2] == 0:
                if action == "add_alfa":

                    event_alfa.add_vote()
                elif action == "add_bruno":
                    event_bruno.add_vote()
                else:
                    event_masego.add_vote()

                user.votes_kill()
                message = "Great !We hope you spent your vote wisely"

            else:
                message = "You already used your vote!!"

        info_bruno = event_bruno.get_bio(remove_name="Bruno+Mars")
        votes_bruno = event_bruno.get_vote()
        info_masego = event_masego.get_bio(remove_name="masego")
        votes_masego = event_masego.get_vote()
        info_alfa = event_alfa.get_bio("Alfa+Mist")
        votes_alfa = event_alfa.get_vote()
        return render_template("vote.html", sign_inform=SignInForm(),
                               info_bruno=info_bruno
                               , votes_bruno=votes_bruno,
                               info_masego=info_masego,
                               votes_masego=votes_masego,
                               info_alfa=info_alfa,
                               votes_alfa=votes_alfa, message=message, result=True)


class CreateUser(MethodView):

    def get(self):
        sign_up_form = SignUpForm()

        return render_template("user.html", signupform=sign_up_form)

    def post(self):
        signupform = SignUpForm(request.form)
        user = User(name=signupform.name.data, surname=signupform.surname.data, email=signupform.email.data,
                    password=signupform.password.data)
        confirm_password = signupform.confirm_password.data
        if user.password != confirm_password:
            message = "Password confirmation failed. Please make sure both fields match."
            return render_template("user.html", result=True, signupform=SignUpForm(), message=message)

        else:
            signupform.email.data = ''

            print(user.password, user.email, signupform.email.data, signupform.password.data)
            message = user.make_profile()

            return render_template("user.html", result=True, signupform=SignUpForm(), message=message)


class BuyTicketForm(Form):
    name = StringField(label="First name ")
    surname = StringField(label="Last name")
    email = EmailField(label="Email")
    seat_id = StringField(label="Choose your Seat")
    card_holder_name = StringField(label="First name ")
    card_holder_surname = StringField(label="Last name")
    card_type = StringField(label="Card type")
    card_number = StringField(label="Card number")
    card_cvc = StringField(label="CVC")


class BillFrisellTicket(MethodView):
    def get(self):
        ticket_form = BuyTicketForm()
        return render_template("billfrisell_ticket.html", ticketform=ticket_form)

    def post(self):
        ticketform = BuyTicketForm(request.form)
        user = User(name=ticketform.name.data, surname=ticketform.surname.data, email=ticketform.email.data)
        ticket = Ticket(name=user.name, surname=user.surname, email=user.email, artist_name="Bill Frisell")
        seat = Seat(seat_id=ticketform.seat_id.data)
        card = Card(holder_name=ticketform.card_holder_name.data, holder_surname=ticketform.card_holder_surname.data,
                    card_type=ticketform.card_type.data, number=ticketform.card_number.data,
                    cvc=ticketform.card_cvc.data)
        message = user.buy(seat=seat, card=card)
        if message == "The purchase is completed ":
            ticket.insert_ticket_data()
            ticket.make_ticket()
            event = Events(artist_name=ticket.artist_name, id=1)
            ticket.send_ticket(event=event)

        return render_template("billfrisell_ticket.html", ticketform=BuyTicketForm(), result=True, message=message)


class CinOrcTicket(MethodView):
    def get(self):
        ticket_form = BuyTicketForm()
        return render_template("cinematic_orchestra.html", ticketform=ticket_form)

    def post(self):
        ticketform = BuyTicketForm(request.form)
        user = User(name=ticketform.name.data, surname=ticketform.surname.data, email=ticketform.email.data)
        ticket = Ticket(name=user.name, surname=user.surname, email=user.email, artist_name="Cinematic Orchestra")
        seat = Seat(seat_id=ticketform.seat_id.data)
        card = Card(holder_name=ticketform.card_holder_name.data, holder_surname=ticketform.card_holder_surname.data,
                    card_type=ticketform.card_type.data, number=ticketform.card_number.data,
                    cvc=ticketform.card_cvc.data)
        message = user.buy(seat=seat, card=card)
        if message == "The purchase is completed ":
            ticket.insert_ticket_data()
            ticket.make_ticket()
            event = Events(artist_name=ticket.artist_name, id=5)
            ticket.send_ticket(event=event)

        return render_template("cinematic_orchestra.html", ticketform=BuyTicketForm(), result=True, message=message)


if __name__ == "__main__":
    app.add_url_rule('/', view_func=HomePage.as_view('home'))
    app.add_url_rule('/about', view_func=AboutPage.as_view('about'))
    app.add_url_rule('/upcoming', view_func=UpcomingEvents.as_view('upcoming'))
    app.add_url_rule('/vote', view_func=VotePage.as_view('vote'))
    app.add_url_rule('/user', view_func=CreateUser.as_view('user'))
    app.add_url_rule('/billfrisell_ticket', view_func=BillFrisellTicket.as_view('bfticket'))
    app.add_url_rule('/cinematic_orchestra_ticket', view_func=CinOrcTicket.as_view('coticket'))
    app.run(debug=True)
