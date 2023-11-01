<template>
  <div class="wrapper">
    <notifications></notifications>
    <side-bar>
      <template slot="links">

        <sidebar-item :link="{
          name: 'Dashboard',
          path: '/dashboard',
          icon: 'ni ni-tv-2 text-primary',
        }">

        </sidebar-item>
        <sidebar-item v-if="user.is_staff" :link="{
          name: 'Usuarios',
          path: '/users',
          icon: 'ni ni-single-02 text-yellow'
        }">
        </sidebar-item>

        <sidebar-item v-if="user.is_staff" :link="{
          name: 'Cámaras',
          path: '/cameras',
          icon: 'ni ni-camera-compact text-red'
        }">
        </sidebar-item>

        <sidebar-item v-if="user.is_staff" :link="{
          name: 'Reconocimiento',
          path: '/recognition',
          icon: 'ni ni-camera-compact text-green'
        }">
        </sidebar-item>

        <sidebar-item :link="{
          name: 'Monitoreo',
          path: '/cameras/list/lives',
          icon: 'ni ni-tablet-button text-primary'
        }">
        </sidebar-item>

        <sidebar-item v-if="user.is_staff" :link="{
          name: 'Grabaciones',
          path: '/clips',
          icon: 'ni ni-archive-2 text-primary'
        }">
        </sidebar-item>

      </template>

    </side-bar>
    <div class="main-content">
      <dashboard-navbar  :type="$route.meta.navbarType"></dashboard-navbar>

      <div @click="$sidebar.displaySidebar(false)">
        <fade-transition :duration="200" origin="center top" mode="out-in">
          <!-- your content here -->
          <router-view></router-view>
        </fade-transition>
      </div>
      <!--
      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
      -->
    </div>
  </div>
</template>
<script>
/* eslint-disable no-new */
import PerfectScrollbar from 'perfect-scrollbar';
import 'perfect-scrollbar/css/perfect-scrollbar.css';

function hasElement(className) {
  return document.getElementsByClassName(className).length > 0;
}

function initScrollbar(className) {
  if (hasElement(className)) {
    new PerfectScrollbar(`.${className}`);
  } else {
    // try to init it later in case this component is loaded async
    setTimeout(() => {
      initScrollbar(className);
    }, 100);
  }
}

import DashboardNavbar from './DashboardNavbar.vue';
import ContentFooter from './ContentFooter.vue';
import DashboardContent from './Content.vue';
import { FadeTransition } from 'vue2-transitions';

export default {
  components: {
    DashboardNavbar,
    ContentFooter,
    DashboardContent,
    FadeTransition
  },
  data(){
    return{
      user : null
    };
  },
  methods: {
    initScrollbar() {
      let isWindows = navigator.platform.startsWith('Win');
      if (isWindows) {
        initScrollbar('sidenav');
      }
    }
  },
  mounted() {
    this.initScrollbar();
  },
  created(){
    this.user = JSON.parse(localStorage.getItem('usuario'));
  }
};
</script>
<style lang="scss"></style>
