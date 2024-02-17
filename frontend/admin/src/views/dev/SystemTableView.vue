<template>
<div>
    <TableView ref="tableRef" @add="handleAdd" @edit="handleEdit">
      <template #addForm>
        <div>
          <Form ref="formRef" :title="meta.name" :defaultForm="meta.addForm.default" :fields="meta.addForm.fields" :progressFormData="handleProgressFormData" @submit="handleAddSubmit">
            
              <!-- columns  -->
              <template #columns="{form,field}">
                <div class="overflow-x-auto w-full">
                  
                  <!-- table -->
                  <!-- fields: title type key dataIndex width align fixed render scopedSlots -->
                  <ElTable :data="form[field.name]">
                    <ElTableColumn label="title" :prop="field.title">
                      <template #default="{row}">
                        <ElInput v-model="row.title" placeholder="请输入" />
                      </template>
                    </ElTableColumn>
                    <ElTableColumn label="type" :prop="field.type">
                      <template #default="{row}">
                        <ElInput v-model="row.type" placeholder="请输入" />
                      </template>
                    </ElTableColumn>
                    <ElTableColumn label="key" :prop="field.key">
                      <template #default="{row}">
                        <ElInput v-model="row.key" placeholder="请输入" />
                      </template>
                    </ElTableColumn>
                    <ElTableColumn label="dataIndex" :prop="field.dataIndex">
                      <template #default="{row}">
                        <ElInput v-model="row.dataIndex" placeholder="请输入" />
                      </template>
                    </ElTableColumn>
                    <ElTableColumn label="width" :prop="field.width" width="auto">
                      <template #default="{row}">
                        <ElInput v-model="row.width" placeholder="请输入" />
                      </template>
                    </ElTableColumn>
                    <!-- 操作 -->
                    <ElTableColumn label="操作" width="auto">
                      <template #default="{row}">
                        <ElButton type="danger" link @click="handleDeleteColumn(form,field.name,row)">删除</ElButton>
                      </template>
                    </ElTableColumn>
                  </ElTable>

                  <!-- btn add  -->
                  <div class="mt-2">
                    <ElButton type="primary" link  @click="handleAddColumn(form,field.name)">添加表格列</ElButton>
                  </div>
                </div>
              </template>

          </Form>
        </div>
      </template>
    </TableView>
</div>
</template>
<script>
import { ElTable, ElTableColumn,ElInput } from 'element-plus';
import TableView from '../TableView.vue';
import Form from '../components/Form.vue';
export default {
  components: {
    TableView, Form,
    ElTable,
    ElTableColumn
},
  props: {},
  data() {
    return {
      meta:this.$route.meta,

    };
  },
  watch: {},
  computed: {},
  methods: {
    handleAddSubmit(data) {
      this.$refs.tableRef?.handleAddSubmit(data);
    },
    handleAdd() {
      this.$refs.formRef?.add();
    },
    handleEdit(row) {
      this.$refs.formRef?.edit(row);
    },
    handleAddColumn(form,key) {
      if(!form[key]){
        form[key] = [];
      }
      form[key].push({
        title:'',
        type:'',
        key:'',
        dataIndex:'',
        width:120,
      });
    },
    handleProgressFormData(data){
      let res = {};
      for(let key in data){
        if(key == 'columns'){
          try{
            console.log(data[key]);
            res[key] = JSON.parse(data[key]);
          }catch(e){
            console.error(e);
          }
          continue;
        }

        res[key] = data[key];

      }
      return res;
    },
    handleDeleteColumn(form,key,row){
      form[key] = form[key].filter(el=>el!=row);
    }
  },
  created() {},
  mounted() {

  }
};
</script>
<style lang="scss" scoped>
</style>