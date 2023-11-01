<template>
  <b-card no-body>
    <b-card-header class="border-0">
        <h3 class="mb-0">Crear Usuario</h3>
    </b-card-header>
    <b-card-body>
      <validation-observer v-slot="{ handleSubmit }" ref="formValidator">
        <b-form role="form" @submit.prevent="handleSubmit(onSubmit)">
          <div class="pl-lg-4">
            <b-row>
              <b-col lg="4">
                <base-input name="UserName" type="text" label="Nombre de usuario" placeholder="xyz"
                    v-model="model.username" :rules="{ required: true }">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="Email" type="email" label="Correo Electrónico"
                    placeholder="example@email.com" v-model="model.email"
                    :rules="{ required: true, email: true }">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="Password" type="password" label="Contraseña" placeholder="Password"
                    v-model="model.password" :rules="{ required: true, min: 6 }">
                </base-input>
              </b-col>
            </b-row>
            <b-row>
              <b-col lg="4">
                <base-input name="Name" type="text" label="Nombres" v-model="model.name"
                    :rules="{ required: true , regex: /^[A-Za-z]+$/}">
                </base-input>
              </b-col>
              <b-col lg="4">
                <base-input name="LastName" type="text" label="Apellidos" v-model="model.last_name"
                    :rules="{ required: true, regex: /^[A-Za-z]+$/ }">
                </base-input>
              </b-col>
              <b-col lg="4" class="align-self-center" v-if="user.is_superuser">
                <base-checkbox  v-model="model.is_staff">
                    Es administrador
                </base-checkbox>
              </b-col>
            </b-row>
            <b-row lg="12">
              <base-input name="image" type="file" label="Imagen" v-model="user.image" @change="handleFileUpload( $event )"
                  :rules="{ required: true }">
              </base-input>
            </b-row>
          </div>
          <div class="text-right">
            <b-button variant="warning" :to="{ name : 'users'}"  :disabled="disabled">Volver</b-button>
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
        username: '',
        email: '',
        name: '',
        last_name: '',
        password: '',
        is_staff: false,
        image: null
      },
      disabled:false,
      user:null
    };
  },
  created(){
    this.user = JSON.parse(localStorage.getItem('usuario'));
  },
  methods: {
    async onSubmit() {
      this.disabled = true;
      let formData = new FormData();
      formData.append('username', this.model.username);
      formData.append('email', this.model.email);
      formData.append('name', this.model.name);
      formData.append('last_name', this.model.last_name);
      formData.append('password', this.model.password);
      formData.append('is_staff', this.model.is_staff);
      formData.append('image', this.model.image);

      try {
        await this.axios.post(process.env.VUE_APP_API_URL + "users/users/", formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        });
        this.$router.push({ name: 'users' });
        this.$dialog.notify.success('Se registró el usuario correctamente');
      } catch (error) {
        this.$dialog.notify.error('Error al registrar usuario');
      }
      this.disabled = false;
    },
    handleFileUpload( event ){
      this.model.image = event.target.files[0];
    },
  },

};
</script>
