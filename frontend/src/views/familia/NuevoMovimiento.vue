<template>
  <div style="max-width:600px;margin:0 auto">
    <h2 class="page-title">Registrar Movimiento</h2>
    <div class="chart-card">
      <MovimientoForm :grupos="grupos" :tipos="tipos" @guardado="onGuardado" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/services/api'
import MovimientoForm from '@/components/movimientos/MovimientoForm.vue'

const router = useRouter()
const grupos = ref([])
const tipos = ref([])

function onGuardado() {
  ElMessage.success('Movimiento registrado')
  router.push('/familia/movimientos')
}

onMounted(async () => {
  const [g, t] = await Promise.all([api.get('/catalogos/grupos'), api.get('/catalogos/tipos')])
  grupos.value = g.data
  tipos.value = t.data
})
</script>
