from typing import TypedDict, List, Dict, Any, Union, Optional
from enum import Enum

class QrStatus(Enum):
    已刷新 = 'refused'
    已扫码 = 'scanned'
    已扫码2 = '2'
    未扫码 = 'new'
    未扫码2 = '1'
    登录成功 = '3'
    取消登录 = '4'
    刷新扫码 = '5'

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

class FrontierDevice(TypedDict):
    access_key: str
    frontier_device: str
    method: int
    product_id: int
    service_id: int

class QrCheckErrorCode(Enum):
    Success = 0
    Error = 2156
    Verify = 2046

class QrChceckVerifyWays(TypedDict):
    mobil: str
    verify_way: str
    channel_mobile: str
    sms_content: str

class QrCheckData(TypedDict):
    captcha: str
    desc_url: str
    description: str
    error_code: QrCheckErrorCode
    is_frontier: bool
    qrcode: str
    qrcode_index_url: str
    status: QrStatus
    token: str
    redirect_url: str
    app_name: str
    frontier_params: Optional[FrontierDevice]

    biz_params: Any
    event_params: Any
    is_optional_verify: bool
    need_show_verify_tab: bool
    schema: str
    url: str
    verify_scene_desc: str
    verify_ticket: str
    verify_ways: Any

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

class ErrorRes(TypedDict):
    status_code: int
    status_msg: str
    log_pb: dict

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

class UserMiniType(TypedDict):
    uid: str
    short_id: str
    nickname: str
    signature: str
    avatar_larger: Dict[str, Any]
    avatar_thumb: Dict[str, Any]
    avatar_medium: Dict[str, Any]
    is_verified: int
    follow_status: int
    aweme_count: int
    following_count: int
    follower_count: int
    favoriting_count: int
    total_favorited: int
    is_block: int
    hide_search: int
    constellation: int
    creator_tag_list: str
    hide_location: int
    weibo_verify: str
    custom_verify: str
    unique_id: str
    private_relation_list: str
    special_lock: int
    need_recommend: int
    is_binded_weibo: int
    weibo_name: str
    weibo_schema: str
    weibo_url: str
    story_open: int
    story_count: int
    has_facebook_token: int
    has_twitter_token: int
    fb_expire_time: int
    tw_expire_time: int
    has_youtube_token: int
    youtube_expire_time: int
    room_id: int
    live_verify: int
    authority_status: int
    verify_info: str
    shield_follow_notice: int
    shield_digg_notice: int
    shield_comment_notice: int
    batch_unfollow_contain_tabs: str
    batch_unfollow_relation_desc: str
    verification_permission_ids: str
    with_commerce_entry: int
    verification_type: int
    enterprise_verify_reason: str
    is_ad_fake: int
    disable_image_comment_saved: int
    region: str
    account_region: str
    sync_to_toutiao: int
    commerce_user_level: int
    live_agreement: int
    platform_sync_info: str
    with_shop_entry: int
    is_discipline_member: int
    secret: int
    has_orders: int
    prevent_download: int
    show_image_bubble: int
    geofencing: List[Any]
    unique_id_modify_time: int
    video_icon: Dict[str, Any]
    ins_id: str
    google_account: str
    youtube_channel_id: str
    youtube_channel_title: str
    apple_account: int
    with_dou_entry: int
    with_fusion_shop_entry: int
    is_phone_binded: int
    accept_private_policy: int
    twitter_id: str
    twitter_name: str
    user_canceled: int
    has_email: int
    is_gov_media_vip: int
    live_agreement_time: int
    status: int
    avatar_uri: str
    follower_status: int
    neiguang_shield: int
    comment_setting: int
    duet_setting: int
    reflow_page_gid: int
    reflow_page_uid: int
    user_rate: int
    download_setting: int
    download_prompt_ts: int
    react_setting: int
    live_commerce: int
    cover_url: List[Any]
    show_gender_strategy: int
    language: str
    has_insights: int
    item_list: str
    user_mode: int
    user_period: int
    has_unread_story: int
    new_story_cover: str
    is_star: int
    cv_level: str
    type_label: str
    ad_cover_url: str
    comment_filter_status: int
    avatar_168x168: Dict[str, Any]
    avatar_300x300: Dict[str, Any]
    relative_users: str
    cha_list: str
    sec_uid: str
    urge_detail: Dict[str, Any]
    need_points: str
    homepage_bottom_toast: str
    aweme_hotsoon_auth: int
    can_set_geofencing: str
    room_id_str: str
    white_cover_url: str
    user_tags: str
    stitch_setting: int
    is_mix_user: int
    enable_nearby_visible: int
    ban_user_functions: List[Any]
    aweme_control: Dict[str, Any]
    user_not_show: int
    ky_only_predict: int
    user_not_see: int
    card_entries: str
    signature_display_lines: int
    display_info: str
    follower_request_status: int
    live_status: int
    new_friend_type: int
    is_not_show: int
    card_entries_not_display: str
    card_sort_priority: str
    show_nearby_active: int
    interest_tags: str
    school_category: int
    search_impr: Dict[str, Any]
    link_item_list: str
    user_permissions: str
    offline_info_list: str
    is_cf: int
    is_blocking_v2: int
    is_blocked_v2: int
    close_friend_type: int
    signature_extra: str
    max_follower_count: int
    personal_tag_list: str
    cf_list: str
    im_role_ids: str
    not_seen_item_id_list: str
    profile_mob_params: str
    contacts_status: int
    risk_notice_text: str
    follower_list_secondary_information_struct: str
    endorsement_info_list: str
    text_extra: str
    contrail_list: str
    data_label_list: str
    not_seen_item_id_list_v2: str
    is_ban: int
    special_people_labels: str
    special_follow_status: int
    familiar_visitor_user: str
    live_high_value: int
    awemehts_greet_info: str
    avatar_schema_list: str

