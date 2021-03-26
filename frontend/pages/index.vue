<template>
  <div>
    <div>
    <div class="bs-example">
    <nav class="navbar navbar-expand-md navbar-dark">
        <div class="navbar-nav">
            <h1>Error Management Board</h1>
          </div>
        <div class="navbar-nav ml-auto">
                <a class="nav-item nav-link">Operator Name: {{operator}}</a>
        </div>
    </nav>
    </div>
   </div>
   <div>
     <div>
     <button class="btn btn-outline-primary float-right" style="width:150px;margin-top:20px;margin-right:10px" v-on:click="undoaction">Undo</button>
     <button class="btn btn-outline-primary float-right" style="width:150px;margin-top:20px;margin-right:10px" v-on:click="undoactionall">Undo All</button>
      <button class="btn btn-outline-primary float-right" style="width:150px;margin-top:20px;margin-right:10px" v-on:click="fetchSomething">Send Resolved</button>
     </div>
   </div>
    <div class="container-fluid pt-3">
    <div class="row flex-row flex-sm-nowrap py-3">
        <div class="col-md-6 col-lg-4 col-xl-3" style="max-width: 60rem;margin-left:30px;margin-top:43px">
            <div class="card bg-light" style="width: 27rem">
                <div class="card-body">
                    <h6 class="card-title">
                         <p class = "font-weight-bold">RESOLVED: {{resolved.length}}</p>
                    </h6>
                    <div v-for="error in resolved" :key="error.index">
                        <div class="items border border-light">
                        <div class="card draggable shadow-sm" style="margin-top:10px">
                            <div class="card-body p-2">
                                <div class="card-title">
                                    <p class="lead font-weight-light">{{ error.code }}</p>
                                </div>
                                <p>
                                    {{ error.text }}
                                </p><br>
                                <button class="btn btn-primary btn-sm float-right" style="margin-right:20px" v-on:click="pushpop(error.index,resolved,'`resolved`','`unresolved`')">Unresolve</button>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 col-xl-3" style="max-width: 60rem;margin-left:30px;margin-top:43px">
            <div class="card bg-light" style="width: 27rem">
                <div class="card-body">
                    <h6 class="card-title">
                      <p class = "font-weight-bold">UNRESOLVED: {{unresolved.length}}</p>
                    </h6>
                    <div v-for="error in unresolved" :key="error.index">
                        <div class="items border border-light">
                        <div class="card draggable shadow-sm" style="margin-top:10px">
                            <div class="card-body p-2">
                                <div class="card-title">
                                    <p class="lead font-weight-light">{{ error.code }}</p>
                                </div>
                                <p>
                                    {{ error.text }}
                                </p><br>
                                <button class="btn btn-primary btn-sm float-right" style="margin-right:20px" v-on:click="pushpop(error.index,unresolved,'`unresolved`','`resolved`')">Resolve</button>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 col-xl-3" style="max-width: 60rem;margin-left:30px;margin-top:43px">
            <div class="card bg-light" style="width: 27rem">
                <div class="card-body">
                    <h6 class="card-title">
                      <p class = "font-weight-bold">BACKLOG: {{backlog.length}}</p>
                    </h6>
                    <div v-for="error in backlog" :key="error.index">
                        <div class="items border border-light">
                        <div class="card draggable shadow-sm" style="margin-top:10px">
                            <div class="card-body p-2">
                                <div class="card-title">
                                    <p class="lead font-weight-light">{{ error.code }}</p>
                                </div>
                                <p>
                                    {{ error.text }}
                                </p><br>
                                <button class="btn btn-primary btn-sm float-right"  style="margin-right:20px" v-on:click="pushpop(error.index,backlog,'`backlog`','`unresolved`')">Unresolve</button>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
  </div>
  </div>
  </div>
</template>

<script>
import cloneDeep from 'lodash';

