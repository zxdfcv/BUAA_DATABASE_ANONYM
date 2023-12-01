import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { IResponse } from './type';
import { BASE_URL } from '/@/store/constants'
import { useUserStore } from '/@/store';

let waiting = [] as any;
let getting = false;

const addRequest = (config) => {
  waiting.push(config);
}
const service: AxiosInstance = axios.create({
  baseURL: BASE_URL + '',
  timeout: 15000,
});
/**
 * 封装 Request 实例完成异步请求
 * @param {AxiosRequestConfig} config
 */
 const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
  const conf = config;
  return new Promise((resolve, reject) => {
    service.request<any, AxiosResponse<IResponse>>(conf).then((res: AxiosResponse<IResponse>) => {
      const data = res.data
      resolve(data as T);
    }).catch(err => {
      reject(err)
    });
  });
};

/* 封装 GET/POST 方法 */
export function get<T = any>(config: AxiosRequestConfig): Promise<T> {
  return request({ ...config, method: 'GET' });
}

export function post<T = any>(config: AxiosRequestConfig): Promise<T> {
  return request({ ...config, method: 'POST' });
}
const retryRequest = () => {
  console.log("Retry failed request");
  waiting.forEach(config => request(config));
  waiting = [];
}

const refresh = () => {
  const userStore = useUserStore();
  if (!getting) {
    getting = true;
    let refreshToken = userStore.user_refresh;
    if (refreshToken) {
      post({url: '/token/refresh/', params: {}, data: {refresh: refreshToken}}).then((res) => {
        
        if (res.access === null) {
          /* 长 Token 失效，直接登出 */
          getting = false;
          userStore.logout();
        } else {
          /* 长 Token 未过期，重新更新 */
          // userStore.user_refresh = res.data.refresh; '/refresh' 接口需要同时更新 freshToken 吗 -> 不需要
          userStore.user_access = res.access;
          userStore.token_expire_time = Date.now() + 1000 * 60 * 30;
          getting = false;
          retryRequest();
        }
      })
    }
  }
}


/* 允许不携带 Token 访问的 Api 白名单 */
const whiteList = ['/login', '/register', '/token/refresh/']

/* 拦截 Request 添加请求头 */
service.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const userStore = useUserStore();
  /* TODO: 未处理 Admin 的请求头 */

    // config.headers.ADMINTOKEN = localStorage.getItem(ADMIN_USER_TOKEN)

    if (whiteList.includes(config.url as string)) {
      return config;
    } else if (userStore.token_expire_time > Date.now()) { /* 客户端判断 Access token valid */
    config.headers.TOKEN = userStore.user_access;
    } else { /* Access token invalid */
      userStore.user_access = undefined;
      addRequest(config)
      refresh()
    }
    return config;
  }, (error: AxiosError) => {
    return Promise.reject(error);
  });


/* 拦截 Response 异常返回 */
service.interceptors.response.use((response: AxiosResponse) => {
  // let { config, data } = response;
  // return new Promise((resolve, reject) => {
  //   if (response.status === 401 && data.code === "access_token_not_valid") {
  //     /* 短 token 失效 */
  //     userStore.user_access = undefined;
  //     addRequest(() => resolve(request(config)))
  //     refresh()
  //   } else {
  //     resolve(data)
  //   }
  // })}

    if (response.status === 200) {
      return response /* 正常返回 */
    } else {
      return Promise.reject(response.data)
    }
  }, (error: any) => {
    /* 异常状态码处理 */
    switch (error.response.status) {
      case 404:
        /* TODO: 跳转 404 页面 */
        break;
      case 403:
        /* TODO: 跳转 Forbidden 页面 */
        break;
      case 401:
        /* TODO: 跳转 Login 页面 */
        break;
      default:
        console.log("Undetected error code as " + error.response.status);
    }
    return Promise.reject(error)
  },
);



export default request;

export type { AxiosInstance, AxiosResponse };

export { refresh }