# # BRAIZET Rémi
# # Version 1.0
#
#
# from db import db
# from werkzeug.security import generate_password_hash
#
#
# class ProjectModel(db.Model):
#     """Project model."""
#
#     __tablename__ = 'projects'
#
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.Integer())
#     description = db.Column(db.String(80))
#     departement = db.Column(db.String())
#     infrastructure = db.Column(db.String(80))
#     name = db.Column(db.String(80))
#
#
#     def __init__(self, userid, name, description, departement, infrastructure):
#         self.userid = userid
#         self.description = description
#         self.departement = departement
#         self.infrastructure = infrastructure
#         self.name = name
#
#
#     @classmethod
#     def get_all_project(cls):
#         return cls.query.all()
#
#
#     @classmethod
#     def find_by_userid(cls, id):
#         """
#         Selects all project from one user from the DB and returns it.
#
#         :param userid: the id of the user.
#         :type email: str
#         :return: a user.
#         :rtype: ProjectModel list.
#         """
#         return cls.query.filter_by(userid=id).all()
#
#
#     @classmethod
#     def find_by_name(cls, userid, name):
#         """
#         Selects a user project from the DB and returns it.
#
#         :param email: the UserName of the user.
#                name: the name of the project.
#         :type email: str
#               name: str
#         :return: a user.
#         :rtype: ProjectModel.
#         """
#         return cls.query.filter_by(userid=userid, name=name).first()
#
#
#     @classmethod
#     def update_one_project(cls, userid, name, newname, description):
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
#         project = cls.query.filter_by(userid=userid, name=name).first()
#         project.name = newname
#         project.description = description
#         db.session.commit()
#         return project
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
