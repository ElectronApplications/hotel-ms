<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "service" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <SurfaceCard>service</SurfaceCard>
  </main>
</template>
