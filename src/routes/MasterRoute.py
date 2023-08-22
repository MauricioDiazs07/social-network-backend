from flask import Blueprint, jsonify, request
from src.models.ShareModel import ShareModel
from src.models.MasterModel import MasterModel
from src.models.MultimediaModel import MultimediaModel

main = Blueprint('master_blueprint', __name__)

@main.route('/<profile_id>', )
def get_master_data(profile_id):
    try:
        
        shares = ShareModel.get_shares_from_profile(profile_id)
        multimedias = MultimediaModel.get_all_multimedia_from_profile(profile_id)

        post_multimedia = []
        for share in shares:
            share.pop('name')
            share.pop('profileId')
            share.pop('profileImage')
            for multimedia in multimedias:
                if str(share['id']) == multimedia['share_id']:
                    multimedia.pop('share_id')
                    multimedia.pop('share_type')
                    multimedia.pop('profile_id')
                    post_multimedia.append(multimedia)
                    print(post_multimedia)
            share['multimedia'] = {"count": len(post_multimedia), "data": post_multimedia}

        data = MasterModel.get_info(profile_id)
        data['shares'] = {'count': len(shares), 'shares': shares}
        print(data)
        return jsonify(data)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500