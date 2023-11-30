export interface RequestOptions {
  // Whether to process the request result
  isTransformResponse?: boolean;
}

/**
 * 封装请求返回数据的抽象类
 */
export interface IResponse<T = any> {
  code: number | string;
  result: T;
  message: string;
  status: string | number;
}
