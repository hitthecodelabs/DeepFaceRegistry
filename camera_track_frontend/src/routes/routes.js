import DashboardLayout from '@/views/Layout/DashboardLayout.vue';
import AuthLayout from '@/views/Pages/AuthLayout.vue';
import UsersPage from '../views/Pages/Users/Users.vue';
import CamerasPage from '../views/Pages/Cameras/Cameras.vue';
import ClipsPage from '../views/Pages/Clips/Clips.vue';
import RecognitionPage from '../views/Pages/Recognition/Recognition.vue'

import NotFound from '@/views/NotFoundPage.vue';

const routes = [
    {
        path: '/',
        component: AuthLayout,
        children: [
            {
                path: '',
                name: 'login',
                component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Login.vue')
            },
            {
                path: '/register',
                name: 'register',
                component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Register.vue')
            },
        ]
    },
    {
        path: '/pages',
        redirect: 'pages.dashboard',
        component: DashboardLayout,
        children: [
            {
                path: '/dashboard',
                name: 'pages.dashboard',
                component: () => import(/* webpackChunkName: "demo" */ '../views/Dashboard.vue')
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
                        props: true,
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
                        props: true,
                        component: () => import(/* webpackChunkName: "demo" */ '../views/Forms/Cameras/CameraFormEdit.vue')
                    },
                    {
                        path: 'live/:id',
                        name: 'cameras.live',
                        props: true,
                        component: () => import(/* webpackChunkName: "demo" */ '../views/Cards/CarmeraLiveCard.vue')
                    },
                    {
                        path: 'list/lives',
                        name: 'cameras.list.lives',
                        props: true,
                        component: () => import(/* webpackChunkName: "demo" */ '../views/Tables/Cameras/CamerasLiveTable.vue')
                    },
                ]
            },
            {
              path: '/clips',
              name: 'clips',
              redirect: '/clips/list',
              component: ClipsPage,
              children: [
                  {
                      path: 'list',
                      name: 'clips.list',
                      component: () => import(/* webpackChunkName: "demo" */ '../views/Tables/Clips/ClipsTable.vue')
                  }
              ]
            },
            {
              path: '/recognition',
              name: 'recognition',
              component: RecognitionPage,
              redirect: '/recognition/face-person',
              children: [
                {
                    path: 'face-person',
                    name: 'recognition.facePerson',
                    component: () => import(/* webpackChunkName: "demo" */ '../views/Cards/CameraRecognition.vue')
                }
              ]
            },
        ],
    },
    { path: '*', component: NotFound }
];

export default routes;
