// Dashboard JavaScript para Biotica Nexus

// Variables globales
let readingsChart = null;
let statusChart = null;

// Elementos del DOM
const totalSensorsEl = document.getElementById('totalSensors');
const activeSensorsEl = document.getElementById('activeSensors');
const maintenanceSensorsEl = document.getElementById('maintenanceSensors');
const totalReadingsEl = document.getElementById('totalReadings');
const lastReadingTimeEl = document.getElementById('lastReadingTime');
const sensorTypesEl = document.getElementById('sensorTypes');
const tempCountEl = document.getElementById('tempCount');
const humidityCountEl = document.getElementById('humidityCount');
const averageValueEl = document.getElementById('averageValue');
const valueRangeEl = document.getElementById('valueRange');
const sensorsTableBody = document.getElementById('sensorsTableBody');
const lastUpdateEl = document.getElementById('lastUpdate');
const refreshBtn = document.getElementById('refreshBtn');

// Formatear tiempo relativo
function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'hace unos segundos';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `hace ${minutes} min`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `hace ${hours} h`;
    const days = Math.floor(hours / 24);
    return `hace ${days} días`;
}

// Formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-CO', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Obtener datos de la API
async function fetchData() {
    try {
        // Obtener sensores
        const sensorsResponse = await fetch('/sensores/');
        const sensors = await sensorsResponse.json();
        
        // Obtener lecturas
        const readingsResponse = await fetch('/lecturas/?limit=20');
        const readings = await readingsResponse.json();
        
        return { sensors, readings };
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

// Actualizar tarjetas
function updateCards(sensors, readings) {
    // Total de sensores
    totalSensorsEl.textContent = sensors.length;
    
    // Contar sensores por estado
    const activeCount = sensors.filter(s => s.estado === 'activo').length;
    const maintenanceCount = sensors.filter(s => s.estado === 'mantenimiento').length;
    const inactiveCount = sensors.filter(s => s.estado === 'inactivo').length;
    
    activeSensorsEl.textContent = activeCount;
    maintenanceSensorsEl.textContent = maintenanceCount;
    
    // Total de lecturas
    totalReadingsEl.textContent = readings.length;
    
    // Última lectura
    if (readings.length > 0) {
        const lastReading = readings[0];
        lastReadingTimeEl.textContent = timeAgo(lastReading.timestamp);
    } else {
        lastReadingTimeEl.textContent = 'N/A';
    }
    
    // Tipos de sensores
    const types = [...new Set(sensors.map(s => s.tipo))];
    sensorTypesEl.textContent = types.length;
    
    // Contar por tipo específico
    const tempCount = sensors.filter(s => s.tipo.toLowerCase().includes('temp')).length;
    const humidityCount = sensors.filter(s => s.tipo.toLowerCase().includes('hum')).length;
    
    tempCountEl.textContent = tempCount;
    humidityCountEl.textContent = humidityCount;
    
    // Valor promedio y rango
    if (readings.length > 0) {
        const values = readings.map(r => r.valor);
        const avg = values.reduce((a, b) => a + b, 0) / values.length;
        const min = Math.min(...values);
        const max = Math.max(...values);
        
        averageValueEl.textContent = avg.toFixed(2);
        valueRangeEl.textContent = `${min.toFixed(1)} - ${max.toFixed(1)}`;
    } else {
        averageValueEl.textContent = '0.00';
        valueRangeEl.textContent = '0 - 0';
    }
}

// Actualizar tabla de sensores
function updateSensorsTable(sensors) {
    // Limpiar tabla
    sensorsTableBody.innerHTML = '';
    
    if (sensors.length === 0) {
        sensorsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                    No hay sensores registrados
                </td>
            </tr>
        `;
        return;
    }
    
    // Agregar cada sensor a la tabla
    sensors.forEach(sensor => {
        // Determinar color del estado
        let statusColor = 'bg-gray-100 text-gray-800';
        if (sensor.estado === 'activo') statusColor = 'bg-green-100 text-green-800';
        if (sensor.estado === 'mantenimiento') statusColor = 'bg-yellow-100 text-yellow-800';
        if (sensor.estado === 'inactivo') statusColor = 'bg-red-100 text-red-800';
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${sensor.id}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${sensor.tipo}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${sensor.ubicacion}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColor}">
                    ${sensor.estado}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                ${sensor.lecturas_count || 0}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${sensor.ultima_lectura ? timeAgo(sensor.ultima_lectura) : 'N/A'}
            </td>
        `;
        sensorsTableBody.appendChild(row);
    });
}

// Crear gráfico de lecturas
function createReadingsChart(readings) {
    const ctx = document.getElementById('readingsChart').getContext('2d');
    
    // Ordenar lecturas por fecha (más recientes primero)
    const sortedReadings = [...readings].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    
    // Tomar las últimas 10 lecturas para el gráfico
    const chartReadings = sortedReadings.slice(-10);
    
    const labels = chartReadings.map(r => {
        const date = new Date(r.timestamp);
        return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    });
    
    const data = chartReadings.map(r => r.valor);
    
    if (readingsChart) {
        readingsChart.destroy();
    }
    
    readingsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Valor de Lectura',
                data: data,
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        drawBorder: false
                    },
                    title: {
                        display: true,
                        text: 'Valor'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Hora'
                    }
                }
            }
        }
    });
}

