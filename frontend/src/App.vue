<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { Bars3Icon } from "@heroicons/vue/24/outline";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;
</script>

<template>
  <header>
    <nav
      class="container sticky mx-auto flex flex-row justify-between border-b p-4"
    >
      <RouterLink to="/" class="text-sm font-bold">
        {{ BRAND_HOTEL_NAME }}
      </RouterLink>

      <button class="block md:hidden">
        <span class="sr-only">Open menu</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <div
        class="hidden flex-row gap-x-8 text-sm font-semibold text-gray-900 md:flex"
      >
        <a href="/admin">Django admin page</a>
        <RouterLink to="/vue-admin">Admin page</RouterLink>
      </div>
    </nav>
  </header>

  <RouterView />
</template>
