/** 
 * 用户组管理: 
 * 
 * user: 用户组管理
 * admin: 管理员
 */
export type RoleType = '' | '*' | 'admin' | 'user';

/** 
 * 用户信息 Storage
 * 
 * user_id: 用户名
 * user_refresh: 用于刷新的 token
 * user_token:
 */
export interface UserState {
  user_id: any;
  user_name: any;
  user_access: any;
  user_avatar: any;
  user_refresh: any;
  token_expire_time: any;

  is_admin: any

  admin_user_id: any;
  admin_user_name: any;
  admin_user_token: any;
  admin_user_avatar: any;

  remember_me: any;
}
