set dotenv-load := true

docker:
		docker compose up --build -d

sql:
    sql-studio postgres postgresql://postgres:098098@localhost:5432/chat
    # rainfrog --url $DB__DSN_RAINFROG

redis:
    redis_tui -address localhost:6379 -db 0

env:
    source /home/jaskier/.cache/pypoetry/virtualenvs/chat-c72m4GGP-py3.13/bin/activate

uml:
    docker run -d -p 8081:8080 plantuml/plantuml-server:jetty
