<template>
    <b-container>
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
                  
                  <b-navbar-nav class="ml-auto">
                    <button class="btn btn-danger" v-if="token" @click="exitApp()">Logout</button>
                  </b-navbar-nav>
                </b-collapse>
              </b-navbar>
            </div>
          </div>
          <h1 >Welcome To Quantified Self!</h1>
          <h2 id="tracker_heading" class="mt-5">Your Trackers</h2>
          <button @click="createTracker()" id="btn_" class="btn btn-primary">Create new Tracker</button>
          <button @click="generateReport()" id="btn_" class="btn btn-primary">Export Trackers</button>
          <br/><br/>
          <b-row id="rows">
            <b-col v-for="r in result" :key="r.tracker_id">
              <b-button @click="DeleteTracker(r.tracker_id)" variant="danger">Delete</b-button>
              <b-button @click="EditTracker(r.tracker_id)" variant="warning">Edit</b-button>
              <b-card >
                  <b-card-text>
                    Name : {{ r.name }}
                  </b-card-text>

                  <b-button :href="'/tracker/' + r.tracker_id" variant="primary">Track</b-button>
              </b-card>
            </b-col>
          </b-row>

        <b-form @submit="EditThisTracker()" v-if="visible">
          <b-form-group
            id="input-group-1"
            label="Tracker Name:"
            label-for="input-1"
            description=""
          >
            <b-form-input
              id="input-1"
              v-model="editForm.name"
              type="text"
              placeholder="Tracker Name"
              required
            ></b-form-input>
          </b-form-group>
    
          <b-dropdown name="tracker_type" id="dropdown-1" text="Tracker type" class="m-md-2">
              <b-dropdown-item active>Numerical</b-dropdown-item>
              <b-dropdown-item>Mutiple Choice</b-dropdown-item>
              <b-dropdown-item>String</b-dropdown-item>
          </b-dropdown>

          <b-form-group
            id="input-group-1"
            label="Enter Tracker Description:"
            label-for="input-1"
            description=""
          >
            <b-form-input
              id="input-1"
              v-model="editForm.desc"
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
              v-model="editForm.settings"
              type="text"
              placeholder="Enter Tracker Settings"
              required
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Edit Tracker</b-button>
        </b-form>
        <VueHtml2pdf
          :show-layout="false"
          :float-layout="true"
          :enable-download="true"
          :preview-modal="true"
          :paginate-elements-by-height="1400"
          filename="trackers"
          :pdf-quality="2"
          :manual-pagination="false"
          pdf-format="a4"
          pdf-orientation="landscape"
          pdf-content-width="800px"
          ref="html2Pdf"
      >
      <div slot="pdf-content">
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
                  
                  <b-navbar-nav class="ml-auto">
                    <button class="btn btn-danger" v-if="token" @click="exitApp()">Logout</button>
                  </b-navbar-nav>
                </b-collapse>
              </b-navbar>
            </div>
          </div>
          <h1 >Welcome To Quantified Self!</h1>
          <h2 id="tracker_heading" class="mt-5">Your Trackers</h2>
          <button @click="createTracker()" id="btn_" class="btn btn-primary">Create new Tracker</button>
          <button @click="generateReport()" id="btn_" class="btn btn-primary">Export Trackers</button>
          <br/><br/>
          <b-row id="rows">
            <b-col v-for="r in result" :key="r.tracker_id">
              <b-button @click="DeleteTracker(r.tracker_id)" variant="danger">Delete</b-button>
              <b-button @click="EditTracker(r.tracker_id)" variant="warning">Edit</b-button>
              <b-card >
                  <b-card-text>
                    Name : {{ r.name }}
                  </b-card-text>

                  <b-button :href="'/tracker/' + r.tracker_id" variant="primary">Track</b-button>
              </b-card>
            </b-col>
          </b-row>

        <b-form @submit="EditThisTracker()" v-if="visible">
          <b-form-group
            id="input-group-1"
            label="Tracker Name:"
            label-for="input-1"
            description=""
          >
            <b-form-input
              id="input-1"
              v-model="editForm.name"
              type="text"
              placeholder="Tracker Name"
              required
            ></b-form-input>
          </b-form-group>
    
          <b-dropdown name="tracker_type" id="dropdown-1" text="Tracker type" class="m-md-2">
              <b-dropdown-item active>Numerical</b-dropdown-item>
              <b-dropdown-item>Mutiple Choice</b-dropdown-item>
              <b-dropdown-item>String</b-dropdown-item>
          </b-dropdown>

          <b-form-group
            id="input-group-1"
            label="Enter Tracker Description:"
            label-for="input-1"
            description=""
          >
            <b-form-input
              id="input-1"
              v-model="editForm.desc"
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
              v-model="editForm.settings"
              type="text"
              placeholder="Enter Tracker Settings"
              required
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Edit Tracker</b-button>
        </b-form>
      </div>
    </VueHtml2pdf>
    </b-container>
</template>
<style scoped>
    #tracker_heading{
        float: left;
    }

    #btn_{
        float: right;
    }
    #rows{
      margin-top: 100px;
    }
</style>

<script>
    import axios from 'axios';
    import VueHtml2pdf from 'vue-html2pdf';
    export default {
      components: {
          VueHtml2pdf
      },
      data(){
        return {
          result:'',
          visible:'',
          id:'',
          editForm:{
            name:'',
            desc:'',
            tracker_type:'',
            settings:'',
            id:''
          },
          token:this.getCookie()
        }
      },
      created(){
        axios.get('http://127.0.0.1:5000/tracker/' + this.getUsername(),
          { headers: {
            'Content-type': 'application/json',
            'Authorization':'Bearer ' + this.getCookie(),
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then((response)=>{
            if(response.status == 200){
              this.result = response.data;
            }
          })
      },methods:{
        generateReport () {
            this.$refs.html2Pdf.generatePdf()
        },
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
        createTracker(){
          this.$router.push('/tracker/create')
        },
        DeleteTracker(id){
          console.log('http://127.0.0.1:5000/tracker/'+ this.getUsername() + '/' + id);
          axios.delete('http://127.0.0.1:5000/tracker/'+ this.getUsername() + '/' + id,
          { headers: {
            'Content-type': 'application/json',
            'Authorization':'Bearer ' +  this.getCookie(),
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then((res)=>{
            if(res.status == 200){
              this.$router.go();
            }
          })
        },
        EditTracker(id){
          this.visible = 'edit';
          axios.get('http://127.0.0.1:5000/tracker/' + this.getUsername() + '/' + id,
          { headers: {
            'Content-type': 'application/json',
            'Authorization':'Bearer ' + this.getCookie(),
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then((response)=>{
            if(response.status == 200){
              this.editForm.name = response.data[0].name;
              this.id = response.data[0].tracker_id;
              this.editForm.desc = response.data[0].desc;
              this.editForm.tracker_type = response.data[0].tracker_type;
              this.editForm.settings = response.data[0].settings;
            }
          })
        },
        EditThisTracker(){
          this.visible = '';
          console.log('http://127.0.0.1:5000/tracker/' + this.getUsername() + '/' + this.id);
          axios.put('http://127.0.0.1:5000/tracker/' + this.getUsername() + '/' + this.id,
          {
              name: this.editForm.name,
              desc:this.editForm.desc,
              tracker_type:this.editForm.tracker_type,
              settings: this.editForm.settings
          },
          { headers: {
            'Content-type': 'application/json',
            'Authorization':'Bearer ' + this.getCookie(),
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then((response)=>{
            if(response.status == 200){
              this.$router.go();
            }
          })
        }
      }
    }
  </script>