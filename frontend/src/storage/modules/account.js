import ls from '../../utils/localstorage.js'

export default {
  namespaced: true,
  state: {
    token: ls.get('USER_TOKEN'),
    expireTime: ls.get('EXPIRE_TIME'),
    user: ls.get('USERNAME'),
    password: ls.get('PASSWORD'),
    permissions: ls.get('PERMISSIONS'),
    roles: ls.get('ROLES')
  },
  mutations: {
    setToken (state, val) {
      ls.save('USER_TOKEN', val)
      state.token = val
    },
    setExpireTime (state, val) {
      ls.save('EXPIRE_TIME', val)
      state.expireTime = val
    },
    setUser (state, val) {
      ls.save('USERNAME', val)
      state.user = val
    },
    setPassword (state, val) {
      ls.save('PASSWORD', val)
      state.user = val
    },
    setPermissions (state, val) {
      ls.save('PERMISSIONS', val)
      state.permissions = val
    },
    setRoles (state, val) {
      ls.save('ROLES', val)
      state.roles = val
    }
  }
}