export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists?operator_name=chandeesh"
      );
      return {
        resolved,
        unresolved,
        backlog
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: [],
      undo: [],
      undoAll: [],
      resolvedcount: [],
      operator: "Chandeesh",
      undoResolved: [],
      undoUnresolved: [],
      undoBacklog: []
    };
  },

  created() {
    //intialize resolved count list which stores the count of the error code that is resolved
    for (let i in this.resolved) {
      this.resolvedcount[i] = {
        index : this.resolved[i].index,
        code : this.resolved[i].code,
        count : 0,
      }
    }
    this.undoResolved =  JSON.parse(JSON.stringify(this.resolved));
    this.undoUnresolved = JSON.parse(JSON.stringify(this.unresolved));
    this.undoBacklog = JSON.parse(JSON.stringify(this.backlog));
  },

  methods: {
  // call to API to send the list containing resolved count
   async fetchSomething() {
     await this.$axios.post('http://localhost:8000/resolvedcount', { resolvedCount : this.resolvedcount})
    .then(function (response) {
  })
  .catch(function (error) {
    console.log(error);
  });
  this.$toasted.global.my_success("Check Logs")
    },

 // function to push and pop the list according to the user action

    pushpop: function (inde, list, str1, str2) {
      for (let i in list) {
        if (list[i].index == inde) {
          this.undo[0] = {
            ori: i,
            index: list[i].index,
            code: list[i].code,
            text: list[i].text,
          }
          if (list[i].index == inde && !this.undoAll.some(e => e.index === inde)) {
            console.log(i)
            this.undoAll.push({
            ori: i,
            index: list[i].index,
            code: list[i].code,
            text: list[i].text,
          });
          }
          list[i].text = list[i].text.replace(str1, str2);
          if (str2 == "`resolved`") {
            this.resolved.push(list[i]);
            this.updatecount(inde,list[i].code);
            list.splice(i, 1);
            this.$toasted.global.my_success(str2);
          } else if (str2 == "`unresolved`") {
            this.unresolved.push(list[i]);
            console.log(this.undoResolved)
            list.splice(i, 1);
            this.$toasted.global.my_success(str2);
          } else {
            this.backlog.push(list[i]);
            list.splice(i, 1);
           this.$toasted.global.my_success(str2);
          }
        }
      }
    },

  //function to undo the last action and place it at the index at start

    undoaction: function () {
      if(this.undo.length!=0) {
        console.log(this.undo)
      if (this.undo[0].text.includes("`unresolved`")) {
        for (let i in this.resolved) {
          if (this.undo[0].index == this.resolved[i].index) {
            this.resolved[i].text = this.resolved[i].text.replace(
              "`resolved`",
              "`unresolved`"
            );
            this.unresolved.splice(
              this.undo[0].ori,
              0,
              this.resolved[i]
            );
            this.resolved.splice(i, 1);
            this.undo = [];
          }
        }
      } else if (this.undo[0].text.includes("`resolved`")) {
        for (let i in this.unresolved) {
          if (this.undo[0].index == this.unresolved[i].index) {
            this.unresolved[i].text = this.unresolved[i].text.replace(
              "`unresolved`",
              "`resolved`"
            );
            this.resolved.splice(
              this.undo[0].ori,
              0,
              this.unresolved[i]
            );
            this.unresolved.splice(i, 1);
            this.undo = [];
          }
        }
      } else {
        for (let i in this.unresolved) {
          if (this.undo[0].index == this.unresolved[i].index) {
            this.unresolved[i].text = this.unresolved[i].text.replace(
              "`unresolved`",
              "`backlog`"
            );
            this.backlog.splice(
              this.undo[0].ori,
              0,
              this.unresolved[i]
            );
            this.unresolved.splice(i, 1);
            this.undo = [];
          }
        }
      }
      }else {
        this.$toasted.global.my_success("Failed")
      }
    },

  //function which counts the error code that is resolved and is stored in a list

    updatecount: function(ind,cod) {
      for (let i in this.resolvedcount) {
        if(this.resolvedcount[i].index==ind) {
          this.resolvedcount[i].count =  this.resolvedcount[i].count+1;
        }
      }
      if(!this.resolvedcount.some(e=>e.index===ind)) {
          this.resolvedcount.push({index:ind,code:cod,count:1})
      }
    },

  // function which undoes all the user actions

    undoactionall: function () {
      this.resolved =JSON.parse(JSON.stringify(this.undoResolved));
      this.unresolved = JSON.parse(JSON.stringify(this.undoUnresolved));
      this.backlog = JSON.parse(JSON.stringify(this.undoBacklog));
    },
  },
};
</script>

<style scoped>
.navbar-nav h1 {
    color: white;
}
.navbar-nav ml-auto a {
    color: white;
}
.navbar {
  background-color: #563d7c;
}

.btn-outline-primary {
      border-color: #563d7c !important;
      color:#563d7c
}

.btn-primary {
   border-color: #563d7c !important;
   background-color:#563d7c !important;
   color: white;
}
.btn-outline-primary:hover {
    background-color: #563d7c !important;
    color: white;
}

.card-body .p-2{
    border-radius: 4px;
    background: #fff;
    box-shadow: 0 6px 10px rgba(0,0,0,.08), 0 0 6px rgba(0,0,0,.05);
      transition: .3s transform cubic-bezier(.155,1.105,.295,1.12),.3s box-shadow,.3s -webkit-transform cubic-bezier(.155,1.105,.295,1.12);
  padding: 14px 80px 18px 36px;
  cursor: pointer;
}

.card-body .p-2:hover{
     transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06);
}
</style>