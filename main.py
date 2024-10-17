from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env
from pywebio.output import clear
from password_checker import PasswordChecker

users = {
    'randomperson@something.com': {'name': 'Random Person', 'password': 'xyz0123'}
}

events = [
    "Welcoming Party!, September 30th - 8pm",
    "New Years Party!, December 31th - 10pm",
    "Leaving Party!, June 11th - 6pm"
]

notifications = [
    "You have a parcel waiting for you! (Sent - May 11th, 9:39 p.m.)",
    "Reminder: You booked the cinema room for tomorrow! (Sent - May 29th, 10:00 a.m.)",
    "Site access required: We will conduct a maintenance check up tomorrow. (Sent - June 15th, 10:00 a.m.)"
]


def main():
    set_env(title="Student Accommodation App")
    while True:
        action = radio("Choose Action", options=['Login', 'Register'])
        if action == 'Register':
            register()
        elif action == 'Login':
            user = login()
            if user:
                welcome_page(user['name'])
                break

def register():
    data = input_group("Register", [
        input('Enter your name', name='name', required=True),
        input('Enter your email', name='email', required=True),
        input('Create a password', name='password', type=PASSWORD, required=True)
    ])

    check_pw = PasswordChecker(data['password'])
    if not check_pw.validate():
        put_error('Password does not meet requirements! You need an a minimum of 8 characters, an lowercase and uppercase character and a number.')
        return

    if data['email'] in users:
        put_error('This email has already been registered!')
        return

    users[data['email']] = {'name': data['name'], 'password': data['password']}
    put_success('You have successfully registered! Try logging in now.')

def login():
    data = input_group("Login", [
        input('Enter your email', name='email', required=True),
        input('Enter your password', name='password', type=PASSWORD, required=True)
    ])
    user = users.get(data['email'])
    if not user or user['password'] != data['password']:
        put_error('Invalid email or password!')
        return None
    return user

def welcome_page(username):
    clear()
    put_html(f"<h3>Welcome, {username}!</h3>")
    put_buttons(['Home', 'Notifications', 'FAQs', 'Account'],
                onclick=[
                    lambda: show_home(username),
                    lambda: show_notifications_page(username),
                    lambda: show_faqs(username),
                    lambda: show_account(username)
                ])
    events_html = "<div style='height:400px; width:100%; border:1px solid #000; overflow-y: auto; padding: 15px;'>"
    events_html += "<h4>Upcoming Events:</h4>"
    for event in events:
        events_html += f"<p>{event}</p>"
    events_html += "</div>"
    put_html(events_html)

def show_home(username):
    clear()
    welcome_page(username)

def show_notifications_page(username):
    clear()
    put_html("<h3>Notifications</h3>")
    for notification in notifications:
        put_text(notification)
    put_buttons(['Return to Home'], onclick=[lambda: welcome_page(username)])

def show_faqs(username):
    clear()
    put_html("<h3>Frequently Asked Questions</h3>")
    faqs_html = "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; max-width: 600px;'>"
    faqs_html += "<p><b>Q: How do I book the cinema room?</b></p>"
    faqs_html += "<p>A: To book the cinema room, head to the front desk and ask for a booking form.</p>"
    faqs_html += "<p><b>Q: Are bedsheets included?</b></p>"
    faqs_html += "<p>A: Unfortunately, we do not provide bedsheets.</p>"
    faqs_html += "</div>"

    put_html(faqs_html)
    put_buttons(['Return to Home'], onclick=[lambda: welcome_page(username)])

def contact_us(username):
    clear()
    put_markdown("""
    ## Contact Us

    If you have any further questions, please don't hesitate to contact us at randomemail@random.com or call us at +44 01209382982.

    """)
    put_buttons(['Return to Home'], onclick=[lambda: welcome_page(username)])


def show_account(username):
    clear()

    # User Info Display
    put_html(f"<h3>Account Information</h3>")
    put_table([
        ['Name', 'Resident ID', 'Email', 'Number'],
        ['Herbie Hancock', 'XXX123', 'headhunter@jazz.com', '2938429300']
    ])


    # Logout Button
    put_buttons(['Log Out'], onclick=logout_user)
    put_buttons(['Return to Home'], onclick=[lambda: welcome_page(username)])

def logout_user(btn_val):
    clear()
    toast(f"You logged out! Bye!")

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)



