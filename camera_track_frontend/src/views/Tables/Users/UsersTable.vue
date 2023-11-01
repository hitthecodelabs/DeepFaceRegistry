<template>
  <b-card no-body>
    <b-card-header class="border-0">
        <h3 class="mb-0">Usuarios</h3>
    </b-card-header>
    <b-card-body>
      <b-button :to="{ name: 'users.create' }" variant="info">Crear</b-button>
      <b-row class="justify-content-end">
        <b-col lg="4" class="my-1">
          <b-input-group size="sm">
            <b-input v-model="filter" placeholder="Buscar..."></b-input>
          </b-input-group>
        </b-col>
      </b-row>
      <b-table id="table-users" :items="users" :per-page="perPage" :current-page="currentPage" :fields="fields" @filtered="onFiltered"
          :filter="filter" show-empty striped hover small>
        <template #cell(actions)="data">
          <b-button :to="{ name: 'users.edit', params: { id: data.item.id } }" variant="info">
              <b-icon icon="pencil-square" aria-hidden="true"></b-icon>
          </b-button>
          <b-button variant="danger" @click="deleteUser(data.item)">
              <b-icon icon="trash-fill" aria-hidden="true"></b-icon>
          </b-button>
        </template>
      </b-table>
      <b-card-footer class="py-4 d-flex justify-content-end">
        <b-pagination v-model="currentPage" :total-rows="total" :per-page="perPage"
            aria-controls="table-users"></b-pagination>
      </b-card-footer>
    </b-card-body>
  </b-card>
</template>
<script>
import { Table, TableColumn } from 'element-ui'
export default {
  name: 'users-table',
  components: {
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  data() {
    return {
      users: [],
      currentPage: 1,
      perPage: 10,
      total: 0,
      filter: '',
      fields: [
        {
          key: 'id',
          label: 'Id',
        },
        {
          key: 'username',
          label: 'Usuario',
        },
        {
          key: 'email',
          label: 'Correo',
        },
        {
          key: 'actions',
          label: 'Acciones',
        }
      ],
    };
  },
  created() {
      this.getUsers();
  },
  methods: {
    async getUsers() {
      try {
        const response = await this.axios.get(process.env.VUE_APP_API_URL + 'users/users');
        this.users = response.data;
        this.total = response.data.length;
      } catch (error) {
        this.$dialog.notify.error('Error al obtener los datos de usuarios');
      }
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.total = filteredItems.length
      this.currentPage = 1
    },
    async deleteUser(user) {
      const res = await this.$dialog.warning({
        text: '¿Esta seguro de eliminar el usuario: ' + user.name + ' ' + user.last_name + '?',
        title: 'Confirmación',
        actions: {
            'false': 'No',
            'true': 'Sí'
        }
      });
      if (res) {
        try {
          await this.axios.delete(process.env.VUE_APP_API_URL + 'users/users/' + user.id + '/');
          this.$dialog.notify.info('Se eliminó correctamente');
          this.getUsers();
        } catch (error) {
          this.$dialog.notify.error('Error al eliminar');
        }
      }
    }
  }
}
</script>
