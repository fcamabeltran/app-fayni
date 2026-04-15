<template>
  <el-container style="min-height:100vh">
    <!-- Sidebar -->
    <el-aside :width="collapsed ? '64px' : '220px'" class="sidebar">
      <div class="sidebar-header" @click="collapsed = !collapsed">
        <span class="logo-icon">💰</span>
        <span v-if="!collapsed" class="logo-text">Fayni</span>
      </div>

      <el-menu
        :default-active="$route.path"
        router
        :collapse="collapsed"
        background-color="#1a1a2e"
        text-color="#cbd5e1"
        active-text-color="#6366f1"
      >
        <template v-for="item in menuItems" :key="item.path">
          <el-menu-item :index="item.path">
            <el-icon><component :is="item.icon" /></el-icon>
            <template #title>{{ item.label }}</template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <!-- Main -->
    <el-container>
      <el-header class="topbar">
        <div class="topbar-left">
          <span class="page-name">{{ currentPageName }}</span>
        </div>
        <div class="topbar-right">
          <el-tag :type="auth.isAdmin ? 'danger' : 'success'" size="small">
            {{ auth.isAdmin ? '👑 Admin' : '👨‍👩‍👧 Familia' }}
          </el-tag>
          <span class="username">{{ auth.user?.nombre }}</span>
          <el-button type="danger" size="small" plain @click="logout">Salir</el-button>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const collapsed = ref(false)

const adminMenu = [
  { path: '/admin/dashboard',   label: 'Dashboard',    icon: 'Odometer' },
  { path: '/admin/movimientos', label: 'Movimientos',  icon: 'List' },
  { path: '/admin/usuarios',    label: 'Usuarios',     icon: 'User' },
  { path: '/admin/catalogos',   label: 'Catálogos',    icon: 'Setting' },
]

const familiaMenu = [
  { path: '/familia/dashboard',   label: 'Dashboard',     icon: 'Odometer' },
  { path: '/familia/movimientos', label: 'Movimientos',   icon: 'List' },
  { path: '/familia/nuevo',       label: 'Nuevo Gasto',   icon: 'Plus' },
]

const menuItems = computed(() => auth.isAdmin ? adminMenu : familiaMenu)
const currentPageName = computed(() => {
  return menuItems.value.find(i => i.path === route.path)?.label || 'Fayni'
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  background: #1a1a2e;
  transition: width 0.3s;
  overflow: hidden;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo-icon { font-size: 1.6rem; }
.logo-text { color: white; font-weight: 800; font-size: 1.2rem; }

.topbar {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 1.5rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username { font-weight: 600; font-size: 0.9rem; color: #374151; }
.page-name { font-weight: 700; font-size: 1.1rem; color: #1a1a2e; }
</style>
