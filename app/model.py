from .models.user import create_user, update_user, singleUser,Address,deactivate_user,Vote
from .models.post import create, singlePost, delete, update, allPost, Like, personal_post, like_unlike,Post
from .models.otp import find_otp_block,find_otp_life_time,save_otp,save_otp_failed_count,save_block_otp,disable_otp