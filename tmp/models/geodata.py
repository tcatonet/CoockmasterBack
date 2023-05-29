# # BRAIZET Rémi
# # Version 1.0
#
#
# from db import db
# from werkzeug.security import generate_password_hash
# import logging
# import requests
# import json
#
#
# class GeoDataModel(db.Model):
#     """GeoData model."""
#
#     __tablename__ = 'geodatas'
#
#     id = db.Column(db.Integer, primary_key=True)
#     departement = db.Column(db.String(20))
#     codecommune = db.Column(db.String(20))
#     datageojson = db.Column(db.JSON)
#     geodataload = db.Column(db.Boolean, default=False, nullable=False)
#
#
#     def __init__(self, departement, codecommune, datageojson):
#         self.departement = departement
#         self.codecommune = codecommune
#         self.datageojson = datageojson
#
#     @classmethod
#     def get_all_project(cls):
#         return cls.query.all()
#
#
#     @classmethod
#     def find_by_departement(cls, departement):
#         """
#         Selects all commune data from the DB and returns it.
#
#         :param departement: the departement
#         :type departement: integer
#         :return: a GeoData.
#         :rtype: GeoDataModel list.
#         """
#         return cls.query.filter_by(departement=departement).all()
#
#
#     @classmethod
#     def find_by_commune(cls, commune):
#         """
#         Selects one commune data from the DB and returns it.
#
#         :param commune: the commune
#         :type commune: integer
#         :return: a GeoData.
#         :rtype: GeoDataModel list.
#         """
#         return cls.query.filter_by(commune=commune).first()
#
#
#     @classmethod
#     def is_empty(cls):
#         """
#         Selects one commune data from the DB and returns it.
#
#         :param commune: the commune
#         :type commune: integer
#         :return: a GeoData.
#         :rtype: GeoDataModel list.
#         """
#         result = cls.query.filter_by().count()
#         return result == 0
#
#     @classmethod
#     def update_geo_data(cls, geo_data_model, codecommune):
#         """
#         update a user project from the DB and returns it.
#
#         :param email: the UserName of the user.
#                name: the name of the project.
#         :type email: str
#               name: str
#         :return: a user.
#         :rtype: ProjectModel.
#         """
#
#         data_geo = db.session.query(GeoDataModel).filter_by(codecommune=codecommune).first()
#         geo_data_model.geodataload = True
#
#         db.session.delete(data_geo)
#         db.session.add(geo_data_model)
#         db.session.commit()
#
#         data_geo = db.session.query(GeoDataModel).filter_by(codecommune=codecommune).first()
#         print(data_geo.datageojson)
#
#
#     def save_to_db(self):
#         """
#         Inserts this user in the DB.
#         """
#         db.session.add(self)
#         db.session.commit()
#
#
#     def delete_from_db(self):
#         """
#         Deletes this user from the DB.
#         """
#         db.session.delete(self)
#         db.session.commit()