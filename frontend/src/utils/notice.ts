import { notification } from 'ant-design-vue';

const openNotification = ({ type, message, description }) => {
    notification[type]({
      message: message,
      description: description
    });
  };

export { openNotification };