import {notification} from 'ant-design-vue';

const notice = {
    success(message = "", description = "", duration = 4.5) {
        notification["success"]({
            message: message,
            description: description,
            duration: duration
        });
    },
    info(message) {

    },
    warning(message) {

    },
    error(message, description) {
        notification["error"]({
            message: message,
            description: description,
        });
    }
}
export default notice
