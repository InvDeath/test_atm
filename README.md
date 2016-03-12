# test_atm
Test task Python/Django

This test app emulates wor ATM with demonstration purpose. 

## Requirements

- Docker
- Gnu Make

Or you can run Django app inside your virtualenv if you want manually.

## Quick start
- Clone repo
- $ make init
- $ make run

Open http://localhost:8000 or http://ip_your_docker_vm:8000 in your web browser.

## What can be improved
- Add JS validation
- Add tests for JS
- Add/improve admin edit models
- Add currency choosing
- Add cardholder info (name etc)
- Encode PIN code in db
- Use Django Auth User
- Disable some unused Django components (middlewares or other)
- ~~Move constants in settings.py~~
- ~~Create card number unique~~
- Check cookies if client use (we use cookies)
- Use Django components for security or create decorator for view
- Write additional test cases
- Add session timeouut

