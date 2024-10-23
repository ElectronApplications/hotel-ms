import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import AdminView from "@/views/AdminView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: MainView,
    },
    {
      path: "/vue-admin",
      component: AdminView,
    },
  ],
});

export default router;
