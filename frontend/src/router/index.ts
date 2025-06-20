import { accountState } from '@/global/account'
import HomeView from '@/views/HomeView.vue'
import Notice from '@/views/Learning/Notice.vue'
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
      meta: { requiresAuth: true }
    },
    {
      path: '/lesson/:courseid',
      component: () => import('@/views/LessonView.vue'),
    },
    {
      path: '/lesson/:courseid/:method',
      component: () => import('@/views/LearningView.vue'),
      meta: { requiresAuth: true },
      redirect: (to) => `${to.params.courseid}/${to.params.method}/notice`,
      children: [
        {
          path: 'notice',
          component: Notice
        },
        {
          path: 'courseware',
          component: () => import('@/views/Learning/Couseware.vue')
        },
        {
          path: 'discussion',
          component: () => import('@/views/Learning/Discussion.vue')
        },
        {
          path: 'exam',
          component: () => import('@/views/Learning/Exam.vue')
        },
        {
          path: 'exam/:examid',
          name: 'examcontent',
          component: () => import('@/views/Learning/ExamContent.vue'),
        },
        {
          path: 'assignments',
          component: () => import('@/views/Learning/Assignments.vue')
        }
      ]
    },
    {
      path: '/offer',
      component: () => import('@/views/OfferCourse.vue'),
      meta: { requiresAuth: true, teacher: true }
    }
  ],
})

router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !accountState.isLoggedIn) {
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }
  if(to.meta.teacher && accountState.role != 'teacher') {
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }
  if(to.params.method == 'manage' && accountState.role != 'teacher'){
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }
})

export default router
