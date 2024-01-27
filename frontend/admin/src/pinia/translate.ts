import { defineStore } from "pinia"
import { ref } from "vue"


export const useTranslateStore = defineStore('translate', () => {
    const supportedLocales = ref(['en', 'fr','zh-cn'])
    const localesToDisplay = ref({
        'en': 'English',
        'fr': 'Français',
        'zh-cn': '简体中文'
    })
    const locale = ref('zh-cn')
    const messages = ref({})

    function setLocale(newLocale) {
        if (!supportedLocales.value.includes(newLocale)) {
            throw new Error(`Locale ${newLocale} is not supported`)
        }
        locale.value = newLocale
    }

    function setMessages(key,_messages) {
        messages.value[key] = _messages
    }

    function getMessage(local){
        return messages.value[local] || {}
    }
    
    function getKey(key) {
        if(!getMessage(locale.value)[key]){
            setTimeout(() => {
                // 仅上报
                console.log(`key:${key} not found in locale:${locale.value}`)
            }, 100);
        }
        return getMessage(locale.value)[key] || key + ""
    }

    function getLocaleToDisplay(_locale) {
        if(!_locale){
            _locale = locale.value
        }
        return localesToDisplay.value[_locale] || _locale
    }

    return { locale, messages, setLocale, setMessages, getKey,getLocaleToDisplay }
})

export default useTranslateStore