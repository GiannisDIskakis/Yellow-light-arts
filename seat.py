import sqlite3


class Seat:
    database = "data.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.price = self._get_price()
        self.available = self._get_availability()

    def occupy(self):
        if self.seat_id != "A0":
            connection = sqlite3.connect(self.database)
            connection.execute("""
            UPDATE "seat" SET "captured"=1 WHERE "seat_id"=?
            """, [self.seat_id])
            connection.commit()
            connection.close()

    def _get_price(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "price" FROM "seat" WHERE "seat_id"=?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]
        connection.close()
        return result

    def _get_availability(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "captured" FROM "seat" WHERE "seat_id"=?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]
        connection.close()
        return result

if __name__ == "__main__":
    seat = Seat(seat_id="A9")
    print(seat.seat_id,seat.price,seat.available)
    seat.occupy()

