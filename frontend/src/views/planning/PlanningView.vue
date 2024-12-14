<script setup lang="ts">
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import PlanningViewClasses from "@/views/planning/PlanningViewClasses.vue";
import type { Class, Service } from "@/types";
import { ref } from "vue";
import PlanningViewServices from "@/views/planning/PlanningViewServices.vue";

const classes = ref<Class[]>([]);
const services = ref<Service[]>([]);

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
    <PlanningViewClasses v-model="classes" />
    <PlanningViewServices v-model="services" :classes="classes" />
  </main>
</template>
