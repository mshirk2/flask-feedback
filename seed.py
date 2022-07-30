# Seed file for sample data

from models import db, User, Feedback
from app import app


# Drop all tables, and create them
db.drop_all()
db.create_all()


# Empty tables, just in case
User.query.delete()
Feedback.query.delete()


# Sample users
u1 = User.register(
    username = 'Monkeybrainz01', 
    password='banana', 
    email='banana@banana.com', 
    first_name='Mr.', 
    last_name='Bannaface'
    )

u2 = User.register(
    username = 'TweedleDee72', 
    password='wonderland', 
    email='ilovecheese@cheese.com', 
    first_name='Tweedle', 
    last_name='Dee'
    )

u3 = User.register(
    username = 'TweedleDum73', 
    password='dumdumdum', 
    email='ialsolovecheese@cheese.com', 
    first_name='Tweedle',
    last_name='Dum'
    )

u4 = User.register(
    username='Kibo99', 
    password='meowmeow', 
    email='kibo@catnetwork.com', 
    first_name='Kibo', 
    last_name='Chan'
    )

u5 = User.register(
    username='Munty44', 
    password='puurrrghggh', 
    email='munty@catnetwork.com', 
    first_name='Mr.', 
    last_name='Breakfast'
    )


db.session.add_all([u1, u2, u3, u4, u5])
db.session.commit()

#Sample feedback

f1 = Feedback(
    title="Banan", 
    content="Bananananananananananananananananana.", 
    username=u1.username
    )

f2 = Feedback(
    title="I found a daisy", 
    content="Chirrrrrrrup! Chirrrrrrrrp Chirrrruuuup.", 
    username=u2.username
    )

f3 = Feedback(
    title="I found another daisy", 
    content="Daisy, Daisy, give me your answer do, I'm half crazy, All for the love of you.", 
    username=u2.username
    )

f4 = Feedback(
    title="I'm the best Tweedle", 
    content="TweedleDumtweedledee tweedledum tweedledee tweedledum tweedledee tweedledum tweedledee.", 
    username=u3.username
    )

f5 = Feedback(
    title="I dunno about this new cat food", 
    content="Puurrrrrrrgghhhh.", 
    username=u4.username
    )

f6 = Feedback(
    title="This new cat food is great", 
    content="Meow mwe wow moew meow mwe wow moew meow mwe wow moew meow mwe wow moew meow.", 
    username=u5.username
    )    

db.session.add_all([f1, f2, f3, f4, f5, f6])
db.session.commit()