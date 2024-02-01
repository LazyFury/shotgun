<template>
    <div>
        <ElCard shadow="never">
            <!-- {{ $route.meta }} -->
            <div class="flex flex-row">
                <div>
                    <h1 class="mb-0 mt-2">{{ meta.title }}</h1>
                    <p class="text-gray">{{ meta.description }}</p>
                </div>
                <div class="flex-grow">
                    <div class="flex flex-row-reverse">

                    </div>
                </div>
            </div>
            <ElDivider></ElDivider>
            <ElForm :inline="true" :model="searchForm" class="mb-2">
                <ElFormItem v-for="field in searchFormFields" :key="field.name" :label="field.label" :prop="field.name" :class="[]" :style="{'min-width':field.width || '100px'}">
                    <!-- select  -->
                    <ElSelect v-if="field.type === 'select'" v-model="searchForm[field.name]" :placeholder="field.placeholder" clearable>
                        <ElOption v-for="option in field.options" :key="option.value" :label="option.label" :value="option.value"></ElOption>
                    </ElSelect>

                    <ElInput v-else v-model="searchForm[field.name]" :placeholder="field.placeholder"></ElInput>

                </ElFormItem>
                <ElFormItem>
                    <ElButton type="primary" @click="submitSearch">
                        <Icon icon="heroicons-solid:magnifying-glass" class="mt-0px mr-4px"></Icon>
                        <span>{{ $t("search") }}</span>
                    </ElButton>
                    <!-- reset  -->
                    <ElButton type="default" @click="resetSearchForm">
                        <Icon icon="la:trash-restore-alt" class="mt-0px mr-4px"></Icon>
                        <span>{{ $t("reset") }}</span>
                    </ElButton>
                </ElFormItem>
            </ElForm>


            <!-- betch actions  -->
            <div class="mb-2">
                <ElButton type="primary" @click="add">
                    <Icon icon="ant-design:plus-outlined"></Icon>
                    <span>添加</span>
                </ElButton>
                <ElButton :loading="loading" type="default" @click="load">
                    <Icon v-if="!loading" icon="ant-design:reload-outlined"></Icon>
                    <span>{{$t("refresh")}}</span>    
                </ElButton>

                <!-- divider vertical  -->
                <ElDivider direction="vertical" class="mx-4"></ElDivider>

                <ElButton :type="action.btnType" @click="batchAction(action.action)" v-for="action in meta.table?.batchActions || []" :key="action.name">
                    {{ action.label }}
                </ElButton>
            </div>
            <ElTable ref="tableRef" v-loading="loading" :data="tableData" :border="true" stripe @sort-change="handleSortChange">
                <!-- selection  -->
                <ElTableColumn type="selection" width="55"></ElTableColumn>
                <ElTableColumn v-for="column in columns" :key="column.key" :sortable="column.sortable ? 'custom' : false" :label="column.title">
                    <template #default="{row}">
                        {{ column.render(row) }}
                    </template>
                </ElTableColumn>
            </ElTable>

            <!-- pagination  -->
            <div class="flex mt-2">
                <ElPagination 
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="pagination.total"></ElPagination>
            </div>

            
        </ElCard>

        <ElDialog title="提示" v-model="editModal">
            <Form :fields="meta.addForm.fields"></Form>
        </ElDialog>
    </div>
</template>
<script>
import { ElPagination } from 'element-plus';
import { request } from '@/api/request';
import Form from '@/views/components/Form.vue'

export default {
    components: { ElPagination,Form },
    props: {},
    data() {
        return {
            meta: this.$route.meta,
            searchForm: {},
            pagination: {
                currentPage: 1,
                pageSize: 10,
                total: 1000
            },
            tableData:[],
            loading:false,
            editModal:false
        };
    },
    watch: {},
    computed: {
        searchFormFields() {
            return this.meta.searchForm?.fields || []
        },
        columns() {
            return (this.meta.table?.columns || []).map(column => {
                return {
                    ...column,
                    render: (row) => {
                        return row[column.key]
                    }
                }
            })
        }
    },
    methods: {
        add(){
            this.editModal = true
        },
        submitSearch(){
            console.log(this.searchForm)
            this.load()
        },
        resetSearchForm(){
            this.searchForm = {}
            this.load()

            // reset table sort
            this.$refs.tableRef.clearSort()
        },
        load(){
            this.loading = true
            request({
                url: this.meta.api,
                method: 'get',
                params: {
                    page: this.pagination.currentPage,
                    pageSize: this.pagination.pageSize,
                    ...this.searchForm
                }
            }).then(res=>{
                let data = res.data.data || {}
                this.tableData = data?.list || []
                let {size,page,total} = data?.pageable
                this.pagination = {
                    pageSize:size,
                    currentPage:page,
                    total
                }

            }).finally(()=>{
                setTimeout(()=>{
                    this.loading = false
                }, 500)
            })
        },
        handleSortChange({column,order}){
            if(!order)return
            let {no} = column
            let col = this.meta.table.columns[no-1]
            this.searchForm.order_by = col.key+(order === 'ascending' ? '_asc' : '_desc')
            console.log(col)
            this.load()
        },
        getTableSelection(){
            return this.$refs.tableRef?.getSelectionRows() || []
        },
        getTableSelectionIds(){
            return this.getTableSelection().map(item=>item.id)
        },
        batchAction(key){
            let actionMap = {
                delete: this.batchDelete
            }
            actionMap[key]?.()
        },
        batchDelete(){
            let ids = this.getTableSelectionIds()
            if(!ids.length)return
            this.$confirm('确定删除选中的数据吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                console.log(ids)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });          
            });
        }
    },
    created() { },
    mounted() {
        this.load()
    }
};
</script>
<style lang="scss" scoped></style>