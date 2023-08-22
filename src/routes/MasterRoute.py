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
        for share in shares:
            post_multimedia = []
            share.pop('name')
            share.pop('profileId')
            share.pop('profileImage')
            for multimedia in multimedias:
                if 'share_id' in multimedia:
                    if str(share['id']) == str(multimedia['share_id']):
                        multimedia.pop('share_id')
                        multimedia.pop('share_type')
                        multimedia.pop('profile_id')
                        post_multimedia.append(multimedia)
            share['multimedia'] = {"count": len(post_multimedia), "data": post_multimedia}
        data = MasterModel.get_info(profile_id)
        data['shares'] = {'count': len(shares), 'shares': shares}
        return jsonify(data)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500