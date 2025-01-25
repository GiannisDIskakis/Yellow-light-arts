import os
import random
import string
import webbrowser
import yagmail
import sqlite3
from dotenv import load_dotenv
from fpdf import FPDF

from Event_informations.event import Events


class Ticket:
    path = "C:\\Users\\d_jas\\PycharmProjects\\Booking_vote_concert\\Event_informations"
    database = "data.db"

    def __init__(self, name, surname, email, artist_name):
        self.name = name
        self.surname = surname
        self.email = email
        self.artist_name = artist_name
        self.ticket_id = self.ticket_id()

    def make_ticket(self):
        """
        makes a ticket pdf with a ticket number 1 to 200
        and a random ticket_id.Creates a pdf that is called
        ex: #number_owner_band
        """
        # ticket_id = self.ticket_id()
        ticket_num = self.ticket_num()
        pdf = FPDF(orientation="P", unit="pt", format=(500, 300))
        pdf.set_text_color(r=255, b=255, g=255)
        pdf.add_page()
        pdf.image(f"{self.path}\\{self.artist_name}.jpeg", x=0, y=0, w=500, h=300)

        pdf.set_font(family="Times", size=30, style="B")
        pdf.cell(w=300, h=20, txt="", border=0)
        pdf.cell(w=150, h=20, txt="TICKET", fill=True, border=0, align="C", ln=1)
        pdf.cell(w=0, h=20, txt="", border=0, ln=1)

        pdf.set_font(family="Times", size=36, style="B")
        pdf.cell(w=250, h=40, txt=f"{self.artist_name}", fill=False, border=0, align="C", ln=1)
        pdf.cell(w=0, h=20, txt="", border=0, ln=1)
        pdf.cell(w=0, h=20, txt="", border=0, ln=1)
        pdf.cell(w=0, h=20, txt="", border=0, ln=1)
        pdf.cell(w=0, h=20, txt="", border=0, ln=1)

        pdf.set_font(family="Times", size=16, style="I")
        pdf.cell(w=80, h=20, txt="Ticket id :  ", fill=False, border=0, align="C", )
        pdf.cell(w=100, h=20, txt=f"{self.ticket_id}", fill=True, border=1, align="C", ln=1)

        pdf.set_font(family="Times", size=12, style="B")

        pdf.cell(w=100, h=15, txt=f"Ticket number ", border=0, fill=False)
        pdf.cell(w=100, h=15, txt=f"#{ticket_num}", border=0, fill=True)
        pdf.cell(w=100, h=15, txt="SwampArts", fill=False, border=0, align="C", ln=2)
        pdf.cell(w=200, h=15, txt=f"Address Athens  Main Avenue 33  17891", border=0, align="C", ln=1)

        pdf.output(f"{self.surname}_{self.artist_name}.pdf")
        webbrowser.open(f"{self.surname}_{self.artist_name}.pdf")

    @staticmethod
    def ticket_id():
        text = string.ascii_uppercase + string.ascii_lowercase + string.digits

        x = ""
        for i in range(8):
            x = x + random.choice(text)

        return x

    def ticket_num(self):
        cnx = sqlite3.connect(database=self.database)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "id" FROM "ticket" WHERE "buyer"=? and "ticket_id"=?
        """, [f"{self.name} {self.surname}",self.ticket_id])
        result = cur.fetchall()[0][0]
        return result

    def insert_ticket_data(self):
        cnx = sqlite3.connect(database=self.database)
        cnx.execute("""
        INSERT INTO "ticket"("event","buyer","ticket_id") VALUES(?,?,?)
        """, [self.artist_name, f"{self.name} {self.surname}", self.ticket_id])
        cnx.commit()
        cnx.close()

    def send_ticket(self, event):
        body = (f"Hi {self.name} {self.surname} find your ticket in this email!!\n"
                f"Welcome to {self.artist_name} concert at Yellow Light Arts!\n\n"
                f"We’re thrilled to have you join us for {self.artist_name} concert on {event.get_date()} at {event.get_time()}!\n"
                " Get ready for an unforgettable night of music, art, "
                "and great vibes in the heart of Yellow Light Arts.\n"
                "Here’s what you need to know to make the most of your experience:\n"
                "Location: Athens  Main Avenue 33  17891 \n"
                f"Doors Open: 20:00 Show Starts: {event.get_time()}\n\n\n"
                "Helpful Tips:\n"
                "• Arrive early to grab a great spot!\n"
                "• Food and drinks will be available for purchase.\n"
                "• Have your ticket ready (printed or on your phone) for smooth entry.\n\n"
                "We can’t wait to see you there and share a night of incredible performances. "
                "If you have any questions before the event, "
                "feel free to reach out to us at [Yellow Light Arts Contact "
                "Email] or visit our FAQ [Link to FAQ].\n"
                "Thank you for choosing Yellow Light. Get ready for a night to remember!\n\n"
                "See you soon,The Yellow Light Arts Team[www.yellowlight.com]")
        load_dotenv()
        password = os.getenv("email_password")
        email = yagmail.SMTP(user="pythonwebmailapp@gmail.com",
                             password=password)

        email.send(to=self.email,
                   subject="Get Ready for an Unforgettable Night at Yellow Light Arts!\n"
                           "Your event is just around the corner — here’s everything you need to know",
                   contents=body,
                   attachments=f"{self.surname}_{self.artist_name}.pdf")


if __name__ == "__main__":
    event = Events(artist_name="Cinematic Orchestra", id="5")

    ticket = Ticket(name="John", surname="Diskakis", email="giannisdiskakis@gmail.com", artist_name="Cinematic Orchestra")

    ticket.insert_ticket_data()
    ticket.make_ticket()
    ticket.send_ticket(event=event)
    print(event.get_time(),event.get_date())
