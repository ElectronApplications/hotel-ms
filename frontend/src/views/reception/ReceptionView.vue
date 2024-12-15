<script setup lang="ts">
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import ReceptionViewClients from "@/views/reception/ReceptionViewClients.vue";
import ReceptionViewAccomodations from "@/views/reception/ReceptionViewAccomodations.vue";

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "reception" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <ReceptionViewClients />
    <ReceptionViewAccomodations />
  </main>
</template>
