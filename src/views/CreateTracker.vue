<template>
  <b-container>
    <div id="nav">
    <div>
      <b-navbar toggleable="lg" type="light" variant="info" class="bg-white">
        <b-navbar-brand><a href="/">Quantified Self</a></b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav class="ml-auto">
          <b-navbar-nav class="ml-auto">
            <b-nav-item><router-link to="/">Home</router-link></b-nav-item>
            <b-nav-item v-if="token"><router-link to="/tracker">My Trackers</router-link></b-nav-item>
          </b-navbar-nav>
          
          <b-navbar-nav class="ml-auto">
            <button class="btn btn-danger" @click="exitApp()">Logout</button>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </div>
  <b-form @submit="submit">
        <b-form-group
          id="input-group-1"
          label="Enter Tracker Name:"
          label-for="input-1"
          description=""
        >
          <b-form-input
            id="input-1"
            v-model="form.name"
            type="text"
            placeholder="Enter Tracker Name"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-1"
          label="Enter Tracker Type:"
          label-for="input-1"
          description=""
        >
  
        <b-form-select v-model="form.tracker_type"  id="dropdown-1" text="Tracker type" class="m-md-2">
            <b-form-select-option value="Numerical">Numerical</b-form-select-option>
            <b-form-select-option value="Mutiple Choice">Mutiple Choice</b-form-select-option>
            <b-form-select-option value="String">String</b-form-select-option>
        </b-form-select>

        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Enter Tracker Description:"
          label-for="input-1"
          description=""
        >
          <b-form-input
            id="input-1"
            v-model="form.desc"
            type="text"
            placeholder="Enter Tracker Description"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-1"
          label="Enter Tracker Settings:"
          label-for="input-1"
          description=""
        >
          <b-form-input
            id="input-1"
            v-model="form.settings"
            type="text"
            placeholder="Enter Tracker Settings"
            required
          ></b-form-input>
        </b-form-group>
  
        <b-button type="submit" variant="primary">Create Tracker</b-button>
      </b-form>
  </b-container>
</template>
<script>
    import axios from 'axios';
    import router from "../router";

    export default {
      data() {
        return {
          form: {
            name:'',
            tracker_type:'',
            desc:'',
            settings:'',
            user_id:''
          },
          token:this.getCookie()
        }
      },methods:{
        getUsername(){
          return this.$cookies.get('username')
        },
        getCookie(){
          return this.$cookies.get('token')
        },
        exitApp(){
          this.$cookies.remove('token')
          this.$cookies.remove('username')
          this.$router.push('/')
        },
        submit(event){
        event.preventDefault()
            axios.post('http://127.0.0.1:5000/tracker/' + this.getUsername(),
          {
            tracker_id:this.form.tracker_id,
            name:this.form.name,
            tracker_type:this.form.tracker_type,
            desc:this.form.desc,
            settings:this.form.settings,
          }, // the data to post
          { headers: {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            'Authorization':'Bearer ' + this.getCookie()
            }
          }).then((response)=>{
            if(response.status == 200){
                router.push('/tracker')
            }else{
              console.log("Not Created");
            }
          })
        }
      }
    }
</script>