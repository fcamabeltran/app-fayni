<template>
  <div class="login-bg">
    <div class="login-card">
      <div class="login-logo">💰</div>
      <h1>Fayni</h1>
      <p class="subtitle">Gestión de Gastos Familiar</p>

      <el-form :model="form" @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="Correo electrónico">
          <el-input v-model="form.email" type="email" placeholder="tu@correo.com" size="large" />
        </el-form-item>
        <el-form-item label="Contraseña">
          <el-input v-model="form.password" type="password" placeholder="••••••••" size="large" show-password />
        </el-form-item>
        <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" style="margin-bottom:1rem" />
        <el-button type="primary" native-type="submit" size="large" :loading="loading" style="width:100%">
          Ingresar
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.value.email, form.value.password)
    router.push(auth.isAdmin ? '/admin/dashboard' : '/familia/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  text-align: center;
}

.login-logo {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
}

h1 {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

:deep(.el-form-item__label) { font-weight: 600; }
</style>
