import { createWebHistory, createRouter } from 'vue-router'

import Login from '@/components/Login.vue'
import AdminDash from '@/components/AdminDash.vue'
import AdminComp from '@/components/AdminComp.vue'
import AdminStud from '@/components/AdminStud.vue'
import AdminSearch from '@/components/AdminSearch.vue'
import AdminSum from '@/components/AdminSum.vue'
import AdminPro from '@/components/AdminPro.vue'
import ComDash from '@/components/ComDash.vue'
import ComPro from '@/components/ComPro.vue'
import ComApp from '@/components/ComApp.vue'
import StudDash from '@/components/StudDash.vue'
import StudPro from '@/components/StudPro.vue'
import StudApp from '@/components/StudApp.vue'

const routes = [
        {  
            path: '/',
            name: 'login',
            component: Login
        },
        {  
            path: '/admin/dashboard',
            name: 'admindash',
            component: AdminDash
        },
        {  
            path: '/admin/companies',
            name: 'admincomp',
            component: AdminComp
        },
        {  
            path: '/admin/students',
            name: 'adminstud',
            component: AdminStud
        },
        {  
            path: '/admin/search',
            name: 'adminsearch',
            component: AdminSearch
        },
        {  
            path: '/admin/summary',
            name: 'adminsummary',
            component: AdminSum
        },
        {  
            path: '/admin/profile',
            name: 'adminprofile',
            component: AdminPro
        },
        {  
            path: '/company/dashboard',
            name: 'comdash',
            component: ComDash
        },
        {  
            path: '/company/profile',
            name: 'comprofile',
            component: ComPro
        },
        {  
            path: '/company/applications',
            name: 'comapp',
            component: ComApp
        },
        {  
            path: '/student/dashboard',
            name: 'studdash',
            component: StudDash
        },
        {  
            path: '/student/profile',
            name: 'studprofile',
            component: StudPro
        },
        {  
            path: '/student/history',
            name: 'studhistory',
            component: StudApp
        },
        {
            path: '/logout',
            name: 'logout',
            beforeEnter: (to, from, next) => {
                localStorage.removeItem('token')
                localStorage.removeItem('role')
                next({ name: 'login' })
                alert('Logged Out Successfully')
            }
        }
]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})