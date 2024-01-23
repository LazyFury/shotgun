<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import NavMenu from './components/layout/NavMenu.vue'
import { ElAvatar, ElBreadcrumb, ElButton, ElTabs } from 'element-plus';
</script>

<template>
  <div>
    <el-container class="min-h-screen bg-gary-100">
        <el-header class=" p-2 bg-primary text-white fixed w-full" style="left: 0;top:0;z-index: 99;height: 60px;">
            <ElRow :align="'middle'" class="py-3 h-full">
                <div class="flex-1">
                    <UIButton>
                        <span class="text-2xl font-bold">Element Vite Admin</span>
                    </UIButton>
                </div>
                <div class="flex flex-row items-center justify-center gap-4">
                    <UIButton class="flex-row-btn">
                        <Icon icon="ant-design:message-outlined"></Icon>
                        <span>Message</span>
                    </UIButton>
                    <UIButton class="flex-row-btn">
                        <Icon icon="ant-design:setting-outlined"></Icon>
                        <span>Setting</span>
                    </UIButton>
                    <UIButton class="flex-row-btn">
                        <Icon icon="ant-design:login-outlined"></Icon>
                        <span>Admin user.</span>
                    </UIButton>
                    <UIButton>
                        <ElAvatar />
                    </UIButton>
                </div>
            </ElRow>
        </el-header>
        <div style="height: 60px;" class="bg-gray-100"></div>
        <ElRow class="flex-1 bg-gray-100">
            <div class="w-200px bg-white fixed h-screen overflow-y-auto hidden-scroll-bar">
                <el-aside width="w-full bg-dark-100">
                    <NavMenu />
                </el-aside>
                <div class="h-100px"></div>
            </div>
            <div class="w-200px"></div>
            <div class="flex-1 ">
                <main class="p-4">
                    <RouterView></RouterView>
                </main>
            </div>
        </ElRow>
        <!-- <el-footer class="bg-dark-600">footer</el-footer> -->
    </el-container>
  </div>
</template>

<style scoped>

</style>
