# BRAIZET Rémi
# Version 1.2


from db import db
from werkzeug.security import generate_password_hash


class MInfrastructure(db.Model):
    """ Infrastructure model """
    __tablename__ = 'infrastructures'

    id = db.Column(db.Integer, primary_key=True)
    infraname = db.Column(db.String(80))

    def __init__(self, infraname):
        self.infraname = infraname

    @classmethod
    def find_all_infrastructure(cls):
        return cls.query.all()

    @classmethod
    def seed_infra(cls):
        """
            Seeds DB at first connection if its empty
        """
        # load_geo_data = LoadGeoData()
        # load_geo_data.geo_data_load_and_save()
        
        infra_data = {"infraname": "habitation"}
        infra = cls.query.filter_by(infraname="habitation").first()

        if not infra:
            infra = MInfrastructure(**infra_data)
            db.session.add(infra)
            db.session.commit()

    def save_to_db(self):
        """
            Inserts this infrastructure in the DB.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
            Deletes this infrastructure from the DB.
        """
        db.session.delete(self)
        db.session.commit()
