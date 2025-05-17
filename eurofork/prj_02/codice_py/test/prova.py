from datetime import datetime, timezone, timedelta

tempo = 3  # minuti

def data():
    expire = datetime.now() + timedelta(minutes=tempo)
    return {
        "exp": expire,
        "iat": datetime.now()
    }

print(data())
