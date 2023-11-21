import Vuex from 'vuex'
import account from './modules/account'
import setting from './modules/setting'

export default new Vuex.Store({
  modules: {
    account,
    setting
  }
})
