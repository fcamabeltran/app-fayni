<template>
  <div>
    <div class="dash-header">
      <h2 class="page-title" style="margin:0">Mi Dashboard Familiar</h2>
      <span class="fecha-hoy">📅 {{ fechaHoy }}</span>
    </div>

    <!-- KPIs generales -->
    <el-row :gutter="14" style="margin-bottom:1.25rem">
      <el-col :xs="12" :sm="6" v-for="kpi in kpis" :key="kpi.label">
        <div class="kpi-card" :style="{ borderLeftColor: kpi.accent }">
          <div class="kpi-icon" :style="{ background: kpi.bg }">{{ kpi.icon }}</div>
          <div class="kpi-body">
            <div class="kpi-value" :style="{ color: kpi.accent }">S/ {{ fmt(kpi.value) }}</div>
            <div class="kpi-label">{{ kpi.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- Mes actual -->
    <div class="mes-actual-bar" style="margin-bottom:1.25rem">
      <span class="mes-titulo">📆 {{ mesActualNombre }}</span>
      <div class="mes-stats">
        <span class="ms ingreso-ms">
          <span class="ms-dot" style="background:#22c55e"></span>
          Ingresos <strong>S/ {{ fmt(mesActual.ingreso) }}</strong>
        </span>
        <span class="ms egreso-ms">
          <span class="ms-dot" style="background:#ef4444"></span>
          Egresos <strong>S/ {{ fmt(mesActual.egreso) }}</strong>
        </span>
        <span class="ms" :style="{ color: mesActual.ingreso - mesActual.egreso >= 0 ? '#22c55e' : '#ef4444' }">
          Net mes <strong>S/ {{ fmtSigned(mesActual.ingreso - mesActual.egreso) }}</strong>
        </span>
      </div>
    </div>

    <!-- Gráficos fila 1 -->
    <el-row :gutter="14" style="margin-bottom:1.25rem">
      <el-col :sm="15">
        <div class="chart-card">
          <div class="chart-title">
            <span>Ingresos vs Egresos por mes</span>
            <el-select v-model="anioFiltro" size="small" style="width:90px" @change="cargarEvolucion">
              <el-option v-for="a in anios" :key="a" :label="a" :value="a" />
            </el-select>
          </div>
          <Bar v-if="evolucionData" :data="evolucionData" :options="barOpts" style="max-height:260px" />
          <div v-else class="empty-chart">Sin datos</div>
        </div>
      </el-col>
      <el-col :sm="9">
        <div class="chart-card">
          <div class="chart-title"><span>¿En qué gasté más?</span></div>
          <Doughnut v-if="grupoData" :data="grupoData" :options="doughnutOpts" style="max-height:260px" />
          <div v-else class="empty-chart">Sin datos</div>
        </div>
      </el-col>
    </el-row>

    <!-- Últimos movimientos -->
    <div class="chart-card">
      <div class="chart-title">
        <span>Últimos 15 movimientos</span>
        <router-link to="/familia/movimientos">
          <el-button size="small" plain>Ver todos →</el-button>
        </router-link>
      </div>

      <div class="mini-table-wrap">
        <table class="mini-table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Descripción</th>
              <th>Grupo</th>
              <th class="r">Monto</th>
              <th class="r">Saldo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in ultimos" :key="row.id" :class="row.monto_ingreso > 0 ? 'tr-ing' : 'tr-egr'">
              <td class="td-fecha">{{ row.fecha }}</td>
              <td class="td-desc" :title="row.descripcion">{{ row.descripcion }}</td>
              <td>
                <span class="grupo-pill" :style="{ background: row.grupo.color+'22', borderColor: row.grupo.color, color: row.grupo.color }">
                  {{ row.grupo.icono }} {{ row.grupo.nombre }}
                </span>
              </td>
              <td class="r">
                <span v-if="row.monto_ingreso > 0" class="ingreso fw">+S/ {{ row.monto_ingreso.toFixed(2) }}</span>
                <span v-else class="egreso fw">-S/ {{ row.monto_egreso.toFixed(2) }}</span>
              </td>
              <td class="r saldo fw">S/ {{ (row.saldo || 0).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement,
  ArcElement, Tooltip, Legend
} from 'chart.js'
import api from '@/services/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend)

const resumen  = ref({})
const porGrupo = ref([])
const evolucion = ref([])
const ultimos  = ref([])
const anioFiltro = ref(new Date().getFullYear())
const anios = [2024, 2025, 2026]

function fmt(v)       { return Number(v || 0).toFixed(2) }
function fmtSigned(v) { return (v >= 0 ? '+' : '') + Number(v || 0).toFixed(2) }

const fechaHoy = computed(() => {
  return new Date().toLocaleDateString('es-PE', { weekday:'long', day:'numeric', month:'long', year:'numeric' })
})

const mesActualNombre = computed(() => {
  return new Date().toLocaleDateString('es-PE', { month:'long', year:'numeric' })
})

// Mes actual calculado desde la evolución
const mesActual = computed(() => {
  const ahora = new Date()
  const found = evolucion.value.find(r => r.anio === ahora.getFullYear() && r.mes === ahora.getMonth() + 1)
  return found || { ingreso: 0, egreso: 0 }
})

const kpis = computed(() => [
  { label: 'Total Ingresos',   value: resumen.value.total_ingreso,  icon: '📈', bg: '#dcfce7', accent: '#16a34a' },
  { label: 'Total Egresos',    value: resumen.value.total_egreso,   icon: '📉', bg: '#fee2e2', accent: '#dc2626' },
  { label: 'Donaciones',       value: resumen.value.total_donacion, icon: '🎁', bg: '#ede9fe', accent: '#7c3aed' },
  { label: 'Saldo Disponible', value: resumen.value.saldo_actual,   icon: '💰', bg: '#fef9c3', accent: '#b45309' },
])

const evolucionData = computed(() => {
  if (!evolucion.value.length) return null
  const meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
  const data = evolucion.value.filter(r => r.anio === anioFiltro.value)
  if (!data.length) return null
  return {
    labels: data.map(r => meses[r.mes - 1]),
    datasets: [
      {
        label: 'Ingresos',
        data: data.map(r => r.ingreso),
        backgroundColor: 'rgba(34,197,94,0.75)',
        borderColor: '#16a34a',
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Egresos',
        data: data.map(r => r.egreso),
        backgroundColor: 'rgba(239,68,68,0.75)',
        borderColor: '#dc2626',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  }
})

const grupoData = computed(() => {
  // Top 6 por egreso
  const top = [...porGrupo.value]
    .filter(g => g.egreso > 0)
    .sort((a, b) => b.egreso - a.egreso)
    .slice(0, 6)
  if (!top.length) return null
  return {
    labels: top.map(g => `${g.icono || ''} ${g.grupo}`),
    datasets: [{
      data: top.map(g => g.egreso),
      backgroundColor: top.map(g => g.color || '#6366f1'),
      borderWidth: 2,
      borderColor: '#fff',
    }],
  }
})

const barOpts = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } },
  scales: {
    y: { ticks: { callback: v => 'S/ ' + v } },
  },
}

const doughnutOpts = {
  responsive: true,
  cutout: '60%',
  plugins: {
    legend: { position: 'bottom', labels: { font: { size: 11 } } },
    tooltip: { callbacks: { label: ctx => ` S/ ${ctx.parsed.toFixed(2)}` } },
  },
}

async function cargarEvolucion() {
  const { data } = await api.get('/dashboard/evolucion-mensual')
  evolucion.value = data
}

onMounted(async () => {
  const [r1, r2, r3, r4] = await Promise.all([
    api.get('/dashboard/resumen'),
    api.get('/dashboard/por-grupo'),
    api.get('/dashboard/evolucion-mensual'),
    api.get('/movimientos/', { params: { limit: 15, desc: true } }),
  ])
  resumen.value   = r1.data
  porGrupo.value  = r2.data
  evolucion.value = r3.data
  // Últimos 15 por orden de inserción (los últimos IDs)
  ultimos.value = r4.data  // ya viene desc: true, limit: 15 desde la API
})
</script>

<style scoped>
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.fecha-hoy {
  font-size: 0.82rem;
  color: #64748b;
  text-transform: capitalize;
}

/* KPI cards */
.kpi-card {
  background: white;
  border-radius: 10px;
  border-left: 4px solid;
  padding: 1rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-bottom: 1rem;
}

.kpi-icon {
  font-size: 1.5rem;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-value {
  font-size: 1.35rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  line-height: 1.2;
}

.kpi-label {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 2px;
}

/* Mes actual bar */
.mes-actual-bar {
  background: white;
  border-radius: 10px;
  padding: 0.75rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  flex-wrap: wrap;
}

.mes-titulo {
  font-weight: 700;
  font-size: 0.9rem;
  color: #1a1a2e;
  text-transform: capitalize;
  white-space: nowrap;
}

.mes-stats { display: flex; gap: 2rem; flex-wrap: wrap; }

.ms {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #374151;
}

.ms-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Charts */
.chart-card {
  background: white;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-bottom: 1rem;
}

.chart-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: #374151;
}

.empty-chart {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.85rem;
}

/* Mini tabla */
.mini-table-wrap {
  overflow-x: auto;
  max-height: 380px;
  overflow-y: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.mini-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.83rem;
}

.mini-table thead tr {
  background: #1a1a2e;
  color: #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 1;
}

.mini-table th {
  padding: 9px 12px;
  font-weight: 600;
  font-size: 0.78rem;
  text-align: left;
  white-space: nowrap;
}

.mini-table td {
  padding: 8px 12px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.mini-table .tr-ing td { background: #f0fdf4; }
.mini-table .tr-egr td { background: #fff5f5; }
.mini-table tbody tr:hover td { filter: brightness(0.97); }

.td-fecha { white-space: nowrap; color: #6b7280; font-size: 0.8rem; }

.td-desc {
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.grupo-pill {
  display: inline-block;
  padding: 2px 7px;
  border-radius: 20px;
  border: 1px solid;
  font-size: 0.72rem;
  font-weight: 600;
  white-space: nowrap;
}

.r  { text-align: right; }
.fw { font-weight: 700; font-variant-numeric: tabular-nums; }

.ingreso { color: #16a34a; }
.egreso  { color: #dc2626; }
.saldo   { color: #0369a1; }
</style>
