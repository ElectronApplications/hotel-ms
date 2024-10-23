<script setup lang="ts">
const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;
</script>

<template>
  <main class="container mx-auto pt-5">
    <h1 class="text-4xl font-extrabold">
      Welcome to the hotel {{ BRAND_HOTEL_NAME }}!
    </h1>
    <h2 class="text-2xl font-bold">
      We are going to provide you with the best hotel experience!
    </h2>
  </main>
</template>
