from telethon import types, utils

photo_id = 6292027024948181024
dc_id = 5

loc = types.InputPeerPhotoFileLocation(
    # min users can be used to download profile photos
    # self.get_input_entity would otherwise not accept those
    peer=utils.get_input_peer(entity, check_hash=False),
    photo_id=photo.photo_id,
    big=download_big
)