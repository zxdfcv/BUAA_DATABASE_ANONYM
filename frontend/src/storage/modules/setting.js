import ls from '../../utils/localstorage.js'

export default {
  namespaced: true,
  state: {
    sidebar: {
      opened: true
    },
    settingBar: {
      opened: false
    },
    isMobile: false,
    theme: ls.get('THEME', 'light'),
    layout: ls.get('LAYOUT', 'side'),
    systemName: 'Salty Fish',
    copyright: `${new Date().getFullYear()} <a>FanK</a>`,
    multipage: getBooleanValue(ls.get('MULTIPAGE'), true),
    fixSiderbar: getBooleanValue(ls.get('FIX_SIDERBAR'), true),
    fixHeader: getBooleanValue(ls.get('FIX_HEADER'), true),
    colorList: [
      'rgb(245, 34, 45)',
      'rgb(250, 84, 28)',
      'rgb(250, 173, 20)',
      'rgb(66, 185, 131)',
      'rgb(82, 196, 26)',
      'rgb(24, 144, 255)',
      'rgb(47, 84, 235)',
      'rgb(114, 46, 209)'
    ],
    color: ls.get('COLOR', 'rgb(24, 144, 255)')
  },
  mutations: {
    setDevice (state, isMobile) {
      state.isMobile = isMobile
    },
    setTheme (state, theme) {
      ls.save('THEME', theme)
      state.theme = theme
    },
    setLayout (state, layout) {
      ls.save('LAYOUT', layout)
      state.layout = layout
    },
    setMultipage (state, multipage) {
      ls.save('MULTIPAGE', multipage)
      state.multipage = multipage
    },
    setSidebar (state, type) {
      state.sidebar.opened = type
    },
    fixSiderbar (state, flag) {
      ls.save('FIX_SIDERBAR', flag)
      state.fixSiderbar = flag
    },
    fixHeader (state, flag) {
      ls.save('FIX_HEADER', flag)
      state.fixHeader = flag
    },
    setSettingBar (state, flag) {
      state.settingBar.opened = flag
    },
    setColor (state, color) {
      ls.save('COLOR', color)
      state.color = color
    }
  }
}

function getBooleanValue (value, defaultValue) {
  if (Object.is(value, null)) {
    return defaultValue
  }
  if (JSON.stringify(value) !== '{}') {
    return value
  } else {
    return false
  }
}
