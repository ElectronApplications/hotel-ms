<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthentication } from "@/composables/auth";
import router from "@/router";

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <SurfaceCard>book</SurfaceCard>
  </main>
</template>
