<template>
  <b-card no-body>
    <b-card-header class="border-0">
      <h3 class="mb-0">Directo : Cámara - {{ model.name }} - {{ model.ip }}</h3>
      <div class="text-right">
          <b-button variant="warning" :to="{ name : 'cameras'}">Volver</b-button>
      </div>
    </b-card-header>
    <b-card-body>
      <div>
        <b-img ref="streamImage" center :src="url" fluid alt="Responsive image"></b-img>
      </div>
    </b-card-body>
  </b-card>
</template>
<script>
export default {
  props: ['id'],
  data() {
    return {
      model: {
          ip: '',
          name: '',
          port: 0
      },
      // url: process.env.VUE_APP_API_URL + "stream/camera/1/live"
      url: ""
    };
  },
  methods: {},
  async created() {
    try {
      const response = await this.axios.get(process.env.VUE_APP_API_URL + "cameras/cameras/" + this.id);
      const camera = response.data;
      this.model.ip = camera.ip;
      this.model.name = camera.name;
      this.model.port = camera.port;
      this.url = process.env.VUE_APP_API_URL + "stream/camera/"+this.id+"/live"
    } catch (error) {
      this.$dialog.notify.error('Error al obtener datos de cámara');
    }
  },
  beforeRouteLeave(to, from, next) {
    // cancelar la descarga de la imagen
    this.$refs.streamImage.src = '';
    next();
  },
};
</script>
