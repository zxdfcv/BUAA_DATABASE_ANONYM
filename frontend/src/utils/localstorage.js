let ls = {
    save(key, value) {
        localStorage.setItem(key, JSON.stringify(value))
    },
    get(key, defaultValue = {}) {
        if (key === 'time') {
            console.log("now is " + new Date().getTime() + "\nexpire time is " + JSON.parse(localStorage.getItem('EXPIRE_TIME')))
        }
        if (new Date().getTime() >= JSON.parse(localStorage.getItem('EXPIRE_TIME'))) {
            localStorage.removeItem('USER_TOKEN')
        }
        return JSON.parse(localStorage.getItem(key)) || defaultValue
    },
    remove(key) {
        localStorage.removeItem(key)
    },
    clear() {
        localStorage.clear()
    }
}

export default ls
