<template>
  <div class="statistic-page-container">
    <h1>Sales Statistics</h1>
    <div>
      <h2 class="h22">Enter sales data:</h2>
      <div class="inputStat">
        <input type="number" v-model.number="newSaleAmount" placeholder="Sales Amount (EUR)">
        <input type="date" v-model="newSaleDate">
      </div>
      <button @click="addSale">Add</button>
    </div>
    <div class="time-range-selector">
      <label for="timeRange">Select time range:</label>
    </div>
    <div class="sales-list">
      <div class="sale-item" v-for="sale in filteredSales" :key="sale.id">
        <div class="sale-date">{{ sale.date }}</div>
        <div class="sale-amount">{{ sale.amount }} EUR</div>
        <button @click="deleteSale(sale.id)" class="delete-button">Delete</button>
      </div>
    </div>
    <div class="font-stat">
      <h2>Total Statistics:</h2>
      <p class="font">Total Sales Amount: {{ totalSales }} EUR</p>
      <p class="font">Average Sales Amount: {{ averageSales }} EUR</p>
    </div>
    <div class="chart">
      <SalesChart :sales="filteredSales" :timeRange="timeRange" />
    </div>
  </div>
</template>

<script>
import SalesChart from './SalesChart .vue';
import ApiService from '@/services/ApiService';

export default {
  components: {
    SalesChart
  },
  name: 'StatisticPage',
  data() {
    return {
      newSaleAmount: '',
      newSaleDate: '',
      sales: [],
      timeRange: 'week'
    };
  },
  computed: {
    filteredSales() {
      const now = new Date();
      let filteredSales = [];

      if (this.timeRange === 'week') {
        const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        filteredSales = this.sales.filter(sale => new Date(sale.date) >= oneWeekAgo);
      } else if (this.timeRange === 'month') {
        const oneMonthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        filteredSales = this.sales.filter(sale => new Date(sale.date) >= oneMonthAgo);
      } else if (this.timeRange === 'year') {
        const oneYearAgo = new Date(now.setFullYear(now.getFullYear() - 1));
        filteredSales = this.sales.filter(sale => new Date(sale.date) >= oneYearAgo);
      }

      return filteredSales;
    },
    totalSales() {
      return this.filteredSales.reduce((sum, sale) => sum + parseFloat(sale.amount), 0).toFixed(2);
    },
    averageSales() {
      return this.filteredSales.length ? (this.totalSales / this.filteredSales.length).toFixed(2) : '0.00';
    }
  },
  methods: {
    async addSale() {
      if (this.newSaleDate && this.newSaleAmount) {
        try {
          const response = await ApiService.post('/sales', {
            amount: parseFloat(this.newSaleAmount),
            date: this.newSaleDate
          }, {
            withCredentials: true
          });
          this.sales.push(response.data);
          this.newSaleAmount = '';
          this.newSaleDate = '';
        } catch (error) {
          console.error('Error adding sale:', error);
        }
      }
    },
    
    async deleteSale(saleId) {
      try {
        await ApiService.deleteSale(saleId);
        this.sales = this.sales.filter(sale => sale.id !== saleId);
      } catch (error) {
        console.error('Error deleting sale:', error);
      }
    }
  },
  async mounted() {
    document.body.style.backgroundColor = "#f0f0f0";
  }
};
</script>

<style scoped>
.chart {
  height: 450px;
  width: 800px;
  box-shadow: 0 0.5px 80px 5px rgba(0, 0, 0, 0.1);
}

.statistic-page-container {
  font-family: "PT Sans", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1125px;
  padding: 20px;
  background-color: rgb(240, 240, 240);
}

.h22 {
  font-weight: bold;
  margin-bottom: 2%;
  font-size: 24px;
}

.inputStat {
  margin-bottom: 4%;
  width: 100%;
  display: flex;
  gap: 20px;
}

.inputStat input[type="number"],
.inputStat input[type="date"] {
  flex-grow: 1;
  padding: 15px 20px;
  font-size: 18px;
  border: 2px solid #ccc;
  border-radius: 8px;
}

button {
  padding: 15px 30px;
  font-size: 20px;
  background-color: #183961;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

.time-range-selector {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-range-selector select {
  padding: 10px;
  font-size: 18px;
  border: 2px solid #ccc;
  border-radius: 8px;
}

.sales-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
}

.sale-item {
  flex: 1 1 calc(50% - 20px);
  display: flex;
  flex-direction: column;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
}

.sale-date,
.sale-amount {
  margin: 5px 0;
}

.delete-button {
  align-self: flex-start;
  margin-top: 5px;
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.font-stat {
  font-size: 20px;
  padding: 25px;
}
</style>