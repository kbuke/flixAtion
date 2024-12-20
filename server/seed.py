from app import app 
from config import db 

from datetime import date

import os

from models import Accounts, ActorDirector, Media, TvShow

from dotenv import load_dotenv
load_dotenv()

if __name__=="__main__":
    with app.app_context():
        print ("Starting seed...")

        db.drop_all()
        db.create_all()
        print("Begin seeding")

        print("Seeding users")
        kaan_buke=Accounts(
            email="kabuke13@gmail.com",
            first_name="Kaan",
            surname="Buke",
            intro="A lover of all things films and television. I have created this app to make finding both of these things easier",
        )
        kaan_buke.password_hash=os.environ.get("kaan_password")
        db.session.add_all([kaan_buke])
        db.session.commit()

        print("Seeding Actors and Directors")
        anya_t_j = ActorDirector(
            name="Anya Taylor Joy",
            dob=date(1996, 4, 16),
            image="https://anyataylorjoy.net/photos/albums/uploads/Photoshoots/2017/011/002.jpg",
            intro="Breakout actor from The Queens Gambit, and Mad Max: Furiosa",
            actor_director="Actor"
        )
        tom_hanks = ActorDirector(
            name="Tom Hanks",
            dob=date(1956, 7, 9),
            image="https://www.usatoday.com/gcdn/presto/2020/07/09/USAT/b850c175-4d38-49fe-9bf7-6950c37657ab-tom_hanks_67.JPG",
            intro="Actor most well known for Forest Gump",
            actor_director="Actor"
        )
        chris_nolan = ActorDirector(
            name="Christopher Nolan",
            dob=date(1970, 7, 30),
            image="https://ca-times.brightspotcdn.com/dims4/default/b8fe84c/2147483647/strip/true/crop/5400x7200+0+0/resize/2000x2667!/quality/75/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F10%2F90%2F88c02d2846cf92fc4313cb342ff5%2F1312323-et-christopher-nolan-1.jpg",
            intro="Legendary director behing Inception, Oppenheimer",
            actor_director="Director"
        )
        db.session.add_all([
            anya_t_j,
            tom_hanks,
            chris_nolan
        ])
        db.session.commit()

        print("Seeding movies")
        lotr_1=Media(
            title="The Lord of the Rings",
            sub_title="The Fellowship of the Ring",
            poster="https://m.media-amazon.com/images/M/MV5BNzIxMDQ2YTctNDY4MC00ZTRhLTk4ODQtMTVlOWY4NTdiYmMwXkEyXkFqcGc@._V1_.jpg",
            cover_photo="https://static.wikia.nocookie.net/lotr/images/d/df/Fellowship1.jpg/revision/latest?cb=20210723041619",
            release_date=date(2001, 12, 15),
            summary="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
            media_type="Movie",
            run_time_hours=3,
            run_rime_minutes=15
        )
        breaking_bad=TvShow(
            title="Breaking Bad",
            poster="https://m.media-amazon.com/images/M/MV5BMzU5ZGYzNmQtMTdhYy00OGRiLTg0NmQtYjVjNzliZTg1ZGE4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            cover_photo="https://www.indiewire.com/wp-content/uploads/2013/07/breaking-bad-9.jpg",
            release_date=date(2008, 9, 28),
            summary="A chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student to secure his family's future.",
            media_type="TV Show",
            run_time_hours=0,
            run_rime_minutes=45,
            end_date=date(2013, 9, 30)
        )
        db.session.add_all([
            lotr_1,
            breaking_bad
        ])
        db.session.commit()

        print("Finished seeding")