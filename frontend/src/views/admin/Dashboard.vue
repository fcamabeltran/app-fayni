<template>
  <div>
    <h2 class="page-title">Dashboard Administrador</h2>

    <!-- Filtros fecha -->
    <el-card style="margin-bottom:1.5rem">
      <el-row :gutter="16" align="middle">
        <el-col :span="8">
          <el-date-picker v-model="fechaRango" type="daterange" range-separator="→"
            start-placeholder="Desde" end-placeholder="Hasta" format="DD/MM/YYYY"
            value-format="YYYY-MM-DD" style="width:100%" @change="cargar" />
        </el-col>
        <el-col :span="4">
          <el-button @click="limpiarFiltro">Limpiar filtro</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- KPIs -->
    <el-row :gutter="16" style="margin-bottom:1.5rem">
      <el-col :xs="12" :sm="6" v-for="kpi in kpis" :key="kpi.label">
        <div class="stat-card" style="margin-bottom:1rem">
          <div class="icon" :style="{ background: kpi.bg }">{{ kpi.icon }}</div>
          <div>
            <div class="value" :class="kpi.class">S/ {{ fmt(kpi.value) }}</div>
            <div class="label">{{ kpi.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- Gráficos fila 1 -->
    <el-row :gutter="16" style="margin-bottom:1.5rem">
      <el-col :sm="14">
        <div class="chart-card">
          <h3>Evolución Mensual Ingresos vs Egresos</h3>
          <Bar v-if="evolucionData" :data="evolucionData" :options="barOpts" style="max-height:280px" />
        </div>
      </el-col>
      <el-col :sm="10">
        <div class="chart-card">
          <h3>Egresos por Grupo (Top categorías)</h3>
          <Doughnut v-if="grupoData" :data="grupoData" :options="doughnutOpts" style="max-height:280px" />
        </div>
      </el-col>
    </el-row>

    <!-- Gráficos fila 2 -->
    <el-row :gutter="16" style="margin-bottom:1.5rem">
      <el-col :sm="12">
        <div class="chart-card">
          <h3>💡 Servicios de Casa (Luz y Agua)</h3>
          <Line v-if="serviciosData" :data="serviciosData" :options="lineOpts" style="max-height:220px" />
        </div>
      </el-col>
      <el-col :sm="12">
        <div class="chart-card">
          <h3>🏆 Top 5 Categorías de Egreso</h3>
          <el-table :data="topEgresos" size="small">
            <el-table-column prop="grupo" label="Categoría" />
            <el-table-column label="Total" align="right">
              <template #default="{ row }">
                <span class="egreso">S/ {{ fmt(row.total) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>

    <!-- Tabla todos los grupos -->
    <div class="chart-card">
      <h3>Resumen por Grupo</h3>
      <el-table :data="porGrupo" stripe style="margin-top:1rem">
        <el-table-column prop="icono" label="" width="50" />
        <el-table-column prop="grupo" label="Grupo" />
        <el-table-column label="Ingresos" align="right">
          <template #default="{ row }">
            <span class="ingreso">S/ {{ fmt(row.ingreso) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Egresos" align="right">
          <template #default="{ row }">
            <span class="egreso">S/ {{ fmt(row.egreso) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Balance" align="right">
          <template #default="{ row }">
            <span :class="row.ingreso - row.egreso >= 0 ? 'ingreso' : 'egreso'">
              S/ {{ fmt(row.ingreso - row.egreso) }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar, Doughnut, Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement,
  LineElement, PointElement, ArcElement, Tooltip, Legend
} from 'chart.js'
import api from '@/services/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Tooltip, Legend)

const fechaRango = ref(null)
const resumen = ref({})
const porGrupo = ref([])
const evolucion = ref([])
const servicios = ref([])
const topEgresos = ref([])

function fmt(v) { return Number(v || 0).toFixed(2) }

const kpis = computed(() => [
  { label: 'Total Ingresos',  value: resumen.value.total_ingreso,  icon: '📈', bg: '#dcfce7', class: 'ingreso' },
  { label: 'Total Egresos',   value: resumen.value.total_egreso,   icon: '📉', bg: '#fee2e2', class: 'egreso' },
  { label: 'Donaciones',      value: resumen.value.total_donacion, icon: '🎁', bg: '#ede9fe', class: 'donacion' },
  { label: 'Saldo Disponible',value: resumen.value.saldo_actual,   icon: '💰', bg: '#fef9c3', class: 'saldo' },
])

const evolucionData = computed(() => {
  if (!evolucion.value.length) return null
  return {
    labels: evolucion.value.map(r => r.periodo),
    datasets: [
      { label: 'Ingresos', data: evolucion.value.map(r => r.ingreso), backgroundColor: 'rgba(34,197,94,0.7)', borderColor: '#22c55e', borderWidth: 2 },
      { label: 'Egresos',  data: evolucion.value.map(r => r.egreso),  backgroundColor: 'rgba(239,68,68,0.7)',  borderColor: '#ef4444', borderWidth: 2 },
    ],
  }
})

const grupoData = computed(() => {
  const data = porGrupo.value.filter(g => g.egreso > 0).slice(0, 8)
  if (!data.length) return null
  return {
    labels: data.map(g => `${g.icono || ''} ${g.grupo}`),
    datasets: [{ data: data.map(g => g.egreso), backgroundColor: data.map(g => g.color || '#6366f1') }],
  }
})

const serviciosData = computed(() => {
  if (!servicios.value.length) return null
  return {
    labels: servicios.value.map(r => r.periodo),
    datasets: [{ label: 'Servicios Casa', data: servicios.value.map(r => r.total), fill: true, backgroundColor: 'rgba(245,158,11,0.15)', borderColor: '#f59e0b', tension: 0.4 }],
  }
})

const barOpts = { responsive: true, plugins: { legend: { position: 'bottom' } } }
const doughnutOpts = { responsive: true, plugins: { legend: { position: 'bottom' } } }
const lineOpts = { responsive: true, plugins: { legend: { display: false } } }

async function cargar() {
  const params = {}
  if (fechaRango.value) {
    params.fecha_desde = fechaRango.value[0]
    params.fecha_hasta = fechaRango.value[1]
  }
  const [r1, r2, r3, r4, r5] = await Promise.all([
    api.get('/dashboard/resumen', { params }),
    api.get('/dashboard/por-grupo', { params }),
    api.get('/dashboard/evolucion-mensual'),
    api.get('/dashboard/servicios-casa'),
    api.get('/dashboard/top-egresos', { params }),
  ])
  resumen.value   = r1.data
  porGrupo.value  = r2.data
  evolucion.value = r3.data
  servicios.value = r4.data
  topEgresos.value = r5.data
}

function limpiarFiltro() { fechaRango.value = null; cargar() }
onMounted(cargar)
</script>
