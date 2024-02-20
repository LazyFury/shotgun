<template>

    <!-- textarea  -->
    <ElInput @change="handleUpdate" v-model="value" v-if="field.type == 'textarea'" type="textarea" :placeholder="field.placeholder"></ElInput>
    <!-- password  -->
    <ElInput @change="handleUpdate" v-model="value" v-else-if="field.type == 'password'" type="password" :placeholder="field.placeholder">
    </ElInput>
    <!-- select  -->
    <ElSelect @change="handleUpdate" v-model="value" v-else-if="field.type == 'select'" :placeholder="field.placeholder">
        <ElOption v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></ElOption>
    </ElSelect>
    <!-- switch -->
    <ElSwitch @change="handleUpdate" v-model="value" v-else-if="field.type == 'switch'" :active-text="field.checkedChildren"></ElSwitch>
    <!-- input  -->
    <ElInput v-model="value" @change="handleUpdate" :type="field.epInputType || 'text'" v-else :placeholder="field.placeholder">
        <!-- suffix  -->
        <template v-if="field.suffix" #suffix>
            <div>
                {{ field.suffix }}
            </div>
        </template>
        <!-- prefix -->
        <template v-if="field.prefix" #prefix>
            <div>
                {{ field.prefix }}
            </div>
        </template>
    </ElInput>
</template>
<script>
import { request } from '@/api/request'
export default {
    components: {},
    props: {
        field: {
            type: Object,
            default: () => ({})
        },
        modelValue: {
            type: [String, Number, Array, Object],
            default: () => ''
        }
    },
    data() {
        return {
            options: [],
            value: ""
        };
    },
    watch: {
        modelValue: {
            handler(val) {
                if(this.field.type == 'switch') return this.value = !!val
                this.value = val
            },
            immediate: true
        },
        value: {
            handler(val) {
                this.$emit('update:modelValue', val)
            }
        }
    },
    computed: {},
    methods: {
        handleUpdate(val) {
            this.$emit('update:modelValue', val)
        }
    },
    created() { },
    mounted() {
        if (this.field.remoteDataApi) request.get(this.field.remoteDataApi).then(res => {
            this.options = (res.data?.data?.list || []).map(v => ({
                label: v[this.field.props?.label || 'name'] || v[this.field.props?.value || 'title'],
                value: v[this.field.props?.value || 'id']
            }))
        })
    }
};
</script>
<style lang="scss" scoped></style>