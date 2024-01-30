import { createRouter, createWebHashHistory } from 'vue-router'
import {ElMessage} from "element-plus";
const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:"",
      redirect:"/overview"
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },

    // 404
    {
        path: '/not-found',
        name: 'not-found',
        component: () => import('../views/NotFoundView.vue')
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: {name: 'not-found'}
    }
  ]
})

router.onError((err) => {
    ElMessage.error(err.message)
    router.push({name: 'not-found'})
})

export default router
