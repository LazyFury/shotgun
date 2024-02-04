<template>
    <ElInput v-if="field.type == 'textarea'" type="textarea" :placeholder="field.placeholder"></ElInput>
    <ElInput v-else :placeholder="field.placeholder"></ElInput>
</template>
<script>
export default {
    components: {},
    props: {
        field: {
            type: Object,
            default: () => ({})
        },
    },
    data() {
        return {
        };
    },
    watch: {},
    computed: {},
    methods: {},
    created() { },
    mounted() { }
};
</script>
<style lang="scss" scoped></style>