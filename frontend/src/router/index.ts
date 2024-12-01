import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import LoginView from "@/views/LoginView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ChangePasswordView from "@/views/ChangePasswordView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: MainView,
    },
    {
      path: "/login",
      component: LoginView,
    },
    {
      path: "/profile",
      component: ProfileView,
    },
    {
      path: "/change-password",
      component: ChangePasswordView,
    },
  ],
});

export default router;
