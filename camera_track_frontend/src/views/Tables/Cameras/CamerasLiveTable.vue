<template>
  <b-card no-body>
    <b-card-header class="border-0">
      <h3 class="mb-0">Monitoreo de Cámaras</h3>
    </b-card-header>
    <b-card-body>
      <b-card-group deck>
        <b-card
          header-tag="header"
          footer-tag="footer"
          v-for="camera in getCamerasPaginate"
          :key="camera.id"
          id="cameras-cards-lives"
        >
          <template #header>
            <h6 class="mb-0">{{ camera.name }}</h6>
          </template>
          <b-img
            ref="streamImage"
            center
            :src="getUrlStream(camera)"
            fluid
          ></b-img>
        </b-card>
      </b-card-group>
      <b-card-footer
        v-if="cameras.length > 0"
        class="py-4 d-flex justify-content-end"
      >
        <b-pagination
          v-model="currentPage"
          :total-rows="total"
          :per-page="perPage"
          aria-controls="cameras-cards-lives"
        ></b-pagination>
      </b-card-footer>
    </b-card-body>
  </b-card>
</template>
<script>
import { Table, TableColumn } from "element-ui";
export default {
  name: "cameras-live-table",
  components: {
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
  },
  data() {
    return {
      cameras: [],
      currentPage: 1,
      perPage: 3,
      total: 0,
      filter: "",
      fields: [
        {
          key: "id",
          label: "Id",
        },
        {
          key: "name",
          label: "Nombre",
        },
        {
          key: "ip",
          label: "Ip",
        },
        {
          key: "port",
          label: "Puerto",
        },
      ],
    };
  },
  created() {
    this.getCameras();
  },
  methods: {
    async getCameras() {
      try {
        const response = await this.axios.get(
          process.env.VUE_APP_API_URL + "cameras/cameras"
        );
        this.cameras = response.data;
        this.total = response.data.length;
      } catch (error) {
        this.$dialog.notify.error("Error al obtener los datos de cámaras");
      }
    },
    getUrlStream(camera) {
      return (
        process.env.VUE_APP_API_URL + "stream/camera/" + camera.id + "/live"
      );
    },
    clearStreamImage() {
      if (this.$refs.streamImage) {
        this.$refs.streamImage.forEach((img) => {
          img.src = "";
        });
      }
    },
  },
  computed: {
    getCamerasPaginate() {
      return this.cameras.slice(
        (this.currentPage - 1) * this.perPage,
        (this.currentPage - 1) * this.perPage + this.perPage
      );
    },
  },
  watch: {
    currentPage() {
      this.clearStreamImage();
    },
  },
  beforeRouteLeave(to, from, next) {
    this.clearStreamImage();
    next();
  },
};
</script>
