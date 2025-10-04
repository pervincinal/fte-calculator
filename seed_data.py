from app.db.database import SessionLocal, engine, Base
from app.models.models import ChapterLead, Tribe, Squad, PriorityEnum, StatusEnum
from datetime import datetime

# Create all tables
Base.metadata.create_all(bind=engine)

# Create a new database session
db = SessionLocal()

try:
    # Check if data already exists
    existing_tribes = db.query(Tribe).count()
    if existing_tribes > 0:
        print(f"Database already has {existing_tribes} tribes. Skipping seed.")
    else:
        # Create Chapter Leads
        cl1 = ChapterLead(name="John Doe", email="john.doe@kapitalbank.az")
        cl2 = ChapterLead(name="Jane Smith", email="jane.smith@kapitalbank.az")
        cl3 = ChapterLead(name="Mike Johnson", email="mike.johnson@kapitalbank.az")
        db.add_all([cl1, cl2, cl3])
        db.commit()
        print("Created 3 Chapter Leads")

        # Create Tribes
        tribe1 = Tribe(
            name="Digital Banking",
            priority=PriorityEnum.HIGH,
            chapter_lead_id=cl1.id
        )
        tribe2 = Tribe(
            name="Core Banking",
            priority=PriorityEnum.CRITICAL,
            chapter_lead_id=cl2.id
        )
        tribe3 = Tribe(
            name="Payment Systems",
            priority=PriorityEnum.MEDIUM,
            chapter_lead_id=cl3.id
        )
        db.add_all([tribe1, tribe2, tribe3])
        db.commit()
        print("Created 3 Tribes")

        # Create Squads
        squads = [
            Squad(
                name="Mobile Banking",
                priority=PriorityEnum.HIGH,
                tribe_id=tribe1.id,
                platforms=["IOS", "ANDROID"],
                status=StatusEnum.ACTIVE
            ),
            Squad(
                name="Web Banking",
                priority=PriorityEnum.HIGH,
                tribe_id=tribe1.id,
                platforms=["WEB"],
                status=StatusEnum.ACTIVE
            ),
            Squad(
                name="API Gateway",
                priority=PriorityEnum.CRITICAL,
                tribe_id=tribe2.id,
                platforms=["API"],
                status=StatusEnum.ACTIVE
            ),
            Squad(
                name="Transaction Processing",
                priority=PriorityEnum.CRITICAL,
                tribe_id=tribe2.id,
                platforms=["API"],
                status=StatusEnum.ACTIVE
            ),
            Squad(
                name="Card Payments",
                priority=PriorityEnum.MEDIUM,
                tribe_id=tribe3.id,
                platforms=["API", "WEB"],
                status=StatusEnum.ACTIVE
            ),
            Squad(
                name="Mobile Payments",
                priority=PriorityEnum.MEDIUM,
                tribe_id=tribe3.id,
                platforms=["IOS", "ANDROID", "API"],
                status=StatusEnum.ACTIVE
            )
        ]
        db.add_all(squads)
        db.commit()
        print("Created 6 Squads")

        print("\n✅ Seed data created successfully!")
        print(f"- {db.query(ChapterLead).count()} Chapter Leads")
        print(f"- {db.query(Tribe).count()} Tribes")
        print(f"- {db.query(Squad).count()} Squads")

except Exception as e:
    print(f"Error creating seed data: {e}")
    db.rollback()
finally:
    db.close()