class VideoCommentDetailType(TypedDict):
    cid: str
    text: str
    '''评论内容'''
    aweme_id: str
    '''作品id'''
    create_time: int
    digg_count: int
    status: int
    user: UserMiniType
    reply_id: str
    user_digged: int
    reply_comment: str
    text_extra: List[Any]
    label_text: str
    label_type: int
    reply_comment_total: int
    reply_to_reply_id: str
    is_author_digged: int
    stick_position: int
    user_buried: int
    label_list: str
    is_hot: int
    text_music_info: str
    image_list: str
    is_note_comment: int
    ip_label: str
    '''ip属地信息'''
    can_share: int
    item_comment_total: int
    level: int
    video_list: str
    sort_tags: str
    is_user_tend_to_reply: int
    content_type: int
    is_folded: int

class VideoCommentType(TypedDict):
    status_code: int
    comments: Optional[List[VideoCommentDetailType]]
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

class HomePageUserInfoType(TypedDict):
    uid: str
    secUid: str
    shortId: str
    realName: str
    remarkName: str
    nickname: str
    desc: str
    descExtra: List[Any]
    gender: int
    avatarUrl: str
    avatar300Url: str
    followStatus: int
    followerStatus: int
    awemeCount: int
    followingCount: int
    followerCount: int
    mplatformFollowersCount: int
    favoritingCount: int
    watchLaterCount: int
    totalFavorited: int
    userCollectCount: Dict[str, Any]
    uniqueId: str
    customVerify: str
    generalPermission: Dict[str, Any]
    punishRemindInfo: str
    age: int
    birthday: str
    country: str
    province: str
    city: str
    district: str
    school: str
    schoolVisible: str
    enterpriseVerifyReason: str
    secret: int
    userCanceled: int
    roomData: Dict[str, Any]
    shareQrcodeUrl: str
    shareInfo: Dict[str, Any]
    coverAndHeadImageInfo: Dict[str, Any]
    roomId: int
    isBlocked: int
    isBlock: int
    isBan: int
    favoritePermission: int
    showFavoriteList: int
    viewHistoryPermission: int
    ipLocation: str
    isNotShowBaseTag: str
    isGovMediaVip: int
    isStar: int
    hideLocation: str
    needSpecialShowFollowerCount: int
    isNotShow: int
    avatarAuditing: str
    continuationState: int
    im_role_ids: List[Any]
    roomIdStr: str
    isOverFollower: int

