# Yellow Light Arts

Yellow Light Arts is a web page for a fictional concert hall called "Yellow Light Arts".
It provides a seamless experience for users to discover available and planned concerts, 
book tickets, and stay updated on events. 
The platform integrates powerful features to enhance user engagement and
manage concert-related activities efficiently.

## Description

1. Artist Information Integration:

   * Fetches artist biographies using the Last.fm API.
   * Retrieves artist photos through the Spotify API.
   

2. User Profiles:

   * Users can create personal profiles.
   * Data is securely stored using SQLite 3.
   

3. PDF Ticket Generation:

    * Automatically generates a PDF ticket for each event booked by a user.
    * Tickets are personalized and include event details.

4. Email Notifications:

   * Sends a detailed email to users after booking, including:
     * Event details.
     * The attached ticket.

5. Event Voting:

     * Users with profiles can vote for future events to show their interest and engagement.





## Installing

### Prerequisites
   * Python 3.9 or later.
   * Required libraries (install using the requirements.txt file).
   * SQLite 3
   * Spotify ApiKey 
   * Last Fm ApiKey

### Steps




1. Set up the SQLite database
2. Get your Api Keys to use them in ticket.py
   * Spotify Api Key is not necessary to run the app
     in a local server.Its use is to find photos for 
     creating new events.
   * Last Fm Api Key in necessary because it is used 
     to display artist bio to every event.
3. Use your email or a sample email in Ticket.py and method send_ticket().
   Use/create your app password that google provides you.
4. Run the web_main.py and go to development server 
   http://127.0.0.1:5000 to explore the app.

### Executing program

1. Creating a Profile:
* Visit the homepage and About page to get info's for concert hall.
2. Exploring Artists:
* Search for artists to view their bio and photos.
3. Booking Events:
* Select an event, book a ticket, and receive a PDF and email confirmation.
4. Voting:
* Create a profile to vote for events you’re excited about.
## Technologies Used

* Frontend: HTML5, MaterializeCss, JavaScript
* Backend: Python (Flask)
* Database: SQLite 3
* APIs:
   * Last.fm API: Fetch artist biographies.
   * Spotify API: Fetch artist photos.



