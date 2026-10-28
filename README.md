# Bookora

A Django website where creators can sell ebooks, upload short videos,
and post on their Bookora profiles.

## What it does

- **Sign up / log in** — `/signup/`, `/login/`
- **Profile** — profile pic, bio, and a link to paste: `/profile/edit/`, public at `/@username/`
- **Posts** — text/image posts on your profile: `/post/`
- **Short videos** — upload at `/videos/upload/`, scroll them at `/videos/`, like them (tap again to unlike), and comment on each video at `/videos/<id>/`
- **Ebooks** — sell at `/ebooks/upload/`, browse at `/ebooks/`, buy at `/ebooks/<id>/buy/`, your purchases at `/library/`
- **Pricing** — `/pricing/`: $5.00/month, first month $2.50 (50% off), then $5.00 onwards

## Payment — to connect later

Payment is intentionally NOT live yet. The code has clear hooks in:

- `bookora/settings.py` — `BOOKORA_PAYMENT_PROVIDER` (set to `'polo'` when connected)
- `accounts/views.py` — `subscribe()`
- `shop/views.py` — `checkout()`

Right now subscribing or buying only records the order/subscription as
`pending_payment` and tells the user nothing has been charged. Connect
Polo there when you are ready, and flip those records to paid on webhook
confirmation.

## Run it locally

```bash
cd bookora
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Then open http://127.0.0.1:8000/

Admin is at http://127.0.0.1:8000/admin/

## Structure

- `bookora/` — project settings and main URLs
- `accounts/` — profiles, bio/link, subscription pricing
- `shop/` — ebooks and purchases
- `feed/` — posts, short videos, video likes and video comments
- `templates/` — all pages
- `media/` — uploaded pics, videos and ebook files (created on first upload)
