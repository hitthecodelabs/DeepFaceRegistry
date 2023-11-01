import DashboardLayout from '@/views/Layout/DashboardLayout.vue';
import AuthLayout from '@/views/Pages/AuthLayout.vue';
import UsersPage from '../views/Pages/Users/Users.vue';
import CamerasPage from '../views/Pages/Cameras/Cameras.vue';

import NotFound from '@/views/NotFoundPage.vue';

const routes = [
  {
    path: '/',
    redirect: 'dashboard',
    component: DashboardLayout,
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "demo" */ '../views/Dashboard.vue')
      },
      {
        path: '/icons',
        name: 'icons',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Icons.vue')
      },
      {
        path: '/profile',
        name: 'profile',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/UserProfile.vue')
      },
      {
        path: '/maps',
        name: 'maps',
        component: () => import(/* webpackChunkName: "demo" */ '../views/GoogleMaps.vue')
      },
      {
        path: '/tables',
        name: 'tables',
        component: () => import(/* webpackChunkName: "demo" */ '../views/RegularTables.vue')
      },
      {
        path: '/users',
        name: 'users',
        redirect: '/users/list',
        component: UsersPage,
        children: [
          {
            path: 'list',
            name: 'users.list',
            component: () => import(/* webpackChunkName: "demo" */ '../views/Tables/Users/UsersTable.vue')
          },
          {
            path: 'create',
            name: 'users.create',
            component: () => import(/* webpackChunkName: "demo" */ '../views/Forms/Users/UserFormCreate.vue')
          },
          {
            path: 'edit/:id',
            name: 'users.edit',
            props: true ,
            component: () => import(/* webpackChunkName: "demo" */ '../views/Forms/Users/UserFormEdit.vue')
          },
        ]
      },
      {
        path: '/cameras',
        name: 'cameras',
        redirect: '/cameras/list',
        component: CamerasPage,

        children: [
          {
            path: 'list',
            name: 'cameras.list',
            component: () => import(/* webpackChunkName: "demo" */ '../views/Tables/Cameras/CamerasTable.vue')
          },
          {
            path: 'create',
            name: 'cameras.create',
            component: () => import(/* webpackChunkName: "demo" */ '../views/Forms/Cameras/CameraFormCreate.vue')
          },
          {
            path: 'edit/:id',
            name: 'cameras.edit',
            props: true ,
            component: () => import(/* webpackChunkName: "demo" */ '../views/Forms/Cameras/CameraFormEdit.vue')
          },
        ]
      }
    ]
  },
  {
    path: '/',
    redirect: 'login',
    component: AuthLayout,
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Login.vue')
      },
      {
        path: '/register',
        name: 'register',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Register.vue')
      },
      { path: '*', component: NotFound }
    ]
  }
];

export default routes;
