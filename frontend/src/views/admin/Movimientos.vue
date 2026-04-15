<template>
  <div>
    <div class="dt-header">
      <h2 class="page-title" style="margin:0">Movimientos</h2>
      <div style="display:flex;gap:8px;align-items:center">
        <el-button plain @click="exportarExcel" :loading="exportandoExcel">
          <el-icon><Download /></el-icon> Excel
        </el-button>
        <el-button plain type="danger" @click="exportarPdf" :loading="exportandoPdf">
          <el-icon><Document /></el-icon> PDF
        </el-button>
        <el-button type="primary" @click="showForm = true; editando = null">
          <el-icon><Plus /></el-icon> Nuevo movimiento
        </el-button>
      </div>
    </div>

    <!-- Filtros -->
    <el-card class="filter-card">
      <el-row :gutter="12" align="middle">
        <el-col :xs="24" :sm="8">
          <el-input v-model="buscar" placeholder="Buscar descripción..." clearable :prefix-icon="Search" @input="filtrarLocal" />
        </el-col>
        <el-col :xs="24" :sm="7">
          <el-date-picker v-model="filtros.rango" type="daterange" format="DD/MM/YYYY"
            value-format="YYYY-MM-DD" start-placeholder="Desde" end-placeholder="Hasta"
            style="width:100%" @change="cargar" />
        </el-col>
        <el-col :xs="12" :sm="4">
          <el-select v-model="filtros.grupo_id" clearable placeholder="Grupo" @change="cargar" style="width:100%">
            <el-option v-for="g in grupos" :key="g.id" :label="`${g.icono||''} ${g.nombre}`" :value="g.id" />
          </el-select>
        </el-col>
        <el-col :xs="12" :sm="3">
          <el-select v-model="filtros.tipo_id" clearable placeholder="Tipo" @change="cargar" style="width:100%">
            <el-option v-for="t in tipos" :key="t.id" :label="t.nombre" :value="t.id" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="2">
          <el-button plain @click="limpiar" style="width:100%">Limpiar</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- Info bar -->
    <div class="dt-info-bar">
      <span>{{ paginados.length }} de {{ filtrados.length }} registros</span>
      <div class="totales-bar">
        <span>Ingresos: <strong class="ingreso">S/ {{ fmt(totalIngreso) }}</strong></span>
        <span>Egresos: <strong class="egreso">S/ {{ fmt(totalEgreso) }}</strong></span>
        <span>Balance: <strong :class="balance >= 0 ? 'ingreso' : 'egreso'">S/ {{ fmt(balance) }}</strong></span>
      </div>
    </div>

    <!-- Tabla -->
    <div class="dt-wrapper">
      <el-table
        :data="paginados"
        stripe
        border
        highlight-current-row
        max-height="520"
        :header-cell-style="{ background: '#1a1a2e', color: '#e2e8f0', fontWeight: '600', fontSize: '0.8rem' }"
        :row-class-name="rowClass"
        style="width:100%"
      >
        <el-table-column type="index" label="#" width="52" align="center" fixed="left"
          :index="(i) => (currentPage - 1) * pageSize + i + 1" />

        <el-table-column prop="fecha" label="Fecha" width="105" fixed="left" sortable />

        <el-table-column label="Descripción" min-width="220">
          <template #default="{ row }">
            <span class="desc-cell" :title="row.descripcion">{{ row.descripcion }}</span>
          </template>
        </el-table-column>

        <el-table-column label="Grupo" width="170" sortable :sort-method="(a,b) => a.grupo.nombre.localeCompare(b.grupo.nombre)">
          <template #default="{ row }">
            <span class="grupo-badge" :style="{ background: row.grupo.color + '22', borderColor: row.grupo.color, color: row.grupo.color }">
              {{ row.grupo.icono }} {{ row.grupo.nombre }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="Tipo" width="115" align="center">
          <template #default="{ row }">
            <el-tag :type="tipoTag(row.tipo.nombre)" size="small" effect="dark">{{ row.tipo.nombre }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Ingreso" align="right" width="120" sortable :sort-method="(a,b) => a.monto_ingreso - b.monto_ingreso">
          <template #default="{ row }">
            <span v-if="row.monto_ingreso > 0" class="monto-cell ingreso">
              +S/ {{ row.monto_ingreso.toFixed(2) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="Egreso" align="right" width="120" sortable :sort-method="(a,b) => a.monto_egreso - b.monto_egreso">
          <template #default="{ row }">
            <span v-if="row.monto_egreso > 0" class="monto-cell egreso">
              -S/ {{ row.monto_egreso.toFixed(2) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="Saldo" align="right" width="120">
          <template #default="{ row }">
            <span class="monto-cell saldo">S/ {{ (row.saldo || 0).toFixed(2) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="Acciones" width="90" align="center" fixed="right">
          <template #default="{ row }">
            <el-tooltip content="Editar" placement="top">
              <el-button size="small" circle plain type="primary" :icon="EditPen" @click="editar(row)" />
            </el-tooltip>
            <el-popconfirm title="¿Eliminar este movimiento?" confirm-button-text="Sí" cancel-button-text="No" @confirm="eliminar(row.id)">
              <template #reference>
                <el-tooltip content="Eliminar" placement="top">
                  <el-button size="small" circle plain type="danger" :icon="Delete" />
                </el-tooltip>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Paginación -->
    <div class="dt-pagination">
      <div class="page-size-selector">
        <span class="ps-label">Filas:</span>
        <button
          v-for="opt in pageSizeOpts" :key="opt.value"
          class="ps-btn"
          :class="{ active: pageSize === opt.value }"
          @click="setPageSize(opt.value)"
        >{{ opt.label }}</button>
      </div>

      <el-pagination
        v-if="pageSize !== ALL"
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next, jumper"
        :total="filtrados.length"
        background
      />
      <span v-else class="ps-all-msg">Mostrando todos los {{ filtrados.length }} registros</span>
    </div>

    <!-- Modal -->
    <el-dialog v-model="showForm" :title="editando ? 'Editar Movimiento' : 'Nuevo Movimiento'" width="540px" destroy-on-close>
      <MovimientoForm :grupos="grupos" :tipos="tipos" :inicial="editando" @guardado="onGuardado" @cancelar="showForm = false" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, EditPen, Delete, Plus, Download, Document } from '@element-plus/icons-vue'
import api from '@/services/api'
import MovimientoForm from '@/components/movimientos/MovimientoForm.vue'

const ALL = 99999
const pageSizeOpts = [
  { label: '10',   value: 10 },
  { label: '20',   value: 20 },
  { label: '50',   value: 50 },
  { label: '100',  value: 100 },
  { label: 'Todos', value: ALL },
]

const movimientos = ref([])
const grupos = ref([])
const tipos = ref([])
const showForm = ref(false)
const editando = ref(null)
const buscar = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const filtros = ref({ rango: null, grupo_id: null, tipo_id: null })

function setPageSize(v) { pageSize.value = v; currentPage.value = 1 }

function tipoTag(n) { return n === 'INGRESO' ? 'success' : n === 'EGRESO' ? 'danger' : 'warning' }
function rowClass({ row }) { return row.monto_ingreso > 0 ? 'row-ingreso' : 'row-egreso' }
function fmt(v) { return Number(v || 0).toFixed(2) }

const filtrados = computed(() => {
  if (!buscar.value) return movimientos.value
  const q = buscar.value.toLowerCase()
  return movimientos.value.filter(m =>
    m.descripcion.toLowerCase().includes(q) ||
    m.grupo.nombre.toLowerCase().includes(q)
  )
})

const paginados = computed(() => {
  if (pageSize.value === ALL) return filtrados.value
  const start = (currentPage.value - 1) * pageSize.value
  return filtrados.value.slice(start, start + pageSize.value)
})

const totalIngreso = computed(() => filtrados.value.reduce((s, m) => s + m.monto_ingreso, 0))
const totalEgreso  = computed(() => filtrados.value.reduce((s, m) => s + m.monto_egreso, 0))
const balance      = computed(() => totalIngreso.value - totalEgreso.value)

function filtrarLocal() { currentPage.value = 1 }

async function cargar() {
  const params = {}
  if (filtros.value.rango) { params.fecha_desde = filtros.value.rango[0]; params.fecha_hasta = filtros.value.rango[1] }
  if (filtros.value.grupo_id) params.grupo_id = filtros.value.grupo_id
  if (filtros.value.tipo_id) params.tipo_id = filtros.value.tipo_id
  const { data } = await api.get('/movimientos/', { params: { ...params, limit: 500, desc: true } })
  movimientos.value = data
  currentPage.value = 1
}

function editar(row) { editando.value = row; showForm.value = true }

async function eliminar(id) {
  await api.delete(`/movimientos/${id}`)
  ElMessage.success('Movimiento eliminado')
  cargar()
}

function limpiar() {
  filtros.value = { rango: null, grupo_id: null, tipo_id: null }
  buscar.value = ''
  cargar()
}

function onGuardado() { showForm.value = false; cargar() }

const exportandoExcel = ref(false)
const exportandoPdf   = ref(false)

function buildExportParams() {
  const params = {}
  if (filtros.value.rango) { params.fecha_desde = filtros.value.rango[0]; params.fecha_hasta = filtros.value.rango[1] }
  if (filtros.value.grupo_id) params.grupo_id = filtros.value.grupo_id
  if (filtros.value.tipo_id)  params.tipo_id  = filtros.value.tipo_id
  return params
}

async function exportarExcel() {
  exportandoExcel.value = true
  try {
    const resp = await api.get('/movimientos/exportar/excel', { params: buildExportParams(), responseType: 'blob' })
    const url = URL.createObjectURL(new Blob([resp.data]))
    const a = document.createElement('a'); a.href = url; a.download = 'fayni_movimientos.xlsx'; a.click()
    URL.revokeObjectURL(url)
  } finally { exportandoExcel.value = false }
}

async function exportarPdf() {
  exportandoPdf.value = true
  try {
    const resp = await api.get('/movimientos/exportar/pdf', { params: buildExportParams(), responseType: 'blob' })
    const url = URL.createObjectURL(new Blob([resp.data], { type: 'application/pdf' }))
    const a = document.createElement('a'); a.href = url; a.download = 'fayni_movimientos.pdf'; a.click()
    URL.revokeObjectURL(url)
  } finally { exportandoPdf.value = false }
}

onMounted(async () => {
  const [g, t] = await Promise.all([api.get('/catalogos/grupos'), api.get('/catalogos/tipos')])
  grupos.value = g.data
  tipos.value = t.data
  cargar()
})
</script>

<style scoped>
.dt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.filter-card { margin-bottom: 0.75rem; }
:deep(.filter-card .el-card__body) { padding: 12px 16px; }

.dt-info-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px 8px 0 0;
  font-size: 0.82rem;
  color: #64748b;
}

.totales-bar { display: flex; gap: 1.5rem; }
.totales-bar span strong { font-size: 0.9rem; }

.dt-wrapper {
  border: 1px solid #e2e8f0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  overflow: hidden;
}

.dt-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.page-size-selector {
  display: flex;
  align-items: center;
  gap: 4px;
}

.ps-label {
  font-size: 0.82rem;
  color: #64748b;
  margin-right: 4px;
}

.ps-btn {
  padding: 4px 10px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  color: #374151;
  transition: all 0.15s;
}

.ps-btn:hover { border-color: #6366f1; color: #6366f1; }

.ps-btn.active {
  background: #6366f1;
  border-color: #6366f1;
  color: white;
  font-weight: 600;
}

.ps-all-msg {
  font-size: 0.82rem;
  color: #6366f1;
  font-weight: 600;
}

.desc-cell {
  display: block;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.85rem;
}

.grupo-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 20px;
  border: 1px solid;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.monto-cell {
  font-weight: 700;
  font-size: 0.88rem;
  font-variant-numeric: tabular-nums;
}

:deep(.row-ingreso td) { background: #f0fdf4 !important; }
:deep(.row-egreso td)  { background: #fff5f5 !important; }
:deep(.el-table__row:hover td) { filter: brightness(0.96); }
</style>
