<template>
  <b-card no-body>
    <validation-observer v-slot="{ handleSubmit }" ref="formValidator">
      <b-form role="form" @submit.prevent="handleSubmit(onSubmit)">
          <b-card-header class="border-0">
            <h3 class="mb-0">Reconocimiento de Rostro</h3>
            <!--<div class="text-right">
                <b-button variant="warning" :to="{ name : 'cameras'}">Volver</b-button>
            </div>-->
          </b-card-header>
          <b-card-body>
            <div class="d-flex justify-content-center align-items-center" >
              <b-col cols="6">
                <label >Selecciona un usuario:</label>
                <b-form-select v-model="model.id_user" :options="options"  class="mb-3"></b-form-select>
              </b-col>
            </div>
            <br/>
            <div>
              <b-img ref="streamImage" center :src="url" fluid alt="Responsive image"></b-img>
            </div>
          </b-card-body>
          <b-card-footer>
            <div class="text-right">
              <!--<b-button variant="warning" :to="{ name: 'cameras' }" :disabled="disabled">Volver </b-button>-->
              <b-button variant="primary" type="submit" :disabled="disabled">Registrar</b-button>
            </div>
          </b-card-footer>
      </b-form>
    </validation-observer>
  </b-card>
</template>
<script>
export default {
  data() {
    return {
      model: {
        id_user: null,
      },
      url: "",
      disabled: false,
      options: [
        //{ value: null, text: 'Selecciona un usuario' },
        // { value: '1', text: 'This is First option' },
        // { value: 'b', text: 'Selected Option' },
        // { value: { C: '3PO' }, text: 'This is an option with object value' },
        // { value: 'd', text: 'This one is disabled', disabled: true }
      ]
    };
  },
  methods: {
    async onSubmit() {
      this.disabled = true;
      try {
          await this.axios.post(process.env.VUE_APP_API_URL + "stream/camera/save_recognition_person",this.model);
          this.$router.push({ name: 'pages.dashboard' });
          this.$dialog.notify.success('Se registró los datos correctamente');
      } catch (error) {
          this.$dialog.notify.error('Error al registrar el reconocimiento');
      }
      this.disabled = false;
    }
  },
  async created() {
    try {
      const response = await this.axios.get(process.env.VUE_APP_API_URL + 'users/users');
      this.options = response.data.map(user=>{
        return { value : user.id, text: user.name + " " + user.last_name };
      });
      this.url = process.env.VUE_APP_API_URL + "stream/camera/stream_recognition"
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
