import base64
import sqlite3
import os
import requests
from PIL import Image
from dotenv import load_dotenv

class Events:
    """A class that makes an event obj ,and gets information from
    https://www.lastfm to return artist bio and from spotify
     to return artist picture.Gets API request and extracts information
    from JSON file.Also Validates the votes for the audience
    """

    data_base_path = "C:\\Users\\d_jas\\PycharmProjects\\Booking_vote_concert\\data.db"

    def __init__(self, artist_name, id):
        self.artist_name = artist_name
        self.id = id

    def get_date(self):
        """Gets the date from artist event ,every event has
        a primary key id.Take the id from data.db"""

        cnx = sqlite3.connect(self.data_base_path)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "event_date" FROM "event" WHERE "id" =?
        """, [self.id])
        result = cur.fetchall()[0][0]
        cnx.close()
        return result

    def get_time(self):
        """Gets the time from artist event ,every event has
                a primary key id.Take the id from data.db"""

        cnx = sqlite3.connect(self.data_base_path)
        cur = cnx.cursor()
        cur.execute("""
                SELECT "event_time" FROM "event" WHERE "id" =?
                """, [self.id])
        result = cur.fetchall()[0][0]
        cnx.close()
        return result

    @staticmethod
    def get_token():
        """
        Creates an API token to use Spotify info

        """
        load_dotenv()
        client_id = os.getenv("client_id")
        client_secret = os.getenv("client_secret")

        # Encode credentials as Base64
        auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

        #  Request the token
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': f'Basic {auth_header}', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials'}

        response = requests.post(url, headers=headers, data=data)

        response_data = response.json()

        # Get the access token
        token = response_data.get('access_token')

        return token

    def get_bio(self, remove_name):
        """
        Gets bio from last.fm
        The variable remove_name should be like example below:
        name:Coldplay remove_name:Coldplay
        name:Bill Frisell remove_name:Bill+Frisell
        I use the variable to remove a href link from bio
        """
        load_dotenv()
        last_fm_api = os.getenv("last_fm_api")
        url = (f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&"
               f"artist={self.artist_name}"
               f"&api_key={last_fm_api}&"
               f"format=json")

        response = requests.get(url=url)
        content = response.json()
        artist_bio = content["artist"]["bio"]["summary"].replace(
            f'<a href="https://www.last.fm/music/{remove_name}">Read more on Last.fm</a>', "")

        return artist_bio

    def get_photo(self):
        """
        Gets the artist photo from spotify ,using an API Key
        and writes it to a .jpeg file with the name of the artist
        """
        search_url = f'https://api.spotify.com/v1/search?q={self.artist_name}&type=artist'
        search_headers = {'Authorization': f'Bearer {self.get_token()}'}

        response = requests.get(search_url, headers=search_headers)

        artist_data = response.json()
        artist_pic_url = artist_data["artists"]["items"][0]["images"][0]["url"]  # Image url

        image_response = requests.get(artist_pic_url)
        img_data = image_response.content
        f = open(f"{self.artist_name}.jpeg", "wb")
        f.write(img_data)
        f.close()

        image = Image.open(f"{self.artist_name}.jpeg")
        image.show()

    def get_vote(self):
        """Gets the votes from artist event ,every event has
        a primary key id.Take the id from data.db"""

        cnx = sqlite3.connect(database=self.data_base_path)
        cur = cnx.cursor()
        cur.execute("""
        SELECT "votes" FROM "event" WHERE "id" =?
        """, [self.id])
        result = cur.fetchall()[0][0]
        cnx.close()
        return result

    def add_vote(self):
        """Adds a vote to the artist event every time a person votes,
         every event has a primary key id.Take the id from data.db"""

        cnx = sqlite3.connect(database=self.data_base_path)
        cnx.execute("""
        UPDATE "event" SET "votes" =? WHERE "id" =?
        """, [self.get_vote() + 1, self.id])
        cnx.commit()
        cnx.close()

    def send_mails(self):
        """A method that send automated mails if votes
        of an event reach 200 """
        pass


if __name__ == "__main__":
    events = Events(artist_name="Bill Frisell", id=1)

    print(events.get_bio(remove_name="Bill+Frisell"))
    print(events.get_vote())
    print(events.get_date())

    print(events.get_time())
