import nox


DB_PACKAGE = {
    "mysql": {
        "3.5": ["mysqlclient>=1.3.13"],
        "3.6": ["mysqlclient>=1.3.13"],
        "3.7": ["mysqlclient>=1.3.13"],
        "3.8": ["mysqlclient>=1.3.13"],
    },
    "postgres": {
        "3.5": ["psycopg2>=2.5.4"],
        "3.6": ["psycopg2>=2.5.4"],
        "3.7": ["psycopg2>=2.5.4"],
        "3.8": ["psycopg2>=2.5.4"],
    },
}


@nox.session(python=["3.5", "3.6", "3.7", "3.8"])
@nox.parametrize("django", ["2.2.10", "3.0", "3.0.1", "3.0.2", "3.0.3"])
@nox.parametrize("database", ["postgres", "mysql", "sqlite3"])
def tests(session, django, database):
    if django.split(".")[0] == "3" and session.python == "3.5":
        session.skip("Python: {} and django: {}".format(session.python, django))

    if database != "sqlite3":
        session.install(
            *DB_PACKAGE[database][session.python],
            env={
                "LDFLAGS": "-L/usr/local/opt/openssl@1.1/lib",
                "CPPFLAGS": "-I/usr/local/opt/openssl@1.1/include",
            }
        )
    session.install("django=={}".format(django))
    session.run("bash", "-c", "make test", external=True, env={"ENV_DB": database})


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", ".")
