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
                <ElFormItem v-for="field in searchFormFields" :key="field.name" :label="field.label" :prop="field.name"
                    :class="[]" :style="{ 'min-width': field.width || '100px' }">
                    <!-- select  -->
                    <ElSelect v-if="field.type === 'select'" v-model="searchForm[field.name]"
                        :placeholder="field.placeholder" clearable>
                        <ElOption v-for="option in field.options" :key="option.value" :label="option.label"
                            :value="option.value"></ElOption>
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
                    <span>{{ $t("refresh") }}</span>
                </ElButton>

                <!-- divider vertical  -->
                <ElDivider direction="vertical" class="mx-4"></ElDivider>

                <ElButton :type="action.btnType" @click="batchAction(action.action)"
                    v-for="action in meta.table?.batchActions || []" :key="action.name">
                    {{ action.label }}
                </ElButton>

                <!-- 导出 -->
                <ElButton type="default" @click="exportData">
                    <Icon icon="ant-design:export-outlined"></Icon>
                    <span>导出</span>
                </ElButton>
            </div>
            <ElTable ref="tableRef" v-loading="loading" :data="tableData" :border="true" stripe
                @sort-change="handleSortChange">
                <!-- selection  -->
                <ElTableColumn type="selection" width="55"></ElTableColumn>
                <ElTableColumn v-for="column in columns" :key="column.key" :sortable="column.sortable ? 'custom' : false"
                    :label="column.title">
                    <template #default="{ row }" v-if="!column.slot">
                        <div :class="[column.className]" v-if="column.type=='render'">
                            {{ column.render(row) }}
                        </div>
                        <!-- switch  -->
                        <ElSwitch v-else-if="column.type=='switch'" v-model="row[column.key]" active-color="#13ce66"
                            inactive-color="#ff4949" active-text="" inactive-text="" disabled></ElSwitch>
                        <!-- checkbox  -->
                        <ElCheckbox v-else-if="column.type=='checkbox'" v-model="row[column.key]" disabled></ElCheckbox>

                        <!-- select  -->
                        <ElSelect v-else-if="column.type=='select'" v-model="row[column.key]" :placeholder="column.placeholder"
                            clearable>
                            <ElOption v-for="option in column.options" :key="option.value" :label="option.label"
                                :value="option.value"></ElOption>
                        </ElSelect>
                    </template>
                    <template v-if="column.slot" #default="{row}">
                        <slot :name="column.slot" :row="row"></slot>
                    </template>
                </ElTableColumn>
            </ElTable>

            <!-- pagination  -->
            <div class="flex mt-2">
                <ElPagination layout="total, sizes, prev, pager, next, jumper" :total="pagination.total"></ElPagination>
            </div>
        </ElCard>

        <slot name="addModal">
            <ElDialog v-if="meta.addForm" title="提示" v-model="editModal">
                <Form :fields="meta.addForm.fields"></Form>
            </ElDialog>
        </slot>
    </div>
</template>
<script>
import { ElPagination } from 'element-plus';
import { request } from '@/api/request';
import Form from '@/views/components/Form.vue'

export default {
    components: { ElPagination, Form },
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
            tableData: [],
            loading: false,
            editModal: false
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
                    type:column.type || 'render',
                    render: (row) => {
                        if(column.slot) return ""
                        if(column.formatter) {
                            let {type,key,mapping_key,data=[],def,formatStr="",prefix="",suffix=""} = column.formatter || {}
                            let formatConfig = column.formatter
                            if(type === 'mapping') {
                                console.log(data)
                                console.log(row[column.key])
                                return data.find(item=>item[key] == row[column.key])?.[mapping_key] || def || ""
                            }

                            if(type === 'date') {
                                return row[column.key] ? this.$dayjs(row[column.key]).format('YYYY-MM-DD HH:mm:ss') : ''
                            }

                            if(type === 'datetime') {
                                return row[column.key] ? this.$dayjs(row[column.key]).format('YYYY-MM-DD HH:mm:ss') : ''
                            }

                            // number 
                            if(type === 'number') {
                                let result = row[column.key] ? this.$numeral(row[column.key]).format(formatStr || '0,0') : ''
                                return `${prefix}${result}${suffix}`
                            }

                            // bool 
                            if(type === 'boolean') {
                                return row[column.key] ? (formatConfig.trueText || '是') : (formatConfig.falseText || '否')
                            }
                        }
                        return row[column.key]
                    }
                }
            })
        }
    },
    methods: {
        add() {
            this.editModal = true
        },
        submitSearch() {
            console.log(this.searchForm)
            this.load()
        },
        resetSearchForm() {
            this.searchForm = {}
            this.load()

            // reset table sort
            this.$refs.tableRef.clearSort()
        },
        load() {
            this.loading = true
            request({
                url: this.meta.api,
                method: 'get',
                params: {
                    page: this.pagination.currentPage,
                    pageSize: this.pagination.pageSize,
                    ...this.searchForm
                }
            }).then(res => {
                let data = res.data.data || {}
                this.tableData = data?.list || []
                let { size, page, total } = data?.pageable
                this.pagination = {
                    pageSize: size,
                    currentPage: page,
                    total
                }

            }).finally(() => {
                setTimeout(() => {
                    this.loading = false
                }, 500)
            })
        },
        handleSortChange({ column, order }) {
            if (!order) return
            let { no } = column
            let col = this.meta.table.columns[no - 1]
            this.searchForm.order_by = col.key + (order === 'ascending' ? '_asc' : '_desc')
            console.log(col)
            this.load()
        },
        getTableSelection() {
            return this.$refs.tableRef?.getSelectionRows() || []
        },
        getTableSelectionIds() {
            return this.getTableSelection().map(item => item.id)
        },
        batchAction(key) {
            let actionMap = {
                delete: this.batchDelete
            }
            actionMap[key]?.()
        },
        batchDelete() {
            let ids = this.getTableSelectionIds()
            if (!ids.length) return
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
        },
        exportData() {
            console.log('export')
            request({
                url: this.meta.api + '.export',
                method: 'get',
                responseType: 'blob',
                params: {
                    ...this.searchForm
                },
                binary: true
            }).then(res => {
                let blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
                let url = window.URL.createObjectURL(blob)
                let link = document.createElement('a')
                link.style.display = 'none'
                link.href = url
                link.setAttribute('download', `export-${this.meta.title}-${this.$dayjs().format('YYYYMMDDHHmmss')}.xlsx`)
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
                window.URL.revokeObjectURL(url)
            })
        }
    },
    created() { },
    mounted() {
        this.load()
    }
};
</script>
<style lang="scss" scoped></style>