class AwemeAnchorInfoType(TypedDict):
    type: int
    id: str
    icon: Dict[str, Any]
    title: str
    open_url: str
    web_url: str
    mp_url: str
    title_tag: str
    content: str
    style_info: Dict[str, Any]
    extra: str
    log_extra: str

class AwemeMusicType(TypedDict):
    id: int
    id_str: str
    title: str
    author: str
    album: str
    cover_hd: Dict[str, Any]
    cover_large: Dict[str, Any]
    cover_medium: Dict[str, Any]
    cover_thumb: Dict[str, Any]
    play_url: Dict[str, Any]
    schema_url: str
    source_platform: int
    start_time: int
    end_time: int
    duration: int
    extra: str
    user_count: int
    position: str
    collect_stat: int
    status: int
    offline_desc: str
    owner_id: str
    owner_nickname: str
    is_original: int
    mid: str
    binded_challenge_id: int
    redirect: int
    is_restricted: int
    author_deleted: int
    is_del_video: int
    is_video_self_see: int
    owner_handle: str
    author_position: str
    prevent_download: int
    strong_beat_url: Dict[str, Any]
    unshelve_countries: str
    prevent_item_download_status: int
    external_song_info: List[Any]
    sec_uid: str
    avatar_thumb: Dict[str, Any]
    avatar_medium: Dict[str, Any]
    avatar_large: Dict[str, Any]
    preview_start_time: int
    preview_end_time: int
    is_commerce_music: int
    is_original_sound: int
    audition_duration: int
    shoot_duration: int
    reason_type: int
    artists: List[Any]
    lyric_short_position: str
    mute_share: int
    tag_list: str
    dmv_auto_show: int
    is_pgc: int
    is_matched_metadata: int
    is_audio_url_with_cookie: int
    matched_pgc_sound: Dict[str, Any]
    music_chart_ranks: str
    can_background_play: int
    music_status: int
    video_duration: int
    pgc_music_type: int
    author_status: int
    search_impr: Dict[str, Any]
    song: Dict[str, Any]
    artist_user_infos: str
    dsp_status: int
    musician_user_infos: str
    music_collect_count: int
    music_cover_atmosphere_color_value: str

class AwemeVideoPlayAddrType(TypedDict):
    uri: str
    url_list: List[Any]
    width: int
    height: int
    url_key: str
    data_size: int
    file_hash: str
    file_cs: str

class AwemeVideoType(TypedDict):
    play_addr: AwemeVideoPlayAddrType
    cover: Dict[str, Any]
    height: int
    width: int
    dynamic_cover: Dict[str, Any]
    origin_cover: Dict[str, Any]
    ratio: str
    bit_rate_audio: List[Any]
    big_thumbs: List[Any]
    meta: str
    bit_rate: List[Any]
    duration: int
    gaussian_cover: Dict[str, Any]
    audio: Dict[str, Any]
    play_addr_265: AwemeVideoPlayAddrType
    horizontal_type: int
    play_addr_h264: AwemeVideoPlayAddrType
    format: str
    is_long_video: int
    animated_cover: Dict[str, Any]
    is_source_HDR: int
    misc_download_addrs: str
    video_model: str

class AwemePostDetailAuthorType(TypedDict):
    uid: str
    ban_user_functions: None
    nickname: str
    cf_list: str
    link_item_list: str
    avatar_thumb: Dict[str, Any]
    avatar_schema_list: str
    signature_extra: str
    follow_status: int
    risk_notice_text: str
    private_relation_list: str
    follower_list_secondary_information_struct: str
    custom_verify: str
    can_set_geofencing: str
    batch_unfollow_contain_tabs: str
    display_info: str
    verification_permission_ids: str
    need_points: str
    share_info: Dict[str, Any]
    familiar_visitor_user: str
    homepage_bottom_toast: str
    batch_unfollow_relation_desc: str
    enterprise_verify_reason: str
    is_ad_fake: int
    account_cert_info: str
    interest_tags: str
    user_tags: str
    profile_mob_params: str
    card_entries_not_display: str
    not_seen_item_id_list: str
    card_entries: str
    prevent_download: int
    text_extra: str
    sec_uid: str
    im_role_ids: str
    follower_status: int
    not_seen_item_id_list_v2: str
    contrail_list: str
    data_label_list: str
    cover_url: List[Any]
    user_permissions: str
    offline_info_list: str
    endorsement_info_list: str
    card_sort_priority: str
    personal_tag_list: str
    white_cover_url: str
    creator_tag_list: str
    special_people_labels: str

