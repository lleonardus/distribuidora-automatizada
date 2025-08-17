from db.database import Base, engine
import db.models

Base.metadata.create_all(engine)
