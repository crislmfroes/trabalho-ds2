from app import db
db.create_all()
import app.seeding.user_seeder
import app.seeding.tipo_seeder
