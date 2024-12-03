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
  if (role !== "cleaning" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <SurfaceCard>cleaning</SurfaceCard>
  </main>
</template>
