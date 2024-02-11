<template>
<div>
    <TableView ref="tableRef" @add="handleAdd" @edit="handleEdit">
      <template #addForm>
        <div>
          <Form ref="formRef" :title="meta.name" :defaultForm="meta.addForm.default" :fields="meta.addForm.fields" @submit="handleAddSubmit">
            
              <!-- columns  -->
              <template #columns="{form,field}">
                <div>
                  columns
                  <ElInput v-model="form[field.name]" placeholder="请输入内容"></ElInput>
                </div>
              </template>

          </Form>
        </div>
      </template>
    </TableView>
</div>
</template>
<script>
import TableView from '../TableView.vue';
import Form from '../components/Form.vue';
export default {
  components: {
    TableView,Form
  },
  props: {},
  data() {
    return {
      meta:this.$route.meta
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
    }
  },
  created() {},
  mounted() {}
};
</script>
<style lang="scss" scoped>
</style>