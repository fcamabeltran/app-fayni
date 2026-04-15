<template>
  <el-form :model="form" label-position="top" @submit.prevent="guardar">
    <el-row :gutter="16">
      <el-col :span="12">
        <el-form-item label="Fecha" required>
          <el-date-picker v-model="form.fecha" type="date" format="DD/MM/YYYY" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Tipo" required>
          <el-select v-model="form.tipo_id" style="width:100%" @change="onTipoChange">
            <el-option v-for="t in tipos" :key="t.id" :label="t.nombre" :value="t.id" />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item label="Descripción" required>
      <el-input v-model="form.descripcion" placeholder="Ej: Pago de luz, Compra víveres..." />
    </el-form-item>

    <el-form-item label="Grupo / Categoría" required>
      <el-select v-model="form.grupo_id" style="width:100%" filterable>
        <el-option v-for="g in grupos" :key="g.id" :label="`${g.icono||''} ${g.nombre}`" :value="g.id" />
      </el-select>
    </el-form-item>

    <el-row :gutter="16">
      <el-col :span="12">
        <el-form-item label="Monto Ingreso (S/)">
          <el-input-number v-model="form.monto_ingreso" :min="0" :precision="2" :step="1" style="width:100%" :disabled="tipoNombre === 'EGRESO'" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="Monto Egreso (S/)">
          <el-input-number v-model="form.monto_egreso" :min="0" :precision="2" :step="1" style="width:100%" :disabled="tipoNombre === 'INGRESO'" />
        </el-form-item>
      </el-col>
    </el-row>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" style="margin-bottom:1rem" />

    <el-row :gutter="12">
      <el-col :span="12">
        <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">
          {{ inicial ? 'Actualizar' : 'Guardar' }}
        </el-button>
      </el-col>
      <el-col :span="12">
        <el-button style="width:100%" @click="$emit('cancelar')">Cancelar</el-button>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/services/api'

const props = defineProps({
  grupos: { type: Array, default: () => [] },
  tipos:  { type: Array, default: () => [] },
  inicial: { type: Object, default: null },
})

const emit = defineEmits(['guardado', 'cancelar'])

const loading = ref(false)
const error = ref('')

const emptyForm = () => ({
  fecha: new Date().toISOString().split('T')[0],
  descripcion: '',
  grupo_id: null,
  tipo_id: null,
  monto_ingreso: 0,
  monto_egreso: 0,
})

const form = ref(emptyForm())

watch(() => props.inicial, (val) => {
  if (val) form.value = {
    fecha: val.fecha,
    descripcion: val.descripcion,
    grupo_id: val.grupo.id,
    tipo_id: val.tipo.id,
    monto_ingreso: val.monto_ingreso,
    monto_egreso: val.monto_egreso,
  }
  else form.value = emptyForm()
}, { immediate: true })

const tipoNombre = computed(() => {
  return props.tipos.find(t => t.id === form.value.tipo_id)?.nombre || ''
})

function onTipoChange() {
  const nombre = tipoNombre.value
  if (nombre === 'INGRESO') form.value.monto_egreso = 0
  if (nombre === 'EGRESO') form.value.monto_ingreso = 0
}

async function guardar() {
  error.value = ''
  if (!form.value.fecha || !form.value.descripcion || !form.value.grupo_id || !form.value.tipo_id) {
    error.value = 'Completa todos los campos obligatorios'
    return
  }
  if (form.value.monto_ingreso <= 0 && form.value.monto_egreso <= 0) {
    error.value = 'Ingresa un monto mayor a 0'
    return
  }
  loading.value = true
  try {
    if (props.inicial) await api.put(`/movimientos/${props.inicial.id}`, form.value)
    else await api.post('/movimientos/', form.value)
    ElMessage.success(props.inicial ? 'Actualizado' : 'Guardado')
    emit('guardado')
    form.value = emptyForm()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    loading.value = false
  }
}
</script>
