# @classmethod
# def update_email_name_user(cls, newemail, name, email, password):
#     """
#     update a user project from the DB and returns it.
#
#     :param email: the UserName of the user.
#            name: the name of the project.
#     :type email: str
#           name: str
#     :return: a user.
#     :rtype: ProjectModel.
#     """
#     user = cls.query.filter_by(email=email).first()
#     user.email = newemail
#     user.username = name
#     db.session.commit()

# @classmethod
# def update_password_user(cls, password, newpassword, email):
#     """
#     update a user project from the DB and returns it.
#
#     :param email: the UserName of the user.
#            name: the name of the project.
#     :type email: str
#           name: str
#     :return: a user.
#     :rtype: ProjectModel.
#     """
#
#     newpassword = generate_password_hash(newpassword)
#     user = cls.query.filter_by(email=email).first()
#
#     if user:
#         user.password = newpassword
#         d
#         b.session.commit()

# @classmethod
# def find_by_email_and_password(cls, email, password):
#     """
#         Selects a user from the DB and returns it.
#
#         :param email: the username of the user.
#         :type email: str
#         :return: a user.
#         :rtype: UserModel.
#     """
#
#     user = cls.query.filter_by(email=email).first()
#     response = None
#     if user:
#         if check_password_hash(user.password, password):
#             response = user
#
#     return response

# @classmethod
# def get_id(cls, email, password):
#     """
#     Selects a user from the DB and returns it.
#
#         :email _id: the id of the user.
#         :type _id: int
#         :return: a user.
#         :rtype: UserModel.
#     """
#
#     user = cls.query.filter_by(email=email).first()
#
#     if user:
#         if check_password_hash(user.password, password):
#             return user.id