from app.db.database import SessionLocal, engine, Base
from app.models.models import Tribe, Squad, ChapterLead
import traceback

print("Testing database connection...")

try:
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    # Test session
    db = SessionLocal()
    print("✓ Session created")

    # Test query
    tribes_count = db.query(Tribe).count()
    print(f"✓ Found {tribes_count} tribes")

    squads_count = db.query(Squad).count()
    print(f"✓ Found {squads_count} squads")

    # List all tribes
    tribes = db.query(Tribe).all()
    for tribe in tribes:
        print(f"  - Tribe: {tribe.name} (Priority: {tribe.priority})")

    db.close()
    print("\n✅ Database test successful!")

except Exception as e:
    print(f"\n❌ Database test failed:")
    print(traceback.format_exc())