// Crear gráfico de estado de sensores
function createStatusChart(sensors) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    
    // Contar sensores por estado
    const statusCounts = {
        activo: sensors.filter(s => s.estado === 'activo').length,
        mantenimiento: sensors.filter(s => s.estado === 'mantenimiento').length,
        inactivo: sensors.filter(s => s.estado === 'inactivo').length
    };
    
    if (statusChart) {
        statusChart.destroy();
    }
    
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Activo', 'Mantenimiento', 'Inactivo'],
            datasets: [{
                data: [statusCounts.activo, statusCounts.mantenimiento, statusCounts.inactivo],
                backgroundColor: [
                    'rgb(34, 197, 94)',
                    'rgb(234, 179, 8)',
                    'rgb(239, 68, 68)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Actualizar todo el dashboard
async function updateDashboard() {
    try {
        // Mostrar estado de carga
        lastUpdateEl.innerHTML = '<span class="loading"></span> Actualizando...';
        
        // Obtener datos
        const { sensors, readings } = await fetchData();
        
        // Actualizar componentes
        updateCards(sensors, readings);
        updateSensorsTable(sensors);
        createReadingsChart(readings);
        createStatusChart(sensors);
        
        // Actualizar timestamp
        lastUpdateEl.textContent = `Actualizado: ${new Date().toLocaleTimeString('es-CO')}`;
        
        console.log('Dashboard actualizado exitosamente');
    } catch (error) {
        console.error('Error actualizando dashboard:', error);
        lastUpdateEl.innerHTML = '<span class="text-red-600">Error cargando datos</span>';
        
        // Mostrar mensaje de error en la tabla
        sensorsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-8 text-center text-red-600">
                    <i class="fas fa-exclamation-triangle mr-2"></i>
                    Error conectando con la API. Verifica que el servidor esté ejecutándose.
                </td>
            </tr>
        `;
    }
}

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos iniciales
    updateDashboard();
    
    // Configurar botón de actualización
    refreshBtn.addEventListener('click', updateDashboard);
    
    // Actualizar automáticamente cada 30 segundos
    setInterval(updateDashboard, 30000);
    
    // Configurar botones del gráfico
    const chartDayBtn = document.getElementById('chartDay');
    const chartWeekBtn = document.getElementById('chartWeek');
    const chartMonthBtn = document.getElementById('chartMonth');
    
    if (chartDayBtn) {
        chartDayBtn.addEventListener('click', function() {
            chartDayBtn.classList.remove('bg-gray-100', 'text-gray-700');
            chartDayBtn.classList.add('bg-blue-100', 'text-blue-700');
            chartWeekBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartWeekBtn.classList.add('bg-gray-100', 'text-gray-700');
            chartMonthBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartMonthBtn.classList.add('bg-gray-100', 'text-gray-700');
            // Aquí se podría cambiar el rango del gráfico
        });
    }
    
    if (chartWeekBtn) {
        chartWeekBtn.addEventListener('click', function() {
            chartWeekBtn.classList.remove('bg-gray-100', 'text-gray-700');
            chartWeekBtn.classList.add('bg-blue-100', 'text-blue-700');
            chartDayBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartDayBtn.classList.add('bg-gray-100', 'text-gray-700');
            chartMonthBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartMonthBtn.classList.add('bg-gray-100', 'text-gray-700');
        });
    }
    
    if (chartMonthBtn) {
        chartMonthBtn.addEventListener('click', function() {
            chartMonthBtn.classList.remove('bg-gray-100', 'text-gray-700');
            chartMonthBtn.classList.add('bg-blue-100', 'text-blue-700');
            chartDayBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartDayBtn.classList.add('bg-gray-100', 'text-gray-700');
            chartWeekBtn.classList.remove('bg-blue-100', 'text-blue-700');
            chartWeekBtn.classList.add('bg-gray-100', 'text-gray-700');
        });
    }
});