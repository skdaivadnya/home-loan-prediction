from database import Base,engine
from models import Features

print("Creating database ....")

Base.metadata.create_all(engine)
