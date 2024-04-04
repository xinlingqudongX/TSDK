from typing import TypedDict, List, Dict, Any
from enum import StrEnum, Enum

class QrStatus(StrEnum):
    已刷新 = 'refused'
    已扫码 = 'scanned'
    已扫码2 = '2'
    未扫码 = 'new'
    未扫码2 = '1'
    扫码成功 = '3'

class QrcodeData(TypedDict):
    captcha: str
    desc_url: str
    description: str
    err_code: int
    is_frontier: bool
    qrcode: str
    qrcode_index_url: str
    token: str

class QrcodeDataFrontierParams(TypedDict):
    access_key: str
    frontier_device: str
    method: int
    product_id: int
    service_id: int

class QrcodeData2(TypedDict):
    app_name: str
    frontier_params: QrcodeDataFrontierParams
    is_frontier: bool
    qrcode: str
    qrcode_index_url: str
    token: str
    web_name: str

class QrCheckData(TypedDict):
    captcha: str
    desc_url: str
    description: str
    error_code: int
    is_frontier: bool
    qrcode: str
    qrcode_index_url: str
    status: QrStatus
    token: str
    redirect_url: str

class QrCheckRes(TypedDict):
    data: QrCheckData
    description: str
    error_code: int
    message: str

class QrLoginRes(TypedDict):
    data: QrcodeData2
    description: str
    error_code: int
    message: str

class ProfileOtherUserType(TypedDict):
    apple_account: int
    avatar_168x168: Dict[str, Any]
    avatar_300x300: Dict[str, Any]
    avatar_larger: Dict[str, Any]
    avatar_medium: Dict[str, Any]
    avatar_thumb: Dict[str, Any]
    aweme_count: int
    aweme_count_correction_threshold: int
    birthday_hide_level: int
    can_set_item_cover: int
    can_show_group_card: int
    card_entries: List[Any]
    city: str
    close_friend_type: int
    commerce_info: Dict[str, Any]
    commerce_permissions: Dict[str, Any]
    commerce_user_info: Dict[str, Any]
    commerce_user_level: int
    country: str
    cover_and_head_image_info: Dict[str, Any]
    cover_colour: str
    cover_url: List[Any]
    custom_verify: str
    district: str
    dongtai_count: int
    dynamic_cover: Dict[str, Any]
    enable_ai_double: int
    enable_wish: int
    enterprise_user_info: str
    enterprise_verify_reason: str
    favorite_permission: int
    favoriting_count: int
    follow_guide: int
    follow_status: int
    follower_count: int
    follower_request_status: int
    follower_status: int
    following_count: int
    forward_count: int
    gender: int
    general_permission: Dict[str, Any]
    has_e_account_role: int
    has_subscription: int
    im_primary_role_id: int
    im_role_ids: List[Any]
    image_send_exempt: int
    ins_id: str
    ip_location: str
    is_activity_user: int
    is_ban: int
    is_block: int
    is_blocked: int
    is_effect_artist: int
    is_gov_media_vip: int
    is_mix_user: int
    is_not_show: int
    is_series_user: int
    is_sharing_profile_user: int
    is_star: int
    life_story_block: Dict[str, Any]
    live_commerce: int
    live_status: int
    max_follower_count: int
    message_chat_entry: int
    mix_count: int
    mplatform_followers_count: int
    nickname: str
    no_recommend_user: int
    original_musician: Dict[str, Any]
    pigeon_daren_status: str
    pigeon_daren_warn_tag: str
    profile_show: Dict[str, Any]
    profile_tab_type: int
    province: str
    public_collects_count: int
    publish_landing_tab: int
    r_fans_group_info: Dict[str, Any]
    recommend_reason_relation: str
    recommend_user_reason_source: int
    risk_notice_text: str
    role_id: str
    room_id: int
    room_id_str: str
    school_name: str
    sec_uid: str
    secret: int
    series_count: int
    share_info: Dict[str, Any]
    short_id: str
    show_favorite_list: int
    show_subscription: int
    signature: str
    signature_display_lines: int
    signature_language: str
    special_follow_status: int
    sync_to_toutiao: int
    tab_settings: Dict[str, Any]
    total_favorited: int
    total_favorited_correction_threshold: int
    twitter_id: str
    twitter_name: str
    uid: str
    unique_id: str
    urge_detail: Dict[str, Any]
    user_age: int
    user_not_see: int
    user_not_show: int
    user_permissions: List[Any]
    verification_type: int
    video_cover: Dict[str, Any]
    video_icon: Dict[str, Any]
    watch_status: int
    white_cover_url: List[Any]
    with_commerce_enterprise_tab_entry: int
    with_commerce_entry: int
    with_fusion_shop_entry: int
    with_new_goods: int
    youtube_channel_id: str
    youtube_channel_title: str


class ProfileOtherResType(TypedDict):
    extra: Dict[str, Any]
    log_pb: Dict[str, Any]
    status_code: int
    status_msg: str
    user: ProfileOtherUserType

class WareCsrfToken(TypedDict):
    expiredAt: int
    timeout: bool
    value: str

class VideoCommentType(TypedDict):
    status_code: int
    comments: List[Any]
    cursor: int
    has_more: int
    reply_style: int
    total: int
    extra: Dict[str, Any]
    log_pb: Dict[str, Any]
    hotsoon_filtered_count: int
    user_commented: int
    fast_response_comment: Dict[str, Any]
    comment_config: Dict[str, Any]
    general_comment_config: Dict[str, Any]
    show_management_entry_point: int
    folded_comment_count: int
