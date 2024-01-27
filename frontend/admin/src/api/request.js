import axios from 'axios'
import config from '../config'

const createAxiosInstance = (baseURL,opt={}) => {
    const instance = axios.create({
        baseURL: baseURL,
        timeout: 1000,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        ...opt
    });

    instance.interceptors.request.use(function (config) {
        // Do something before request is sent
        return config;
    })

    instance.interceptors.response.use(function (response) {
        // Do something with response data
        return response;
    }, function (error) {
        // Do something with response error
        return Promise.reject(error);
    });

    return instance
}

export const request = createAxiosInstance(config.apiURL) 