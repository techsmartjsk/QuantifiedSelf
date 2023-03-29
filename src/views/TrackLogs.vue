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
                  <b-nav-item><router-link to="/tracker">My Trackers</router-link></b-nav-item>
                </b-navbar-nav>
                
                <b-navbar-nav class="ml-auto">
                  <button class="btn btn-danger" @click="exitApp()">Logout</button>
                </b-navbar-nav>
              </b-collapse>
            </b-navbar>
          </div>
        </div>
        <b-row v-if="logs" id="rows">
          <b-col v-for="l in logs" :key="l.id">
            <b-button @click="DeleteLog(l.id)" variant="danger">Delete</b-button>
            <b-button @click="EditLog(l.id)" variant="warning">Edit</b-button>
            <b-card >
                <b-card-text>
                  Value : {{ l.value }}
                </b-card-text>
                <b-card-text>
                  Timestamp : {{ l.timestamp }}
                </b-card-text>
                <b-card-text>
                  Value : {{ l.note }}
                </b-card-text>
              </b-card>
          </b-col>
        </b-row>
        <b-button :href="'/trendlines/' + this.$route.params.id"  class="btn btn-success">View Trendlines</b-button>
        <button @click="AddTodayLog()" class="btn btn-primary">
            Add Today's Log
        </button>
        
    <b-form v-if="visible">
            <b-form-group
            id="input-group-1"
            label="Edit Timestamp"
            label-for="input-1"
            description=""
            >
            <b-form-input
                id="input-1"
                v-model="form.timestamp"
                type="text"
                placeholder="Enter Timestamp"
                required
            ></b-form-input>
            </b-form-group>


            <b-form-group
            id="input-group-1"
            label="Enter Log Value:"
            label-for="input-1"
            description=""
            >
            <b-form-input
                id="input-1"
                v-model="form.value"
                type="text"
                placeholder="Enter Log Value"
                required
            ></b-form-input>
            </b-form-group>

            <b-form-group
            id="input-group-1"
            label="Enter Log Note:"
            label-for="input-1"
            description=""
            >
            <b-form-input
                id="input-1"
                type="text"
                v-model="form.note"
                placeholder="Enter Log Note"
                required
            ></b-form-input>
        </b-form-group>
  
        <b-button @click="AddLog()" variant="primary">Create Log</b-button>
    </b-form>


    <b-form v-if="visible_">
        <b-form-group
            id="input-group-1"
            label="Enter Log Note:"
            label-for="input-1"
            description=""
            >
            <b-form-input
                id="input-1"
                type="text"
                v-model="singleLogForm.value"
                placeholder="Enter Log Value"
                required
            ></b-form-input>
        </b-form-group>
        <b-form-group
            id="input-group-1"
            label="Enter Log Note:"
            label-for="input-1"
            description=""
            >
            <b-form-input
                id="input-1"
                type="text"
                v-model="singleLogForm.note"
                placeholder="Enter Log Note"
                required
            ></b-form-input>
        </b-form-group>
  
        <b-button @click="EditTrackerLog()" variant="primary">Edit Log</b-button>
    </b-form>
    <!-- <b-container v-if="visible_trend">

        <h1>data trends of this tracker</h1>
        <ul>
            <li v-for="d in  data" :key="d.data">{{ d.label }} : {{ d.data }}</li>
        </ul>
    </b-container> -->

    

    </b-container>
</template>

<script>
    import axios from 'axios';

    export default{
        data(){
            return{
                logs:'',
                data:[],
                labels:[],
                visible:'',
                visible_:'',
                visible_trend:'',
                form:{
                    timestamp:new Date().toLocaleDateString(),
                    value:'',
                    note:''
                },
                singleLogForm:{
                    id:'',
                    value:'',
                    note:''
                }
            }
        },
        created(){
            axios.get('http://127.0.0.1:5000/' + window.location.pathname + '/',
            { headers: {
            'Content-type': 'application/json',
            'Authorization':'Bearer ' + this.getCookie(),
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            }
          }).then((response)=>{
            if(response.status == 200){
                this.logs = response.data
                for(var i = 0; i<this.logs.length;i++){
                    const obj = {"data": this.logs[i].value,
                            "label":this.logs[i].note
                            }
                    this.data.push(
                        obj  
                    )
                }
            }else{
                this.logs = " "
            }
          })
        },methods:{
            getCookie(){
            return this.$cookies.get('token')
            },
            AddTodayLog(){
                this.visible = 'open'
            },
            AddLog(){
                axios.post('http://127.0.0.1:5000' + window.location.pathname + '/',
                    {
                        timestamp:this.form.timestamp,
                        value:this.form.value,
                        note:this.form.note
                    },
                    { headers: {
                        'Content-type': 'application/json',
                        'Authorization':'Bearer ' + this.getCookie(),
                        'Access-Control-Allow-Origin' : '*',
                        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                        }
                    }
                ).then(response=>{
                    console.log(response)
                    if(response.status == 200){
                        this.visible = ''
                        this.$router.go();
                    }
                })
            },
            DeleteLog(id){
                axios.delete('http://127.0.0.1:5000/log/'+ id + '/',
                    { headers: {
                        'Content-type': 'application/json',
                        'Authorization':'Bearer ' + this.getCookie(),
                        'Access-Control-Allow-Origin' : '*',
                        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                        }
                    }
                ).then((response)=>{
                    if(response.status == 200){
                        this.$router.go();
                    }
                })
            },
            EditLog(id){
                this.visible_ = 'edit';
                axios.get('http://127.0.0.1:5000/log/'+ id + '/',
                    { headers: {
                        'Content-type': 'application/json',
                        'Authorization':'Bearer ' + this.getCookie(),
                        'Access-Control-Allow-Origin' : '*',
                        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                        }
                    }
                ).then(response=>{
                    this.singleLogForm.id = response.data[0].id;
                    this.singleLogForm.value = response.data[0].value
                    this.singleLogForm.note = response.data[0].note
                })
            },
            ViewTrends(){
                this.visible_trend = "yes"
            },
            EditTrackerLog(){
                console.log(this.singleLogForm.id )
                axios.put('http://127.0.0.1:5000/log/'+ this.singleLogForm.id + '/',
                {
                    note:this.singleLogForm.note,
                    value:this.singleLogForm.value
                },{ headers: {
                        'Content-type': 'application/json',
                        'Authorization':'Bearer ' + this.getCookie(),
                        'Access-Control-Allow-Origin' : '*',
                        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                        }
                }).then((res)=>{
                    if(res.status == 200){
                        this.$router.go();
                    }
                })
            },
            exitApp(){
            this.$cookies.remove('token')
            this.$cookies.remove('username')
            this.$router.push('/')
            }
        }
    }

</script>