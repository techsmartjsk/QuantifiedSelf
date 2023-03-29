<template>
  
  <div class="container">
    <div id="nav">
          <div>
            <b-navbar toggleable="lg" type="light" variant="info" class="bg-white">
              <b-navbar-brand><a href="/">Quantified Self</a></b-navbar-brand>

              <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

              <b-collapse id="nav-collapse" is-nav class="ml-auto">
                <b-navbar-nav class="ml-auto">
                  <b-nav-item><router-link to="/">Home</router-link></b-nav-item>
                  <b-nav-item><router-link to="/tracker">My Trackers</router-link></b-nav-item>
                </b-navbar-nav>
                
                <b-navbar-nav class="ml-auto">
                  <button class="btn btn-danger" @click="exitApp()">Logout</button>
                </b-navbar-nav>
              </b-collapse>
            </b-navbar>
          </div>
        </div>

        <h3>Your Trendlines </h3>
    <Bar v-if="loaded" :chart-data="chartData" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  data: () => ({
    loaded: false,
    chartData: {
      labels: [],
        datasets: [
          {
            label: 'Daily Logs',
            backgroundColor: '#f87979',
            data: []
          }
        ]
    },
    TrackerName:'',
  }),
  async mounted () {
    this.loaded = false

    try {
      const url = 'http://127.0.0.1:5000/tracker/' + this.$route.params.id + '/';
      axios.get(url,
          { headers: {
              'Content-type': 'application/json',
              'Authorization':'Bearer ' + this.getCookie(),
              'Access-Control-Allow-Origin' : '*',
              'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
              }
          }
      ).then(response=>{
          const dataArr=[];
          const labelArr = [];
          for(var i=0;i < response.data.length; i++){
            dataArr.push(response.data[i].value)
          }
          for(var j=1;j<=31;j++){
            labelArr.push('Log' + j)
          }
          this.chartData.datasets[0].data = dataArr
          this.chartData.labels = labelArr
      })

      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  },
  methods:{
    getCookie(){
      return this.$cookies.get('token')
    }
  }
}
</script>