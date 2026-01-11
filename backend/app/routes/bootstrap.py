from app.db.conn import db_session, engine
from app.db.repository import ClientRepository
from app.models import Base
import uuid

LOCAL_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

def init_db():
    Base.metadata.create_all(bind=engine)

def init_local_client():
    """Initialize a local client for testing/development."""
    with db_session() as db:
        existing_client = ClientRepository.get_by_id(db, LOCAL_USER_ID)
        if not existing_client:
            ClientRepository.create(db, client_id=LOCAL_USER_ID, client_name="local-dev-client")