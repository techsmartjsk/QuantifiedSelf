import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue';
import Tracker from "../views/Tracker.vue"
import CreateTracker from "../views/CreateTracker.vue"
import TrackLogs from "../views/TrackLogs.vue"
import TrendLines from "../views/Trendlines.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: Signup
  },
  {
    path: '/tracker/create',
    name: 'My Trackers',
    component: CreateTracker
  },
  {
    path: '/tracker',
    name: 'Our App',
    component: Tracker
  },
  {
    path:'/tracker/:id',
    name:'Track Logs',
    component:TrackLogs
  },
  {
    path:'/trendlines/:id',
    name:'Trend Lines',
    component: TrendLines
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
