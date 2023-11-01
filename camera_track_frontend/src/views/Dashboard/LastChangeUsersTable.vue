<template>

  <b-card body-class="p-0" header-class="border-0">
    <template v-slot:header>
      <b-row align-v="center">
        <b-col>
          <h3 class="mb-0">Ultimas Actualizaciones en los Usuarios</h3>
        </b-col>
        <!--<b-col class="text-right">
          <a href="#!" class="btn btn-sm btn-primary">See all</a>
        </b-col>-->
      </b-row>
      <b-row class="justify-content-end">
        <b-col lg="1" class="my-1">
          <b-button variant="warning" @click="resetData()">
            <i class="fas fa-sync"></i>
          </b-button>
        </b-col>
        <b-col lg="5" class="my-1">
          <b-input-group size="sm">
            <label class="my-1"> Desde: </label>
            <b-input v-model="startDate" type="date" class="my-1"></b-input>
            <label class="my-1"> Hasta: </label>
            <b-input v-model="endDate" type="date" class="my-1"></b-input>
          </b-input-group>
        </b-col>
        <b-col lg="4" class="my-1">
          <b-input-group size="sm">
            <b-input v-model="filter" placeholder="Buscar..."></b-input>
          </b-input-group>
        </b-col>
      </b-row>
    </template>

    <b-table :items="filteredData" :fields="fields" :per-page="perPage" :current-page="currentPage" @filtered="onFiltered"
          :filter="filter" show-empty striped hover small>
        <template #cell(user_responsible)="data">
          {{ data.item.user_responsible_name }}  {{ data.item.user_responsible_last_name }}
        </template>
        <template #cell(action)="data">
            {{ getAcctionUser(data.item.action,data.item.user_affected_name,data.item.user_affected_last_name) }}
        </template>
      </b-table>
      <b-card-footer class="py-4 d-flex justify-content-end">
        <b-pagination v-model="currentPage" :total-rows="total" :per-page="perPage"
            aria-controls="table-users"></b-pagination>
      </b-card-footer>
  </b-card>
</template>
<script>
  import { Table, TableColumn} from 'element-ui'
  export default {
    name: 'last-change-users-table',
    components: {
      [Table.name]: Table,
      [TableColumn.name]: TableColumn,
    },
    // props:{
    //   data : Array
    // },
    data() {
      return {
        data :[],
        currentPage: 1,
        perPage: 10,
        total: 0,
        filter: '',
        startDate : null,
        endDate : null,
        fields: [
          {
            label: 'USUARIO RESPONSABLE',
            key: 'user_responsible'
          },
          {
            label: 'ACCIÓN',
            key: 'action'
          },
          {
            label: 'FECHA DE ACCIÓN',
            key: 'date'
          }
        ],
      }
    },
    computed: {
      filteredData() {
        if (!this.startDate || !this.endDate) {
          return this.data;
        }
        const start = new Date(this.startDate);
        const end = new Date(this.endDate);
        return this.data.filter(row => {
          const dateString = row.date;
          const [datePart, timePart] = dateString.split(" ");
          const [day, month, year] = datePart.split("-");
          const [hours, minutes, seconds] = timePart.split(":");

          // El mes en JavaScript comienza desde 0, por lo que debes restar 1 al mes
          const rowDate = new Date(year, month - 1, day, hours, minutes, seconds);
          //const rowDate = new Date(row.date);
          return rowDate >= start && rowDate <= end;
        });
      }
    },
    watch: {
      // whenever question changes, this function will run
      endDate: function () {
        this.currentPage = 1;
        this.total = this.filteredData.length;
      }
    },
    created(){
      this.getLastChangeUsers()
    },
    methods:{
      getAcctionUser(action, user_affected_name, user_affected_last_name)
      {
        const ACCTIONS_SPANISH = {
          Created : 'Creó',
          Updated : 'Actualizó',
          Deleted : 'Eliminó',
        }
        return ACCTIONS_SPANISH[action] + " al usuario " + user_affected_name + " " + user_affected_last_name;
      },
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.total = filteredItems.length
        this.currentPage = 1
      },
      async getLastChangeUsers(){
        try {
          const response = await this.axios.get(process.env.VUE_APP_API_URL + "totals/historical_users/");
          this.data = response.data;
          this.total = response.data.length;
        } catch (error) {

        }
      },
      resetData(){
        this.startDate = null;
        this.endDate = null;
        this.filter='';
        this.getLastChangeUsers();
      }
    }
  }
</script>
