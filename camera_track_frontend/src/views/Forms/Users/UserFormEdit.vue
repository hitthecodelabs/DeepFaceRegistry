<template>
  <b-card no-body>
    <b-card-header class="border-0">
      <h3 class="mb-0">Editar Usuario</h3>
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
                <base-input name="Name" type="text" label="Nombre" v-model="model.name"
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
          </div>
          <div class="text-right">
            <b-button variant="warning" :to="{ name : 'users'}" :disabled="disabled">Volver</b-button>
            <b-button variant="primary" type="submit" :disabled="disabled">Guardar</b-button>
          </div>
        </b-form>
      </validation-observer>
    </b-card-body>
  </b-card>
</template>
<script>
export default {
  props: ['id'],
  data() {
    return {
      model: {
        username: '',
        email: '',
        name: '',
        last_name: '',
        password: '',
        is_staff: false,
      },
      disabled:false,
      user:null
    };
  },
  methods: {
    async onSubmit() {
      this.disabled = true;
      try {
        await this.axios.put(process.env.VUE_APP_API_URL + "users/users/" + this.id + "/", this.model);
        this.$router.push({ name: 'users' });
        this.$dialog.notify.success('Se actualizó el usuario correctamente');
      } catch (error) {
        this.$dialog.notify.error('Error al actualizar usuario');
      }
      this.disabled = false;
    }
  },
  async created() {
    try {
      const response = await this.axios.get(process.env.VUE_APP_API_URL + "users/users/" + this.id);
      const user = response.data;
      this.model.username = user.username;
      this.model.email = user.email;
      this.model.name = user.name;
      this.model.last_name = user.last_name;
      this.model.is_staff = user.is_staff;
      this.user = JSON.parse(localStorage.getItem('usuario'));
    } catch (error) {
      this.$dialog.notify.error('Error al obtener usuario');
    }
  }
};
</script>
