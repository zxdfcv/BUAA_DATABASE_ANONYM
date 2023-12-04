const BASE_URL = 'http://127.0.0.1:8000'
// const BASE_URL = 'http://118.178.121.33:80'

const USER_ID = 'user_id'
const USER_NAME = 'user_name'
const USER_ACCESS = 'user_access'
const USER_AVATAR = 'user_avatar'
const USER_REFRESH = 'user_refresh'
const TOKEN_EXPIRE_TIME = 'token_expire_time'

const ADMIN_USER_ID = 'admin_user_id'
const ADMIN_USER_NAME = 'admin_user_name'
const ADMIN_USER_TOKEN = 'admin_user_token'
const ADMIN_USER_AVATAR = 'admin_user_avatar'

const REMEMBER_ME = 'remember_me'
const EXPIRE_MINUTE = 30 /* ACCESS TOKEN 过期需要的时间，以 minute 计算 */
const EXPIRE_FRESH_HOUR = 3; /* REFRESH TOKEN 过期需要的时间，以 hour 计算 */


export {
    BASE_URL, 
    USER_ACCESS, USER_NAME, USER_ID, USER_AVATAR, USER_REFRESH, TOKEN_EXPIRE_TIME,
    ADMIN_USER_ID,ADMIN_USER_NAME,ADMIN_USER_TOKEN, ADMIN_USER_AVATAR,
    REMEMBER_ME, EXPIRE_MINUTE, EXPIRE_FRESH_HOUR
}
