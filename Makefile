local:
	docker-compose up -d

local-rebuild:
    docker-compose down &&\
    docker rmi demobotrista-web || true &&\
    docker-compose up --build -d
