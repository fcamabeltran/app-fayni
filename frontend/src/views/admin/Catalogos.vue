<template>
  <div>
    <h2 class="page-title">Catálogos</h2>

    <el-tabs>
      <el-tab-pane label="Grupos / Categorías">
        <el-button type="primary" style="margin-bottom:1rem" @click="showGrupoForm = true; grupoEdit = null">+ Nuevo Grupo</el-button>
        <el-table :data="grupos" stripe border>
          <el-table-column label="Icono" width="60"><template #default="{ row }">{{ row.icono }}</template></el-table-column>
          <el-table-column prop="nombre" label="Nombre" />
          <el-table-column prop="descripcion" label="Descripción" />
          <el-table-column label="Color" width="80">
            <template #default="{ row }">
              <span :style="{ background: row.color, padding: '2px 10px', borderRadius: '4px', color: 'white' }">{{ row.color }}</span>
            </template>
          </el-table-column>
          <el-table-column label="" width="120" align="center">
            <template #default="{ row }">
              <el-button size="small" @click="grupoEdit = row; showGrupoForm = true">✏️</el-button>
              <el-popconfirm title="¿Eliminar?" @confirm="eliminarGrupo(row.id)">
                <template #reference><el-button size="small" type="danger">🗑️</el-button></template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="Tipos">
        <el-table :data="tipos" stripe border style="max-width:400px">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="nombre" label="Nombre" />
        </el-table>
        <p style="margin-top:0.5rem;color:#6b7280;font-size:0.85rem">Los tipos (INGRESO, EGRESO, DONACIÓN) son fijos del sistema.</p>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showGrupoForm" :title="grupoEdit ? 'Editar Grupo' : 'Nuevo Grupo'" width="420px">
      <el-form :model="grupoForm" label-position="top">
        <el-form-item label="Nombre"><el-input v-model="grupoForm.nombre" /></el-form-item>
        <el-form-item label="Descripción"><el-input v-model="grupoForm.descripcion" /></el-form-item>
        <el-form-item label="Icono (emoji)"><el-input v-model="grupoForm.icono" placeholder="ej: 🛒" /></el-form-item>
        <el-form-item label="Color (hex)"><el-input v-model="grupoForm.color" placeholder="ej: #22c55e" /></el-form-item>
        <el-button type="primary" style="width:100%" @click="guardarGrupo">Guardar</el-button>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/services/api'

const grupos = ref([])
const tipos = ref([])
const showGrupoForm = ref(false)
const grupoEdit = ref(null)
const grupoForm = ref({ nombre: '', descripcion: '', icono: '', color: '' })

watch(grupoEdit, (val) => {
  if (val) grupoForm.value = { nombre: val.nombre, descripcion: val.descripcion || '', icono: val.icono || '', color: val.color || '' }
  else grupoForm.value = { nombre: '', descripcion: '', icono: '', color: '' }
})

async function cargar() {
  const [g, t] = await Promise.all([api.get('/catalogos/grupos'), api.get('/catalogos/tipos')])
  grupos.value = g.data
  tipos.value = t.data
}

async function guardarGrupo() {
  if (grupoEdit.value) await api.put(`/catalogos/grupos/${grupoEdit.value.id}`, grupoForm.value)
  else await api.post('/catalogos/grupos', grupoForm.value)
  ElMessage.success('Guardado')
  showGrupoForm.value = false
  cargar()
}

async function eliminarGrupo(id) {
  await api.delete(`/catalogos/grupos/${id}`)
  ElMessage.success('Eliminado')
  cargar()
}

onMounted(cargar)
</script>
