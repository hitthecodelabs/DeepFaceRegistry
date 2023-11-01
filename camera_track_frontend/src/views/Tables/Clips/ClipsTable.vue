<template>
  <b-card no-body>
    <b-card-header class="border-0">
        <h3 class="mb-0">Grabaciones</h3>
    </b-card-header>
    <b-card-body>
      <b-row class="justify-content-end">
        <b-col lg="1" class="my-1">
          <!--<i class="ni ni-cloud-download-95"></i> <span></span>-->
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
      <b-table id="table-clips" :items="filteredClips" :per-page="perPage" :current-page="currentPage" :fields="fields"
          :filter="filter" show-empty striped hover small>
        <template #cell(actions)="data">
          <!--<b-button :to="{ name: 'clips.live', params: { id: data.item.id } }" variant="warning">
              <b-icon icon="tv-fill" aria-hidden="true"></b-icon>
          </b-button>-->
          <b-button variant="primary" @click="getDownloadClip(data.item.file)">
              <i class="ni ni-cloud-download-95"></i> <span></span>
          </b-button>
        </template>
      </b-table>
      <b-card-footer class="py-4 d-flex justify-content-end">
        <b-pagination v-model="currentPage" :total-rows="total" :per-page="perPage"
            aria-controls="table-clips"></b-pagination>
      </b-card-footer>
    </b-card-body>
  </b-card>
</template>
<script>
import { Table, TableColumn } from 'element-ui'
export default {
  name: 'clips-table',
  components: {
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  data() {
    return {
      clips: [],
      currentPage: 1,
      perPage: 10,
      total: 0,
      filter: '',
      startDate : null,
      endDate : null,
      fields: [
        {
          key: 'id',
          label: 'Id',
        },
        {
          key: 'name',
          label: 'Nombre',
        },
        {
          key: 'camera_name',
          label: 'Cámara',
        },
        {
          key: 'created_date',
          label: 'Fecha de creación',
        },
        {
          key: 'actions',
          label: 'Acciones',
        }
      ],
    };
  },
  computed: {
    filteredClips() {
      if (!this.startDate || !this.endDate) {
        return this.clips;
      }
      const start = new Date(this.startDate);
      const end = new Date(this.endDate);
      return this.clips.filter(row => {
        const rowDate = new Date(row.created_date);
        return rowDate >= start && rowDate <= end;
      });
    }
  },
  watch: {
    // whenever question changes, this function will run
    endDate: function () {
      this.currentPage = 1;
      this.total = this.filteredClips.length;
    }
  },
  created() {
    this.getclips();
  },
  methods: {
    async getclips() {
      try {
        const response = await this.axios.get(process.env.VUE_APP_API_URL + 'clips/clips')
        this.clips = response.data;
        this.total = response.data.length;
      } catch (error) {
        this.$dialog.notify.error('Error al obtener los datos de grabaciones');
      }
    },
    getDownloadClip(url){
      window.open(url, '_blank');
    },
    resetData(){
      this.startDate = null;
      this.endDate = null;
      this.filter='';
      this.getclips();
    }
  }
}
</script>
