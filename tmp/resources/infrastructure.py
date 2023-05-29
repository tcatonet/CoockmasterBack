# BRAIZET Rémi
# Version 1.0

from flask_restful import Resource, reqparse

from utils.success_payload_formatter import response_success


class Infrastructure(Resource):
    """Infrastructure' endpoint."""

    parser = reqparse.RequestParser()


    def get(self):
        """
        get all infrastructure for one user.
        params: 
        :return: success or failure.
        :rtype: application/json response.
        """

        if not auth_data['auth_success']:
          return auth_data['message'] 
        
        current_email = auth_data["current_email"] 
        current_password = auth_data["current_password"] 
        refresh_token = auth_data["refresh_token"] 

        data = InfrastructureModel.find_all_infrastructure()

        all_infra = []
        for d in data:
            cur_inra = d.__dict__.copy()
            del cur_inra['_sa_instance_state']
            all_infra.append(cur_inra)

        response = response_success(message='Infrastructure successfully retrieve', data=all_infra, refresh_token=refresh_token)
        return response