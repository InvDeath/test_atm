build:
	docker build -t test_atm:dockerfile .

run:
	$(MAKE) build
	docker run -ti --rm -v $(shell pwd):/usr/src -p 8000:8000 test_atm:dockerfile python manage.py runserver 0.0.0.0:8000

shell:
	$(MAKE) build
	docker run -ti --rm -v $(shell pwd):/usr/src test_atm:dockerfile bash

test:
	$(MAKE) build
	docker run -ti --rm -v $(shell pwd):/usr/src test_atm:dockerfile python manage.py test
