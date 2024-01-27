import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'virtual:uno.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import { Icon } from '@iconify/vue';

import App from './App.vue'
import router from './router'
import axios from 'axios'
import { request } from './api/request'
import useTranslateStore from './pinia/translate'
import zhCN from './i18n/zh-cn/main.js'

const app = createApp(App)
app.use(ElementPlus)
app.use(createPinia())
app.use(function (vm) {
    const translateStore = useTranslateStore()
    vm.component("Icon", Icon)
    vm.config.globalProperties.$t = translateStore.getKey
    setTimeout(() => {
        translateStore.setMessages("zh-cn",{
            "AdminTitle": "Element Vite Admin ｜ EVA",
            "首页":"控制台",
            ...zhCN,
        })
        translateStore.setMessages("en",{
            "AdminTitle": "Element Vite Admin ｜ EVA",
            "首页":"Dashboard"
        })
    }, 200);

    // setTimeout(() => {
    //     translateStore.setLocale("en")
    // }, 3000);
})

const registerRoute = (menu) => {
    if (menu.component) {
        // register router
        const component = () => import(/* @vite-ignore */ `/src/views/${menu.component}.vue` /* @vite-ignore */)
        const route = {
            path: menu.path,
            name: menu.key,
            component: component,
            meta:{
                title:menu.title,
                key:menu.key,
                api:menu.api || "",
            }
        }
        router.addRoute('Admin', route)
    }
    if (menu.children) {
        for (let i = 0; i < menu.children.length; i++) {
            registerRoute(menu.children[i])
        }
    }
}

request.get('/menus').then(res => {
    let menus = res.data.data?.menus || []
    for (let i = 0; i < menus.length; i++) {
        let el = menus[i]
        registerRoute(el)
    }
    app.use(router)
    app.mount('#app')
})