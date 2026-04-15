<template>
  <div>
    <h2 class="page-title">Gestión de Usuarios</h2>
    <el-button type="primary" style="margin-bottom:1rem" @click="showForm = true">+ Nuevo Usuario</el-button>

    <el-table :data="usuarios" stripe border>
      <el-table-column prop="nombre" label="Nombre" />
      <el-table-column prop="email" label="Email" />
      <el-table-column label="Rol" width="120">
        <template #default="{ row }">
          <el-tag :type="row.rol === 'admin' ? 'danger' : 'success'">
            {{ row.rol === 'admin' ? '👑 Admin' : '👨‍👩‍👧 Familia' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Estado" width="100">
        <template #default="{ row }">
          <el-tag :type="row.activo ? 'success' : 'info'">{{ row.activo ? 'Activo' : 'Inactivo' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="" width="100" align="center">
        <template #default="{ row }">
          <el-popconfirm title="¿Desactivar usuario?" @confirm="desactivar(row.id)">
            <template #reference>
              <el-button size="small" type="danger" :disabled="!row.activo">Desactivar</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showForm" title="Nuevo Usuario" width="420px">
      <el-form :model="form" label-position="top">
        <el-form-item label="Nombre"><el-input v-model="form.nombre" /></el-form-item>
        <el-form-item label="Email"><el-input v-model="form.email" type="email" /></el-form-item>
        <el-form-item label="Contraseña"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="Rol">
          <el-select v-model="form.rol" style="width:100%">
            <el-option label="Familia" value="familia" />
            <el-option label="Administrador" value="admin" />
          </el-select>
        </el-form-item>
        <el-button type="primary" style="width:100%" @click="crearUsuario">Crear Usuario</el-button>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/services/api'

const usuarios = ref([])
const showForm = ref(false)
const form = ref({ nombre: '', email: '', password: '', rol: 'familia' })

async function cargar() {
  const { data } = await api.get('/auth/usuarios')
  usuarios.value = data
}

async function crearUsuario() {
  await api.post('/auth/usuarios', form.value)
  ElMessage.success('Usuario creado')
  showForm.value = false
  form.value = { nombre: '', email: '', password: '', rol: 'familia' }
  cargar()
}

async function desactivar(id) {
  await api.delete(`/auth/usuarios/${id}`)
  ElMessage.success('Usuario desactivado')
  cargar()
}

onMounted(cargar)
</script>
