import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('@/views/Login.vue') },

  // Admin
  {
    path: '/admin',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard',    component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'movimientos',  component: () => import('@/views/admin/Movimientos.vue') },
      { path: 'usuarios',     component: () => import('@/views/admin/Usuarios.vue') },
      { path: 'catalogos',    component: () => import('@/views/admin/Catalogos.vue') },
    ],
  },

  // Familia
  {
    path: '/familia',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true, role: 'familia' },
    children: [
      { path: '', redirect: '/familia/dashboard' },
      { path: 'dashboard',   component: () => import('@/views/familia/Dashboard.vue') },
      { path: 'movimientos', component: () => import('@/views/familia/Movimientos.vue') },
      { path: 'nuevo',       component: () => import('@/views/familia/NuevoMovimiento.vue') },
    ],
  },

  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) return next('/login')
    if (to.meta.role === 'admin' && !auth.isAdmin) return next('/familia/dashboard')
    if (to.meta.role === 'familia' && auth.isAdmin) return next('/admin/dashboard')
  }
  if (to.path === '/login' && auth.isAuthenticated) {
    return next(auth.isAdmin ? '/admin/dashboard' : '/familia/dashboard')
  }
  next()
})

export default router
