<template>
<div>
    <ElForm :inline="true" :model="form" :rules="rules" class="mb-4 grid xl:grid-cols-2" :label-width="100">
        <ElFormItem v-for="field in fields" :key="field.name" :label="field.label + ':'" :prop="field.name">
            <ElInput v-if="field.type == 'textarea'" type="textarea" :placeholder="field.placeholder"></ElInput>
            <ElInput v-else :placeholder="field.placeholder"></ElInput>
        </ElFormItem>
    </ElForm>

    <div class="flex flex-row items-center justify-end">
        <ElButton type="primary" class="w-24">保存</ElButton>
    </div>
</div>
</template>
<script>
export default {
  components: {},
  props: {
    fields:{
        type:Array,
        default:()=>[]
    }
  },
  computed:{
    rules(){
        // check required in fields 
        let map = {}
        this.fields.forEach(el=>{
            if(el.required){
                map[el.name] = [
                    {required:true,message:el.placeholder}
                ]
            }
        })
        return map;
    }
  },
  data() {
    return {
        form:{

        }
    };
  },
  watch: {},
  methods: {},
  created() {},
  mounted() {}
};
</script>
<style lang="scss" scoped>
</style>