import HomeView from '@/views/HomeView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Profile.vue'),
    },
    {
      path: '/lesson/:id',
      component: () => import('@/views/LessonView.vue'),
    },
    {
      path: '/lesson/:id/learn',
      component: () => import('@/views/LearningView.vue'),
      redirect: (to) => `${to.params.id}/learn/notice`,
      children: [
        {
          path: 'notice',
          component: () => import('@/views/Learning/Notice.vue'),
        },
        {
          path: 'courseware',
          component: () => import('@/views/Learning/Couseware.vue')
        },
        {
          path: 'discussion',
          component: () => import('@/views/Learning/Discussion.vue')
        }
      ]
    }
  ],
})

export default router
