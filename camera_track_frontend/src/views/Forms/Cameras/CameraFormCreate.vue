<template>
  <b-card no-body>
    <b-card-header class="border-0">
        <h3 class="mb-0">Crear Cámara</h3>
    </b-card-header>
    <b-card-body>
      <validation-observer v-slot="{ handleSubmit }" ref="formValidator">
        <b-form role="form" @submit.prevent="handleSubmit(onSubmit)">
          <div class="pl-lg-4">
            <b-row>
              <b-col lg="4">
                <base-input name="Name" type="text" label="Name" placeholder="Nombre" v-model="model.name"
                  :rules="{ required: true }">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="Ip" type="text" label="Ip" placeholder="IP" v-model="model.ip"
                  :rules="{ required: true, regex: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/ }">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="Port" type="text" label="Port" v-model="model.port"
                  :rules="{ required: true, numeric: true }">
                </base-input>
              </b-col>
            </b-row>
            <b-row>
              <b-col lg="4">
                <base-input name="CamUsername" type="text" label="Cam Username"
                    placeholder="Usuario de Cámara" v-model="model.cam_username">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="CamPassword" type="text" label="Cam Password"
                    placeholder="Contraseña de Cámara" v-model="model.cam_password">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="File" type="text" label="File" v-model="model.file">
                </base-input>
              </b-col>
            </b-row>
          </div>
          <div class="text-right">
            <b-button variant="warning" :to="{ name: 'cameras' }" :disabled="disabled">Volver </b-button>
            <b-button variant="primary" type="submit" :disabled="disabled">Registrar</b-button>
          </div>
        </b-form>
      </validation-observer>
    </b-card-body>
  </b-card>
</template>
<script>
export default {
  data() {
    return {
      model: {
        ip: '',
        name: '',
        port: 0,
        cam_username: '',
        cam_password: '',
        file: ''
      },
      disabled: false
    };
  },
  methods: {
    async onSubmit() {
      this.disabled = true;
      try {
          await this.axios.post(process.env.VUE_APP_API_URL + "cameras/cameras/", this.model);
          this.$router.push({ name: 'cameras' });
          this.$dialog.notify.success('Se registró los datos de cámara correctamente');
      } catch (error) {
          this.$dialog.notify.error('Error al registrar cámara');
      }
      this.disabled = false;
    }
  },
};
</script>