class AwemePostDetailType(TypedDict):
    aweme_id: str
    desc: str
    create_time: int
    author: AwemePostDetailAuthorType
    music: AwemeMusicType
    trends_infos: str
    video: AwemeVideoType
    share_url: str
    user_digged: int
    statistics: Dict[str, Any]
    status: Dict[str, Any]
    visual_search_info: Dict[str, Any]
    text_extra: List[Any]
    is_top: int
    video_game_data_channel_config: Dict[str, Any]
    share_info: Dict[str, Any]
    mark_largely_following: int
    video_labels: str
    jump_tab_info_list: str
    is_ads: int
    flash_mob_trends: int
    duration: int
    aweme_type: int
    item_title: str
    life_anchor_show_extra: Dict[str, Any]
    image_infos: str
    risk_infos: Dict[str, Any]
    media_type: int
    image_comment: Dict[str, Any]
    position: str
    uniqid_position: str
    comment_list: str
    author_user_id: int
    chapter_bar_color: str
    geofencing: List[Any]
    entertainment_product_info: Dict[str, Any]
    activity_video_type: int
    region: str
    video_text: str
    author_mask_tag: int
    collect_stat: int
    label_top_text: str
    promotions: List[Any]
    group_id: str
    prevent_download: int
    nickname_position: str
    challenge_position: str
    slides_music_beats: str
    enable_comment_sticker_rec: int
    packed_clips: str
    origin_text_extra: str
    long_video: str
    yumme_recreason: str
    image_crop_ctrl: int
    disable_relation_bar: int
    video_share_edit_status: int
    interaction_stickers: str
    authentication_token: str
    origin_comment_ids: str
    commerce_config_data: str
    xigua_base_info: Dict[str, Any]
    video_control: Dict[str, Any]
    aweme_control: Dict[str, Any]
    original: int
    is_24_story: int
    anchor_info: AwemeAnchorInfoType
    voice_modify_id_list: str
    reply_smart_emojis: str
    anchors: str
    hybrid_label: str
    geofencing_regions: str
    is_use_music: int
    tts_id_list: str
    is_story: int
    dislike_dimension_list_v2: str
    collection_corner_mark: int
    friend_interaction: int
    cover_labels: str
    caption: str
    ref_voice_modify_id_list: str
    guide_btn_type: int
    create_scale_type: str
    ref_tts_id_list: str
    images: str
    relation_labels: str
    horizontal_type: int
    boost_status: int
    impression_data: Dict[str, Any]
    distribute_circle: Dict[str, Any]
    user_recommend_status: int
    libfinsert_task_id: str
    social_tag_list: str
    suggest_words: Dict[str, Any]
    show_follow_button: Dict[str, Any]
    duet_aggregate_in_music_tab: int
    is_duet_sing: int
    comment_permission_info: Dict[str, Any]
    original_images: str
    series_paid_info: Dict[str, Any]
    img_bitrate: str
    comment_gid: int
    image_album_music_info: Dict[str, Any]
    video_tag: List[Any]
    is_collects_selected: int
    chapter_list: str
    feed_comment_config: Dict[str, Any]
    is_image_beat: int
    dislike_dimension_list: str
    standard_bar_info_list: str
    photo_search_entrance: Dict[str, Any]
    danmaku_control: Dict[str, Any]
    is_life_item: int
    image_list: str
    component_info_v2: str
    common_bar_info: str
    item_warn_notification: Dict[str, Any]


class AwemePostResType(TypedDict):
    status_code: int
    min_cursor: int
    max_cursor: int
    has_more: int
    aweme_list: List[AwemePostDetailType]
    time_list: List[str]
    log_pb: Dict[str, Any]
    request_item_cursor: int
    post_serial: int
    replace_series_cover: int



