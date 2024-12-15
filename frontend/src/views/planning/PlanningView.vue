<script setup lang="ts">
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import PlanningViewClasses from "@/views/planning/PlanningViewClasses.vue";
import type { Class, Gallery, Room, Service } from "@/types";
import { onMounted, ref } from "vue";
import PlanningViewServices from "@/views/planning/PlanningViewServices.vue";
import PlanningViewRooms from "./PlanningViewRooms.vue";
import axios from "axios";

const galleries = ref<Gallery[]>([]);
const classes = ref<Class[]>([]);
const services = ref<Service[]>([]);
const rooms = ref<Room[]>([]);

async function fetchGalleries() {
  galleries.value = (await axios.get("/api/gallery/")).data;
}

onMounted(() => {
  fetchGalleries();
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "planning" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <PlanningViewClasses v-model="classes" :galleries="galleries" />
    <PlanningViewServices
      v-model="services"
      :classes="classes"
      :galleries="galleries"
    />
    <PlanningViewRooms v-model="rooms" :classes="classes" />
  </main>
</template>
