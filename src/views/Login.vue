<template>
    <b-container>
      <div id="nav">
        <div>
          <b-navbar toggleable="lg" type="light" variant="info" class="bg-white">
            <b-navbar-brand><a href="/">Quantified Self</a></b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-navbar-nav class="ml-auto">
              <b-nav-item class="btn btn-success mr-5"><router-link to="/login">Login</router-link></b-nav-item>
              <b-nav-item class="btn btn-primary"><router-link to="/signup">Signup</router-link></b-nav-item>
            </b-navbar-nav>

          </b-navbar>
        </div>
      </div>
      <b-form @submit="onSubmit">
        <b-form-group
          id="input-group-1"
          label="Enter Username:"
          label-for="input-1"
          description=""
        >
          <b-form-input
            id="input-1"
            v-model="form.username"
            type="text"
            placeholder="Enter username"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Your Password:" label-for="input-2">
          <b-form-input
            id="input-2"
            type="password"
            v-model="form.pswd"
            placeholder="Enter Password"
            required
          ></b-form-input>
        </b-form-group>
  
        <b-button type="submit" variant="primary">Login</b-button>
      </b-form>
    </b-container>
  </template>
  
  <script>
import axios from 'axios';
import router from '../router';
    export default {
      data() {
        return {
          form: {
            username:'',
            pswd:''
          },
        }
      },
      methods: {
        onSubmit(event) {
          event.preventDefault();
          axios.post('http://127.0.0.1:5000/api/login',{
            username:this.form.username,
            pswd:this.form.pswd
          },{ headers: {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then(response=>{
            if(response.status == 200){
              this.$cookies.set("token", response.data.token, 30 * 24 * 60 * 60 * 1000)
              this.$cookies.set("username", response.data.username, 30 * 24 * 60 * 60 * 1000)
              router.push('/tracker/')
            }
          })
        }
      }
    }
  </script>