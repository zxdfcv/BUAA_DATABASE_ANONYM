/**
 * @param {number} time
 * @param {string} option
 * @returns {string}
 */
export function formatTime(timeString: any){
    let time = Date.parse(timeString)
    if (('' + time).length === 10) {
        time = parseInt(String(time)) * 1000
    } else {
        time = +time
    }
    const d = +new Date(time)
    const now = Date.now()

    const diff = (now - d) / 1000

    if (diff < 30) {
        return '刚刚'
    } else if (diff < 3600) {
        // less 1 hour
        return Math.ceil(diff / 60) + '分钟前'
    } else if (diff < 3600 * 24) {
        return Math.ceil(diff / 3600) + '小时前'
    } else {
        return timeString
    }
}