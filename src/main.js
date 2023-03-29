import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VeeValidate from "vee-validate"
import VueCookies from "vue-cookies";
import './registerServiceWorker'

Vue.use(VeeValidate);
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VueCookies)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
