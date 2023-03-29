import { Line } from "vue-chartjs";

export default {
  extends: Line,
  props: ["chartData"],
  data() {
    return {
      options: {
        //Chart.js options
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }
          ],
          xAxes: [
            {
              gridLines: {
                display: false
              }
            }
          ]
        },
        legend: {
          display: false
        },
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  mounted() {
    this.render();
  },
  methods: {
    render() {
      console.log(this.chartdata)
      this.renderChart(this.chartdata, this.options);
    }
  }
};
