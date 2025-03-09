import datetime
import uuid

class Event:
    def _init_(self, title, description, date_str, time_str, location, organizer):
        self.id = str(uuid.uuid4())  # Unique event ID
        self.title = title
        self.description = description
        self.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        self.time = datetime.datetime.strptime(time_str, '%H:%M').time()
        self.location = location
        self.organizer = organizer
        self.attendees = set()  # Set of usernames

    def add_attendee(self, username):
        self.attendees.add(username)

class EventManager:
    def _init_(self):
        self.events = {}  # Dictionary to store events (key: event ID, value: Event object)
        self.users = {}   # Dictionary to store users (key: username, value: User object)

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            print("User registered successfully!")
        else:
            print("Username already exists.")

    def login_user(self, username, password):
        if username in self.users and self.users[username].check_password(password):
            print("Login successful!")
            return self.users[username]
        else:
            print("Invalid username or password.")
            return None

    def create_event(self, title, description, date_str, time_str, location, organizer):
        try:
            event = Event(title, description, date_str, time_str, location, organizer)
            self.events[event.id] = event
            print(f"Event '{title}' created successfully with ID: {event.id}")
            return event
        except ValueError:
            print("Invalid date or time format.")
            return None

    def schedule_event(self, user, event_id, date_str, time_str):
        if event_id not in self.events:
            print("Event not found.")
            return

        event = self.events[event_id]
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.datetime.strptime(time_str, '%H:%M').time()

            # Ensure scheduled time is in the future
            if datetime.datetime.combine(date, time) <= datetime.datetime.now():
                print("Cannot schedule event in the past.")
                return

            user.scheduled_events[event.id] = (date, time)
            print(f"Event '{event.title}' scheduled by {user.username} for {date} at {time}.")

            print(f"Notification sent to {user.username}: Event '{event.title}' is scheduled for {date} at {time}.")
        except ValueError:
            print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

    def get_user_events(self, user):
        if not user.scheduled_events:
            print(f"{user.username} hasn't scheduled any events.")
        else:
            print(f"Events scheduled by {user.username}:")
            for event_id, (date, time) in user.scheduled_events.items():
                event = self.events.get(event_id)
                if event:
                    print(f"- {event.title} on {date} at {time}")

    def attend_event(self, user, event_id):
        if event_id in self.events:
            event = self.events[event_id]
            if user.username not in event.attendees:
                event.add_attendee(user.username)
                print(f"{user.username} is now attending '{event.title}'.")
            else:
                print(f"{user.username} is already attending '{event.title}'.")
        else:
            print("Event not found.")

    def view_event(self, event_id):
        if event_id in self.events:
            event = self.events[event_id]
            print(f"Event Details:\nTitle: {event.title}\nDescription: {event.description}\nDate: {event.date}\nTime: {event.time}\nLocation: {event.location}\nOrganizer: {event.organizer}\nAttendees: {len(event.attendees)}")
        else:
            print("Event not found.")

    def list_events(self):
        if not self.events:
            print("No events available.")
        else:
            print("Available Events:")
            for event in self.events.values():
                print(f"- {event.title} on {event.date} at {event.time} (Organizer: {event.organizer})")

class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password  # In a real app, hash passwords securely!
        self.scheduled_events = {}  # Dictionary (event ID -> (date, time))

    def check_password(self, password):
        return self.password == password  # In a real app, compare password hashes

# Example Usage
manager = EventManager()

# User registration and login
manager.register_user("john_doe", "password123")
user1 = manager.login_user("john_doe", "password123")

if user1:
    event1 = manager.create_event("Tech Conference", "Annual tech conference", "2024-03-15", "09:00", "Convention Center", "John Doe")
    if event1:
        manager.schedule_event(user1, event1.id, "2024-03-16", "10:00")
        manager.attend_event(user1, event1.id)
        manager.get_user_events(user1)
        manager.view_event(event1.id)

    event2 = manager.create_event("Music Festival", "Summer music festival", "2024-07-20", "14:00", "City Park", "Jane Smith")
    if event2:
        manager.schedule_event(user1, event2.id, "2024-07-21", "15:00")
        manager.get_user_events(user1)

    manager.list_events()