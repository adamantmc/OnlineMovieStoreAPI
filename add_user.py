if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")

    args = parser.parse_args()

    import os, django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineMovieStore.settings")
    django.setup()
    from django.contrib.auth.models import User
    User.objects.create_user(username=args.username, password=args.password)
