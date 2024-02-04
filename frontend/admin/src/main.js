
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/scss/main.scss'
// unocss 
import 'virtual:uno.css'

// element-plus
import ElementPlus from 'element-plus'
import './assets/scss/element-variables.scss'
// dark theme 
import 'element-plus/theme-chalk/dark/css-vars.css'

import ElzhCn from 'element-plus/dist/locale/zh-cn.mjs'
// end element-plus

// iconify
import { Icon } from '@iconify/vue';
// end iconify

import App from './App.vue'
import router from './router'
import axios from 'axios'

// request
import { request } from './api/request'

// translate
import useTranslateStore from './pinia/translate'
import zhCN from './i18n/zh-cn/main.js'
// end translate

import config from './config'
import dayjs from 'dayjs'
import numeral from 'numeral'

const app = createApp(App)
app.use(ElementPlus, { locale: ElzhCn })
app.use(createPinia())
app.use(function (vm) {
    vm.config.globalProperties.$dayjs = dayjs
    vm.config.globalProperties.$numeral = numeral

    vm.config.globalProperties.$img = (url) => {
        console.log(url)    
        const target =  config.imgURL + url
        console.log(target)
        return target
    }

    const translateStore = useTranslateStore()
    vm.component("Icon", Icon)
    vm.config.globalProperties.$t = translateStore.getKey
    setTimeout(() => {
        const serverData = {
            "zh-cn": {
                "AdminTitle": "Element Vite Admin ｜ EVA",
                "首页":"控制台",
                "welcome.documentation":"欢迎 {user} 使用文档",
            },
        }
        translateStore.setMessages("zh-cn",{
            ...zhCN,
            ...(serverData["zh-cn"] || {})
        })
    }, 200);

    translateStore.setLocale("zh-cn")

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
                ...(menu.meta || {})
            }
        }
        if(!menu.parent){
            menu.parent = 'layout' //default layout
        }
        if(menu.parent){
            const parentRoute = router.getRoutes().find(el => el.name === menu.parent)
            if(parentRoute){
                if(!parentRoute.children){
                    parentRoute.children = []
                }
                parentRoute.children.push(route)
            }
            router && router.addRoute(parentRoute.name, route)
        }else{
            router.addRoute('Admin', route)
        }
    }
    if (menu.children) {
        for (let i = 0; i < menu.children.length; i++) {
            registerRoute(menu.children[i])
        }
    }
}

request.get('/menus',{
    noMsgAlert:true
}).then(res => {
    let menus = res.data.data?.menus || []
    for (let i = 0; i < menus.length; i++) {
        let el = menus[i]
        registerRoute(el)
    }
    app.use(router)
    app.mount('#app')
    
}).catch(() => {
    app.use(router)
    app.mount('#app')
})