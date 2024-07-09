import { createRouter, createWebHistory } from 'vue-router';
import Home from '../Views/MainPage.vue';
import ChatBotPage from '../Views/ChatBotPage.vue';
import StatPage from '../Views/StatisticPage.vue';
import Doc from '../Views/DocPage.vue';
import List from '../Views/ListPage.vue';
import Enter from '../Views/EnterPage.vue';
import Registr from '../Views/RegistrationPage.vue';
import UserInfoPage from '../Views/UserInfoPage.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },{
        path: '/chat-bot',
        name: 'ChatBot',
        component: ChatBotPage,
    },{
        path: '/statistic-page',
        name: 'Statistic',
        component: StatPage,
    },{
        path: '/doc',
        name: 'Document',
        component: Doc
    },{
        path: '/list',
        name: 'Lists',
        component: List
    },{
        path: '/enter',
        name: 'Enter',
        component: Enter
    },{
        path: '/registr',
        name: 'Registr',
        component: Registr
    },{
        path: '/userInfo',
        name: 'UserInfoPage',
        component: UserInfoPage
    },
    
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
