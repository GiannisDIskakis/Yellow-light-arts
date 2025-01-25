import sqlite3


class User:
    database = "data.db"

    def __init__(self, name, surname, email, password=""):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def make_profile(self):

        try:
            cnx = sqlite3.connect(self.database)
            cnx.execute("""
                                   INSERT INTO "user"("name","surname","email","password") VALUES (?,?,?,?)
                                   """, [self.name, self.surname, self.email, self.password])
            cnx.commit()
            cnx.close()
            return "Your profile is created successfully"
        except:
            return "This email is already registered.Please use a different email."

    def check_db(self):
        cnx = sqlite3.connect(database=self.database)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "password","email","vote" FROM "user" WHERE "password"=? AND "email"=? 
        """, [self.password, self.email])
        result = cur.fetchall()
        cnx.close()
        return result

    def vote(self, event):
        cnx = sqlite3.connect(self.database)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "id" FROM "event" WHERE "event_name"=?
        """, [event.artist_name])

        id = cur.fetchall()[0][0]
        cnx.close()
        event.add_vote(id=id)

    def votes_kill(self):
        cnx = sqlite3.connect(database=self.database)
        cnx.execute("""
        UPDATE "user" SET "vote" =1 WHERE "email"=? AND "password"=?
        """, [self.email, self.password])
        cnx.commit()
        cnx.close()

    def buy(self, card, seat):

        """ result is going to hold a string or none :
        1. If the information that user provides are not right
        the str is :
              "Please type again the information about your card, maybe there is something wrong"
        2. If the balance is not enough the str is :
              "Your balance it's not enough to continue purchase"
        3.If the information is ok and the balance is enough then the purchase is going
         to be complete and result is going to be equal to none
        """
        if seat.available == 0:
            result = card.set_balance(ticket_price=seat.price)

            if not result:
                seat.occupy()

                return "The purchase is completed "
            else:
                return result
        else:
            return f"Seat {seat.seat_id} is reserved for someone else. Try another!"


# ticket = Ticket(name="Ioanna", surname="Zouli", email="some@wow.gr")
# ticket.make_ticket("Portishead")


if __name__ == "__main__":
    user = User(name="JOHN", surname="DISKAKIS", email="stauroskapridakis@hotmail.com", password="apassword")
    # ticket = Ticket(name=user.name, surname=user.surname, email=user.email, artist_name="Bill Frisell")
    # seat = seat.Seat(seat_id="A8")
    # card = Card(holder_name="JOHN", holder_surname="DISKAKIS", card_type="Mastercard", number="12345678", cvc="123")
    # result = user.buy(seat=seat, card=card)
    # if result == "The purchase is completed ":
    #     ticket.insert_ticket_data()
    #     ticket.make_ticket()
    #     event = Events(artist_name=ticket.artist_name, id=1)
    #     ticket.send_ticket(event=event)
    if user.check_db() == []:
        print("Make a profile first")

    else:
        if user.check_db()[0][2] == 0:
            for i in user.check_db()[0]:
                user.votes_kill()
            print("Great !Spend your vote wisely")

        else:
            print("You already used your vote")

    print(user.check_db())
