//router.js
import Vue from 'vue';
import Router from 'vue-router';
import Home from '../src/Views/MainPage.vue';
import EnterPage from '../src/Views/EnterPage.vue';
import RegisterPage from '../src/Views/RegistrationPage.vue';
import UserInfoPage from '../src/Views/UserInfoPage.vue';

Vue.use(Router);

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/enter',
            name: 'enter',
            component: EnterPage,
            meta: { hideFooter: true },
        },
        {
            path: '/registr',
            name: 'registr',
            component: RegisterPage,
            meta: { hideFooter: true },
        },
        {
            path: '/userInfo',
            name: 'UserInfoPage',
            component: UserInfoPage
        },
    ],
});

export default router;
