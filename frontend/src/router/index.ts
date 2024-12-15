import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import LoginView from "@/views/LoginView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ChangePasswordView from "@/views/ChangePasswordView.vue";
import ReceptionView from "@/views/ReceptionView.vue";
import ServiceView from "@/views/ServiceView.vue";
import CleaningView from "@/views/CleaningView.vue";
import PlanningView from "@/views/planning/PlanningView.vue";
import AdminView from "@/views/AdminView.vue";
import BookView from "@/views/BookView.vue";
import GalleryView from "@/views/GalleryView.vue";

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
    {
      path: "/management/reception",
      component: ReceptionView,
    },
    {
      path: "/management/service",
      component: ServiceView,
    },
    {
      path: "/management/cleaning",
      component: CleaningView,
    },
    {
      path: "/management/planning",
      component: PlanningView,
    },
    {
      path: "/management/admin",
      component: AdminView,
    },
    {
      path: "/book",
      component: BookView,
    },
    {
      path: "/gallery/:id",
      component: GalleryView,
    },
  ],
});

export default router;
