<template>
  <div class="home">
    <div id="nav">
    <div>
      <b-navbar toggleable="lg" type="light" variant="info" class="bg-white">
        <b-navbar-brand><a href="/">Quantified Self</a></b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav class="ml-auto">
          <b-navbar-nav class="ml-auto">
            <b-nav-item v-if="token"><router-link to="/">Home</router-link></b-nav-item>
            <b-nav-item v-if="token"><router-link to="/tracker">My Trackers</router-link></b-nav-item>
          </b-navbar-nav>
          
          <b-navbar-nav class="ml-auto" v-if="!token">
            <b-nav-item class="btn btn-success mr-5"><router-link to="/login">Login</router-link></b-nav-item>
            <b-nav-item class="btn btn-primary"><router-link to="/signup">Signup</router-link></b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </div>
    <div class="d-flex container gap-5">
      <div id="main">
        Welcome to Quantified Self!
      </div>
      <div>
        <img id="mainImg" src="../assets/main.svg">
      </div>
    </div>
  </div>
</template>

<style scoped>
  #main{
    font-size: 50px;
    width:50%;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin-top: 100px;
  }
  #mainImg{
    width: 600px;
  }
</style>

<script>
export default {
  name: 'Home',
  data(){
    return {
      token : this.getCookie()
    }
  },
  methods:{
    getCookie(){
      return this.$cookies.get('token')
    }
  }
}
</script>
