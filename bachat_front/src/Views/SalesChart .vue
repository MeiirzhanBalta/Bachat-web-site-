<template>
  <canvas ref="salesChart"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns'; // Adapter for date-fns

export default {
  name: 'SalesChart',
  props: {
    sales: {
      type: Array,
      required: true
    },
    timeRange: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      chart: null
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.createChart();
    });
  },
  methods: {
    getUnitForTimeRange() {
      if (this.timeRange === 'week') {
        return 'day';
      } else if (this.timeRange === 'month') {
        return 'week';
      } else if (this.timeRange === 'year') {
        return 'month';
      }
      return 'day';
    },
    createChart() {
      this.destroyChart(); 

      const canvas = this.$refs.salesChart;
      if (!canvas) {
        console.error('Canvas element not found!');
        return;
      }

      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error('Failed to get context from canvas element!');
        return;
      }

      const unit = this.getUnitForTimeRange();

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.sales.map(sale => new Date(sale.date)),
          datasets: [{
            label: 'Sales in EUR',
            data: this.sales.map(sale => sale.amount),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: unit,
                tooltipFormat: 'MMM d, yyyy', // Format for tooltip
                displayFormats: {
                  day: 'MMM d, yyyy',
                  week: 'MMM d',
                  month: 'MMM yyyy'
                }
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    }
  },
  watch: {
    sales: {
      deep: true,
      handler() {
        this.$nextTick(() => {
          this.createChart();
        });
      }
    },
    timeRange() {
      this.$nextTick(() => {
        this.createChart();
      });
    }
  },
  beforeUnmount() {
    this.destroyChart();
  }
};
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>
