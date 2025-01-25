import sqlite3


class Card:
    database = "data.db"

    def __init__(self, holder_name, holder_surname, card_type, number, cvc):
        self.hn = holder_name
        self.hs = holder_surname
        self.card_type = card_type
        self.number = number
        self.cvc = cvc

    def get_cursor_fetchall(self):

        cnx = sqlite3.connect(self.database)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "balance" FROM "card" WHERE "holder_name"=? and "holder_surname"=?
        and "type"=? and "cvc"=? and "number" = ?
        """, [self.hn, self.hs, self.card_type, self.cvc, self.number])
        result = cur.fetchall()
        return result

    def set_balance(self, ticket_price):
        """Checks if the information about the card that user gave are correct,
        and if they are sets balance in the database and returns True"""

        if self.get_cursor_fetchall():
            balance = self.get_cursor_fetchall()[0][0]

            if balance >= ticket_price:
                cnx = sqlite3.connect(self.database)
                cnx.execute(f"""
                UPDATE "card" SET "balance"=? WHERE "type"=? and "cvc"=? and "number" = ?
                """, [balance - ticket_price, self.card_type, self.cvc, self.number])
                cnx.commit()
                cnx.close()

            else:
                return "Your balance it's not enough to continue purchase"

        else:
            return "Please type again the information about your card, maybe there is something wrong"


if __name__ == "__main__":
    card = Card(holder_name="JOHN", holder_surname="DISKAKIS", card_type="Mastercard", number="12345678", cvc="123")
    print(card.get_cursor_fetchall())
    print(card.set_balance(ticket_price=100))
