

# # User Database Route
# # this route sends back list of users
# @app.route('/login_required', methods=['GET'])
# @token_required
# def check_login(current_user):
#     # querying the database
#     # for all the entries in it
#     users = User.query.all()
#     # converting the query objects
#     # to list of jsons
#     output = []
#     for user in users:
#         # appending the user data json
#         # to the response list
#         output.append({
#             'public_id': user.public_id,
#             'name': user.name,
#             'email': user.email
#         })
#
#     return jsonify({'users': output})
